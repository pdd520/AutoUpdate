import requests
import json
import base64
import os
import time
import random
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URLS_FILE = os.path.join(BASE_DIR, 'getnodelist.txt')
OUTPUT_FILE = os.path.abspath(os.path.join(BASE_DIR, '../nodes/nodes.txt'))
ACCOUNTS_FILE = os.path.join(BASE_DIR, 'registered_accounts.txt')

# 统一密码
UNIFIED_PASSWORD = '@lluPCwCyfh7Gf'

# 添加重试配置
MAX_RETRIES = 3
RETRY_DELAY = 2

def read_urls(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('')
        print(f'未找到 {file_path}，已自动创建空文件，请填写节点接口后重新运行。')
        exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        print(f'{file_path} 为空，请填写节点接口后重新运行。')
        exit(1)
    return lines

def need_email_code(html_text):
    return 'email_code' in html_text or '邮箱验证码' in html_text

def has_slider_or_cloudflare(html_text):
    keywords = ['slider', 'geetest', 'cloudflare', 'cf-challenge', '验证码']
    return any(kw in html_text.lower() for kw in keywords)

def generate_random_gmail():
    """生成随机Gmail邮箱"""
    # 生成随机用户名部分
    username_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    username = ''.join(random.choice(username_chars) for _ in range(random.randint(8, 12)))
    
    # 添加随机数字后缀
    random_suffix = random.randint(100, 999)
    
    # 生成邮箱
    email = f'{username}{random_suffix}@gmail.com'
    print(f'[生成邮箱] 随机Gmail邮箱: {email}')
    return email

def save_account_info(website_url, email, password, status):
    """保存注册的账号信息到文件"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    account_info = f'时间: {timestamp} | 网址: {website_url} | 邮箱: {email} | 密码: {password} | 状态: {status}\n'
    
    try:
        with open(ACCOUNTS_FILE, 'a', encoding='utf-8') as f:
            f.write(account_info)
        print(f'[保存账号] 账号信息已保存到 {ACCOUNTS_FILE}')
    except Exception as e:
        print(f'[保存账号] 保存账号信息失败: {e}')

def safe_request(session, url, method='GET', data=None, timeout=10, max_retries=MAX_RETRIES):
    """安全的网络请求，带重试机制"""
    for attempt in range(max_retries):
        try:
            if method.upper() == 'GET':
                response = session.get(url, timeout=timeout)
            else:
                response = session.post(url, data=data, timeout=timeout)
            return response
        except requests.exceptions.Timeout:
            print(f'[网络请求] 第{attempt+1}次请求超时: {url}')
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
                continue
            else:
                raise
        except requests.exceptions.RequestException as e:
            print(f'[网络请求] 第{attempt+1}次请求失败: {url} - {e}')
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
                continue
            else:
                raise
    return None

def auto_register(session, base_url, email, password):
    register_url = base_url + '/auth/register'
    print(f'[注册] 开始注册: {register_url}')
    print(f'[注册] 使用邮箱: {email}')
    print(f'[注册] 使用密码: {password}')
    
    try:
        page = safe_request(session, register_url)
        if page is None:
            return False
            
        html = page.text
        if need_email_code(html):
            print(f'[注册] {register_url} 需要邮箱验证码，跳过注册')
            return False
        if has_slider_or_cloudflare(html):
            print(f'[注册] {register_url} 检测到滑动/Cloudflare验证，尝试自动通过（当前直接跳过）')
            return False
    except Exception as e:
        print(f'[注册] 获取注册页面失败: {e}')
        return False
    
    data = {
        'email': email,
        'passwd': password,
        'repasswd': password,
        'invite_code': '',
        'email_code': '',
    }
    
    print(f'[注册] 发送注册请求...')
    try:
        resp = safe_request(session, register_url, method='POST', data=data)
        if resp is None:
            return False
            
        print(f'[注册] {register_url} 返回状态码: {resp.status_code}')
        print(f'[注册] {register_url} 返回内容: {resp.text}')
        
        # 新增：支持JSON返回的注册成功
        try:
            resp_json = resp.json()
            if resp.status_code == 200 and resp_json.get('ret') == 1:
                print(f'[注册] 注册成功 (JSON响应)')
                return True
        except Exception:
            pass
        
        success = resp.status_code == 200 and ('成功' in resp.text or '注册成功' in resp.text)
        if success:
            print(f'[注册] 注册成功 (文本响应)')
        else:
            print(f'[注册] 注册失败')
        
        return success
    except Exception as e:
        print(f'[注册] 注册请求失败: {e}')
        return False

def auto_login(session, base_url, email, password):
    login_url = base_url + '/auth/login'
    print(f'[登录] 开始登录: {login_url}')
    print(f'[登录] 使用邮箱: {email}')
    
    data = {
        'email': email,
        'passwd': password,
        'remember_me': 'on'
    }
    
    print(f'[登录] 发送登录请求...')
    try:
        resp = safe_request(session, login_url, method='POST', data=data)
        if resp is None:
            return False
            
        print(f'[登录] {login_url} 返回状态码: {resp.status_code}')
        print(f'[登录] {login_url} 返回内容: {resp.text}')
        
        try:
            resp_json = resp.json()
            success = resp.status_code == 200 and resp_json.get('ret') == 1
            if success:
                print(f'[登录] 登录成功 (JSON响应)')
            else:
                print(f'[登录] 登录失败 (JSON响应)')
            return success
        except Exception:
            success = resp.status_code == 200 and ('成功' in resp.text or '登录成功' in resp.text)
            if success:
                print(f'[登录] 登录成功 (文本响应)')
            else:
                print(f'[登录] 登录失败 (文本响应)')
            return success
    except Exception as e:
        print(f'[登录] 登录请求失败: {e}')
        return False

def get_nodes(session, base_url):
    node_url = base_url + '/getnodelist'
    print(f'[获取节点] 请求节点列表: {node_url}')
    
    try:
        resp = safe_request(session, node_url)
        if resp is None:
            return None
            
        print(f'[获取节点] {node_url} 返回状态码: {resp.status_code}')
        print(f'[获取节点] {node_url} 返回内容: {resp.text[:200]}...')
        
        if resp.status_code == 200:
            try:
                return resp.json()
            except Exception as e:
                print(f'[获取节点] JSON解析失败: {e}')
                return None
        return None
    except Exception as e:
        print(f'[获取节点] 请求失败: {e}')
        return None

def process_node_data(data):
    links = []
    if not data or data.get('ret') != 1 or not data.get('nodeinfo'):
        print(f'[处理节点] 数据格式无效或ret!=1')
        return links
    
    nodeinfo = data['nodeinfo']
    print(f'[处理节点] 开始处理节点数据...')
    
    if 'nodes_muport' in nodeinfo and nodeinfo['nodes_muport'] and 'user' in nodeinfo['nodes_muport'][0]:
        user_info = nodeinfo['nodes_muport'][0]['user']
    else:
        user_info = nodeinfo['user']
    
    # 安全获取用户信息
    try:
        uuid = user_info.get('uuid', '')
        ss_password = user_info.get('passwd', '')
        method = user_info.get('method', '')
        
        if not uuid or not ss_password or not method:
            print(f'[处理节点] 用户信息不完整: uuid={uuid}, passwd={ss_password}, method={method}')
            return links
    except Exception as e:
        print(f'[处理节点] 获取用户信息失败: {e}')
        return links
    
    print(f'[处理节点] UUID: {uuid}')
    print(f'[处理节点] SS密码: {ss_password}')
    print(f'[处理节点] 加密方法: {method}')
    
    node_count = 0
    for node in nodeinfo['nodes']:
        try:
            raw_node = node['raw_node']
            node_count += 1
            print(f'[处理节点] 处理第{node_count}个节点: {raw_node["name"]}')
        except Exception as e:
            print(f'[处理节点] 跳过无效节点: {e}')
            continue
        
        # 解析raw_node.server字段中的参数
        server_str = raw_node.get('server', '')
        print(f'[处理节点] 原始server字段: {server_str}')
        
        try:
            # 首先尝试原有的解析逻辑
            if ';port=' in server_str:
                # 原有的SS节点处理逻辑
                server = server_str.split(';port=')[0]
                port = server_str.split('#')[1]
                ss_link = f'{method}:{ss_password}@{server}:{port}'
                ss_link_encoded = base64.b64encode(ss_link.encode()).decode()
                final_link = f'ss://{ss_link_encoded}#{raw_node["name"]}'
                links.append(final_link)
                print(f'[处理节点] 生成SS链接: {final_link[:50]}...')
            elif server_str.count(';') >= 3:
                # 原有的VMess节点处理逻辑
                server_parts = server_str.split(';')
                server = server_parts[0]
                port = server_parts[1]
                aid = server_parts[2] if len(server_parts) > 2 else '64'
                net = server_parts[3] if len(server_parts) > 3 else 'ws'
                host = ''
                path = ''
                if len(server_parts) > 5 and server_parts[5]:
                    for part in server_parts[5].split('|'):
                        if part.startswith('path='):
                            path = part[5:]
                        elif part.startswith('host='):
                            host = part[5:]
                vmess_config = {
                    "v": "2",
                    "ps": raw_node["name"],
                    "add": server,
                    "port": port,
                    "id": uuid,
                    "aid": str(aid),
                    "net": net,
                    "type": "none",
                    "host": host,
                    "path": path,
                    "tls": ""
                }
                vmess_link = base64.b64encode(json.dumps(vmess_config).encode()).decode()
                final_link = f'vmess://{vmess_link}'
                links.append(final_link)
                print(f'[处理节点] 生成VMess链接: {final_link[:50]}...')
            else:
                # 新增：处理特殊格式（包含server=、outside_port=等参数）
                print(f'[处理节点] 使用新格式解析...')
                
                # 提取server地址
                server = ''
                if 'server=' in server_str:
                    server = server_str.split('server=')[1].split('|')[0].split(';')[0]
                else:
                    # 如果找不到server=，尝试其他方式
                    if server_str.count(';') >= 1:
                        server = server_str.split(';')[0]
                    else:
                        server = server_str
                
                # 提取端口
                port = ''
                if 'outside_port=' in server_str:
                    port = server_str.split('outside_port=')[1].split('|')[0]
                elif ';port=' in server_str:
                    port = server_str.split(';port=')[1].split('#')[0]
                elif server_str.count(';') >= 2:
                    port = server_str.split(';')[1]
                else:
                    # 如果都找不到，使用默认端口
                    port = '443'
                
                # 提取路径
                path = ''
                if 'path=' in server_str:
                    path_part = server_str.split('path=')[1].split('|')[0]
                    path = path_part.replace('\\/', '/')  # 处理转义字符
                
                # 提取主机
                host = ''
                if 'host=' in server_str:
                    host = server_str.split('host=')[1].split('|')[0]
                
                print(f'[处理节点] 新格式解析结果 - 服务器: {server}, 端口: {port}, 路径: {path}, 主机: {host}')
                
                # 判断是SS还是VMess
                if 'ws' in server_str or 'tcp' in server_str or 'http' in server_str:
                    # VMess节点
                    aid = '64'  # 默认值
                    net = 'ws'  # 默认值
                    
                    # 尝试从server字段提取aid和net
                    if server_str.count(';') >= 3:
                        server_parts = server_str.split(';')
                        if len(server_parts) > 2:
                            aid = server_parts[2]
                        if len(server_parts) > 3:
                            net = server_parts[3]
                    
                    vmess_config = {
                        "v": "2",
                        "ps": raw_node["name"],
                        "add": server,
                        "port": port,
                        "id": uuid,
                        "aid": str(aid),
                        "net": net,
                        "type": "none",
                        "host": host,
                        "path": path,
                        "tls": ""
                    }
                    vmess_link = base64.b64encode(json.dumps(vmess_config).encode()).decode()
                    final_link = f'vmess://{vmess_link}'
                    links.append(final_link)
                    print(f'[处理节点] 生成VMess链接: {final_link[:50]}...')
                else:
                    # SS节点
                    ss_link = f'{method}:{ss_password}@{server}:{port}'
                    ss_link_encoded = base64.b64encode(ss_link.encode()).decode()
                    final_link = f'ss://{ss_link_encoded}#{raw_node["name"]}'
                    links.append(final_link)
                    print(f'[处理节点] 生成SS链接: {final_link[:50]}...')
        except Exception as e:
            print(f'[处理节点] 处理节点时出错: {e}')
            continue
    
    print(f'[处理节点] 总共处理了 {node_count} 个节点，生成了 {len(links)} 个链接')
    return links

def main():
    print(f'[主程序] 开始运行自动注册和获取节点程序')
    print(f'[主程序] 统一密码: {UNIFIED_PASSWORD}')
    print(f'[主程序] 账号保存文件: {ACCOUNTS_FILE}')
    print(f'[主程序] 节点保存文件: {OUTPUT_FILE}')
    
    # 先清空账号文件
    with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
        pass
    # 创建账号记录文件头部
    if not os.path.exists(ACCOUNTS_FILE):
        header = f'=== 自动注册账号记录 ===\n'
        header += f'开始时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
        header += f'统一密码: {UNIFIED_PASSWORD}\n'
        header += f'格式: 时间 | 网址 | 邮箱 | 密码 | 状态\n'
        header += f'{"="*50}\n'
        with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
            f.write(header)
        print(f'[主程序] 创建账号记录文件: {ACCOUNTS_FILE}')
    else:
        # 如果文件已存在，检查是否有头部信息
        with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.startswith('=== 自动注册账号记录 ==='):
            # 如果没有头部信息，添加头部
            header = f'=== 自动注册账号记录 ===\n'
            header += f'开始时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
            header += f'统一密码: {UNIFIED_PASSWORD}\n'
            header += f'格式: 时间 | 网址 | 邮箱 | 密码 | 状态\n'
            header += f'{"="*50}\n'
            with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                f.write(header + content)
            print(f'[主程序] 为现有账号记录文件添加头部信息: {ACCOUNTS_FILE}')
    
    try:
        urls = read_urls(URLS_FILE)
        print(f'[主程序] 读取到 {len(urls)} 个网址')
        
        all_links = []
        success_count = 0
        register_count = 0
        
        for i, url in enumerate(urls, 1):
            print(f'\n[主程序] 处理第 {i}/{len(urls)} 个网址: {url}')
            
            try:
                base_url = url.split('/getnodelist')[0]
                session = requests.Session()
                
                # 使用更长的超时时间进行请求
                
                try:
                    resp = safe_request(session, url, timeout=15)
                    if resp is None:
                        print(f'[跳过] 访问 {url} 失败，网络请求超时或连接失败')
                        save_account_info(url, '', '', '跳过-网络请求失败')
                        continue
                        
                    try:
                        data = resp.json()
                    except Exception as e:
                        print(f'[跳过] {url} 返回内容不是JSON: {e}')
                        save_account_info(url, '', '', f'跳过-非JSON响应: {e}')
                        continue
                except Exception as e:
                    print(f'[跳过] 访问 {url} 失败: {e}')
                    save_account_info(url, '', '', f'跳过-访问失败: {e}')
                    continue
                
                # 只在 ret == -1 时注册，否则直接跳过注册
                if data.get('ret') == -1:
                    print(f'[主程序] 需要注册新账号')
                    register_count += 1
                    email = generate_random_gmail()
                    
                    reg_ok = auto_register(session, base_url, email, UNIFIED_PASSWORD)
                    if reg_ok:
                        print(f'[主程序] 注册成功，尝试登录...')
                        login_ok = auto_login(session, base_url, email, UNIFIED_PASSWORD)
                        if login_ok:
                            print(f'[主程序] 登录成功，获取节点数据...')
                            data = get_nodes(session, base_url)
                            if data and data.get('ret') == 1:
                                links = process_node_data(data)
                                all_links.extend(links)
                                success_count += 1
                                print(f'[主程序] 注册+登录+获取成功，添加了 {len(links)} 个节点')
                                save_account_info(url, email, UNIFIED_PASSWORD, '成功-注册+登录+获取节点')
                            else:
                                print(f'[主程序] 注册和登录成功，但未获取到节点数据')
                                save_account_info(url, email, UNIFIED_PASSWORD, '部分成功-注册+登录成功但无节点数据')
                        else:
                            print(f'[主程序] 注册成功，但登录失败')
                            save_account_info(url, email, UNIFIED_PASSWORD, '部分成功-注册成功但登录失败')
                    else:
                        print(f'[主程序] 注册失败或需要验证码/Cloudflare')
                        save_account_info(url, email, UNIFIED_PASSWORD, '失败-注册失败或需要验证')
                else:
                    # 只处理 ret==1 的情况
                    if data.get('ret') == 1:
                        print(f'[主程序] 直接获取节点数据（无需注册）')
                        links = process_node_data(data)
                        all_links.extend(links)
                        success_count += 1
                        print(f'[主程序] 直接获取成功，添加了 {len(links)} 个节点')
                        save_account_info(url, '', '', '成功-直接获取节点')
                    else:
                        print(f'[主程序] 跳过，未返回有效节点(ret!=1)')
                        save_account_info(url, '', '', f'跳过-ret={data.get("ret")}')
                        
            except Exception as e:
                print(f'[主程序] 处理 {url} 时出错: {e}')
                save_account_info(url, '', '', f'错误-处理失败: {e}')
                continue
        
        # 保存所有节点到 nodes/nodes.txt
        print(f'\n[主程序] 开始保存节点数据...')
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_links))
        
        # 输出统计信息
        print(f'\n[主程序] ===== 运行统计 =====')
        print(f'[主程序] 总处理网址数: {len(urls)}')
        print(f'[主程序] 尝试注册数: {register_count}')
        print(f'[主程序] 成功获取节点数: {success_count}')
        print(f'[主程序] 总获取节点数: {len(all_links)}')
        print(f'[主程序] 节点保存位置: {OUTPUT_FILE}')
        print(f'[主程序] 账号记录位置: {ACCOUNTS_FILE}')
        print(f'[主程序] ===================')
        
    except Exception as e:
        print(f'[主程序] 运行出错: {e}')
        # 不再 exit(1)，而是继续

if __name__ == '__main__':
    main() 
