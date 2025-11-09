def sanitize_filename(filename):
    """清理文件名，移除Windows不允许的字符"""
    # Windows不允许的字符: < > : " | ? * \ /
    # 将 : 替换为 _
    # 将 / 替换为 _
    # 将 \ 替换为 _
    # 移除其他不允许的字符
    filename = re.sub(r'[<>:"|?*\\/]', '_', filename)
    filename = filename.replace(':', '_')
    return filename

from urllib.parse import urlparse
import re
import os
import string
import secrets
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from datetime import timedelta
from random import choice
from time import time  # 修改：保留 from time import time
import time  # 新增：导入整个 time 模块，支持 time.sleep
from urllib.parse import urlsplit, urlunsplit
import multiprocessing
import requests  # 用于下载远程文件

from apis import PanelSession, TempEmail, guess_panel, panel_class_map
from subconverter import gen_base64_and_clash_config, get
from utils import (clear_files, g0, keep, list_file_paths, list_folder_paths,
                   read, read_cfg, remove, size2str, str2timestamp,
                   timestamp2str, to_zero, write, write_cfg)

# 全局配置
MAX_WORKERS = min(16, multiprocessing.cpu_count() * 2)  # 动态设置最大工作线程数
MAX_TASK_TIMEOUT = 45  # 单任务最大等待时间（秒）
DEFAULT_EMAIL_DOMAINS = ['gmail.com', 'qq.com', 'outlook.com']  # 默认邮箱域名池

# ... (以下函数保持不变：generate_random_username, get_available_domain, log_error, get_sub, should_turn, _register, _get_email_and_email_code, register, is_checkin, try_checkin, try_buy, do_turn, try_turn, cache_sub_info, save_sub_base64_and_clash, save_sub, get_and_save, new_panel_session, get_trial, build_options)

# 修改：下载远程配置函数，支持重试（不变，但现在 time.sleep 可用）
def download_remote_cfg(url: str, max_retries: int = 3) -> str:
    """下载远程 trial.cfg 内容"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text.strip()
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"下载远程配置失败（重试 {max_retries} 次）: {e}")
            time.sleep(1)  # 等待 1 秒重试（现在已导入 time 模块）

# 修改：智能处理 Secrets URL，支持多行 URL 列表或单个远程文件 URL
def parse_secrets_or_remote() -> dict:
    """从 Secrets 或本地文件读取配置，返回类似 read_cfg('trial.cfg')['default'] 的结构"""
    # 优先从 Secrets 取 URL（不打印 URL 以防日志暴露）
    secret_url = os.environ.get('TRIAL_CFG_URL')
    source = '本地文件'  # 默认
    if secret_url:
        secret_url_stripped = secret_url.strip()
        lines = [line.strip() for line in secret_url_stripped.split('\n') if line.strip() and not line.startswith('#')]
        
        if len(lines) == 1 and lines[0].startswith('http'):
            # 情况1：单个远程文件 URL，下载并解析
            try:
                content = download_remote_cfg(lines[0])
                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                source = 'Secrets URL（远程文件）'
                print(f"使用 Secrets URL 下载配置（主机数: {len(lines)}）", flush=True)
            except Exception as e:
                print(f"Secrets URL 下载失败: {e}，fallback 到本地 trial.cfg", flush=True)
                # fallback 到本地
                cfg_dict = read_cfg('trial.cfg')
                if not cfg_dict.get('default'):
                    raise Exception("无有效配置：Secrets 下载失败且本地 trial.cfg 为空")
                return cfg_dict
        else:
            # 情况2：多行 URL 列表（每行一个 URL 或带选项），直接解析
            source = 'Secrets URL（直接列表）'
            print(f"使用 Secrets URL 直接解析配置（主机数: {len(lines)}）", flush=True)
        
        # 统一解析逻辑：每行一个条目，支持 'url key=value' 格式
        config = []
        for line in lines:
            parts = line.split(maxsplit=1)  # 支持空格分隔选项
            if len(parts) == 1:
                config.append([parts[0]])  # 纯 URL
            else:
                # 支持选项，如 'url reg_limit=3' → ['url', 'reg_limit', '3']
                url = parts[0]
                options = parts[1].split()
                entry = [url] + [opt for opt in options if '=' in opt]  # 只取 key=value
                config.append(entry)
        
        print(f"配置解析完成（来源: {source}，主机数: {len(config)}）", flush=True)
        return {'default': config}
    else:
        # 无 Secrets，fallback 到本地文件
        cfg_dict = read_cfg('trial.cfg')
        if not cfg_dict.get('default'):
            raise Exception("请设置 TRIAL_CFG_URL Secrets 或提供本地 trial.cfg 文件")
        print("使用本地 trial.cfg 文件配置", flush=True)
        return cfg_dict

if __name__ == '__main__':
    pre_repo = read('.github/repo_get_trial')
    cur_repo = os.getenv('GITHUB_REPOSITORY')
    if pre_repo != cur_repo and cur_repo is not None:
        remove('trial.cache')
        write('.github/repo_get_trial', cur_repo)

    # 使用新解析函数获取 cfg（无硬编码）
    cfg_dict = parse_secrets_or_remote()
    cfg = cfg_dict['default']
    
    opt = build_options(cfg)
    cache = read_cfg('trial.cache', dict_items=True)

    for host in [*cache]:
        if host not in opt:
            del cache[host]

    for path in list_file_paths('trials'):
        host, ext = os.path.splitext(os.path.basename(path))
        if ext != '.yaml':
            host += ext
        else:
            host = host.split('_')[0]
        if host not in opt:
            remove(path)

    for path in list_folder_paths('trials_providers'):
        host = os.path.basename(path)
        if '.' in host and host not in opt:
            clear_files(path)
            remove(path)

    with ThreadPoolExecutor(MAX_WORKERS) as executor:
        futures = []
        args = [(h, opt[h], cache[h]) for h, *_ in cfg]
        for h, o, c in args:
            futures.append(executor.submit(get_trial, h, o, c))
        for future in as_completed(futures):
            try:
                log = future.result(timeout=MAX_TASK_TIMEOUT)
                for line in log:
                    print(line, flush=True)
            except TimeoutError:
                print("有任务超时（超过45秒未完成），已跳过。", flush=True)
            except Exception as e:
                print(f"任务异常: {e}", flush=True)

    total_node_n = gen_base64_and_clash_config(
        base64_path='trial',
        clash_path='trial.yaml',
        providers_dir='trials_providers',
        base64_paths=(path for path in list_file_paths('trials') if os.path.splitext(path)[1].lower() != '.yaml'),
        providers_dirs=list_folder_paths('trials_providers')
    )

    print('总节点数', total_node_n)
    write_cfg('trial.cache', cache)
