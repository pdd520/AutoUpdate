# sub - 自动化代理节点收集和管理项目

## 项目概述

`sub` 是一个自动化代理节点收集和管理项目，主要用于从各种机场（代理服务商）获取试用订阅、收集代理节点、生成配置文件，并提供多种格式的订阅服务。项目包含多个 Python 脚本，每个脚本都有特定的功能和用途。


## 核心 Python 脚本详细说明

### 根目录核心脚本

#### 1. `TG_proxy_main.py` - Telegram代理收集主程序
**功能概述：** 从Telegram频道和机场网站收集代理节点的主要脚本

**核心功能：**
- **大规模机场支持**：内置760+个试用机场URL列表
- **多线程并发处理**：高效处理大量机场订阅链接
- **智能解码系统**：自动解析Base64编码的订阅内容
- **多协议兼容**：支持SS、SSR、VMess、Trojan、Hysteria2等主流协议
- **多格式输出**：同时生成Clash和V2Ray格式配置文件
- **实时监控**：提供详细的进度显示和错误处理机制

**主要函数详解：**
- `get_channel_http()` - HTTP频道内容获取，支持自定义请求头和超时设置
- `jiemi_base64()` - Base64解密处理，智能识别编码格式
- `get_content()` - 多线程内容获取引擎，支持并发控制和错误重试
- `write_document()` - 文档写入和格式化，支持多种输出格式
- `get_yaml()` - YAML配置生成器，自动生成Clash配置结构
- `get_sub_url()` - 订阅URL获取和验证
- `get_kkzui()` - 特定站点内容获取，针对特殊格式优化

**输出文件结构：**
- `sub/clash.yaml` - 标准Clash配置文件
- `sub/v2ray.txt` - V2Ray订阅链接集合
- `sub/base64.txt` - Base64编码节点列表

**性能优化特性：**
- 智能重试机制，自动处理网络异常
- 内存友好的流式处理
- 动态线程池管理
- 结果缓存和去重

#### 2. `main.py` - IPTV频道聚合处理器
**功能概述：** 专门处理IPTV直播源的聚合、验证和管理工具

**核心功能：**
- **智能源发现**：从GitHub等聚合源自动发现IPTV链接
- **多格式支持**：完整支持m3u、m3u8、txt格式的播放列表
- **协议兼容性**：支持HTTP、HTTPS、RTMP、RTP、P3P等多种直播协议
- **智能分类**：自动识别和分类不同类型的频道
- **CCTV优化**：专门针对CCTV频道的特殊处理和排序
- **质量控制**：自动清理无效链接和重复内容

**协议支持详解：**
- **HTTP/HTTPS**：标准网络直播流，支持HLS和DASH
- **RTMP**：实时消息传输协议，适用于推流服务
- **RTP**：实时传输协议，支持组播和单播
- **P3P**：点对点协议，支持分布式直播

**核心算法：**
- `fetch_url_content_with_retry()` - 智能重试机制的URL获取
- `check_url_validity()` - 多协议URL有效性检测
- `process_urls_multithreaded()` - 高效的多线程URL处理引擎
- `sort_cctv_channels()` - CCTV频道智能排序算法
- `auto_discover_and_update_urls_file()` - 自动发现和更新机制

**GitHub集成特性：**
- 自动搜索GitHub上的IPTV资源
- 智能解析仓库结构
- 版本控制和更新追踪
- 批量处理和合并

#### 3. `Telegram Subscriptions.py` - Telegram订阅爬虫
**功能概述：** 专门从Telegram频道爬取代理订阅链接的高级爬虫系统

**环境变量配置系统：**
- `SEARCH_KEYWORDS_ENV` - 搜索关键词列表，支持正则表达式
- `SUBSCRIPTION_TARGET_REPO` - 目标GitHub仓库，支持私有仓库
- `SUBSCRIPTION_SAVE_PATH` - 保存路径，支持动态路径生成
- `CONFIG_REPO_NAME` - 配置仓库名称，支持多仓库管理
- `CONFIG_FILE_PATH` - 配置文件路径，支持嵌套目录
- `GT_TOKEN` - GitHub访问令牌，支持细粒度权限控制

**高级爬虫特性：**
- **User-Agent轮换**：内置90+种真实浏览器User-Agent
- **智能分页**：自动识别和处理Telegram的分页机制
- **连通性测试**：实时验证爬取到的URL可用性
- **GitHub API集成**：完整的GitHub仓库操作支持
- **多线程队列**：高效的工作队列和任务分发
- **错误恢复**：智能的错误检测和自动恢复机制

**爬虫工作流程：**
1. **配置初始化**：从GitHub读取配置文件获取起始URL和参数
2. **多线程爬取**：并发爬取多个Telegram页面
3. **内容解析**：使用正则表达式和HTML解析提取订阅链接
4. **质量验证**：测试链接的连通性和有效性
5. **数据持久化**：将验证通过的链接保存到GitHub仓库
6. **状态同步**：更新爬取状态和统计信息

**反爬虫对策：**
- 随机延时机制
- IP轮换支持
- 请求头伪装
- 会话保持
- 错误重试策略

#### 4. `get_trial.py` - 试用机场自动注册脚本
**功能概述：** 自动化注册试用机场账号并获取订阅链接的核心脚本

**主要特性：**
- **多面板支持**：兼容V2board、SSPanel、Sspanel-Uim等主流机场面板
- **临时邮箱集成**：集成TempMail、Guerrilla Mail、10MinuteMail等多个服务
- **验证码处理**：智能验证码识别和自动处理
- **并发优化**：多线程并发处理，显著提高效率
- **重试机制**：智能重试和错误恢复
- **代理支持**：支持代理池轮换，避免IP封禁

**工作流程详解：**
1. **配置解析**：读取trial.cfg配置文件，解析机场列表
2. **邮箱生成**：为每个机场生成独立的临时邮箱
3. **自动注册**：模拟浏览器行为，自动填写注册表单
4. **邮箱验证**：自动获取验证邮件并完成验证
5. **账号登录**：使用注册信息登录机场面板
6. **订阅获取**：提取用户专属的订阅链接
7. **链接验证**：验证订阅链接的有效性和节点质量
8. **结果保存**：将有效订阅保存到指定文件

**命令行参数详解：**
- `--thread` - 并发线程数（默认64，可根据系统性能调整）
- `--timeout` - 请求超时时间（秒）
- `--proxy` - 代理服务器地址（支持HTTP/SOCKS5）
- `--output` - 输出文件路径（支持相对和绝对路径）
- `--debug` - 启用调试模式（详细日志输出）
- `--retry` - 重试次数（默认3次）
- `--delay` - 请求间隔（毫秒）

#### 5. `get_trial_update_url.py` - 机场URL更新脚本
**功能概述：** 维护和更新机场URL列表，确保数据源的时效性和可用性

**核心功能：**
- **失效检测**：自动检测和标记失效的机场URL
- **多源补充**：从多个数据源自动补充新的机场地址
- **可用性验证**：全面验证机场的可访问性和注册可用性
- **配置更新**：智能更新配置文件中的URL列表
- **状态报告**：生成详细的机场状态和质量报告

**数据源管理：**
- **Telegram频道**：实时监控Telegram频道的新机场分享
- **GitHub仓库**：监控相关GitHub项目的更新
- **机场导航**：定期抓取机场导航站点的最新信息
- **用户提交**：处理用户提交的新机场地址
- **历史数据库**：维护历史有效地址库，支持地址恢复

#### 6. `ClashForge.py` - Clash配置生成器
**功能概述：** 将收集的节点转换为Clash配置文件的专业工具

**核心功能：**
- **多协议解析**：支持SS、SSR、VMess、Trojan、Hysteria2、VLESS等
- **智能分组**：根据地理位置、协议类型、速度等自动分组
- **规则集成**：集成自定义代理规则和分流规则
- **性能测试**：内置节点测速和质量筛选
- **模板系统**：支持多种配置模板和自定义模板

**配置特性：**
- **地理分组**：自动按国家/地区分组节点
- **负载均衡**：支持轮询、随机、一致性哈希等策略
- **故障转移**：自动检测和切换失效节点
- **自定义规则**：支持域名、IP、GEOIP等多种规则
- **DNS优化**：智能DNS配置和解析优化
- **广告拦截**：内置广告拦截和隐私保护规则

#### 7. `subconverter.py` - 订阅转换核心模块
**功能概述：** 实现多种代理协议间的转换和格式标准化

**输入格式支持：**
- **SS/SSR订阅**：标准Shadowsocks和ShadowsocksR订阅链接
- **VMess链接**：V2Ray VMess协议分享链接
- **Trojan链接**：Trojan协议配置链接
- **Hysteria链接**：Hysteria/Hysteria2高速协议链接
- **原始配置**：各种原始配置文件格式

**输出格式支持：**
- **Clash配置**：标准Clash YAML配置文件
- **V2Ray配置**：V2Ray JSON配置文件
- **Quantumult X**：Quantumult X专用配置格式
- **Surge配置**：Surge代理工具配置
- **SingBox配置**：新一代代理工具配置

#### 8. `collectSub.py` - 订阅链接收集器
**功能概述：** 从多个来源收集和整合代理订阅链接

**收集来源：**
- **免费机场**：公开的免费机场订阅链接
- **Telegram频道**：Telegram上的代理分享频道
- **GitHub项目**：开源的代理节点项目
- **公开代理池**：各种公开的代理服务
- **用户贡献**：社区用户贡献的链接

**处理流程：**
1. **并发获取**：多线程并发获取订阅内容
2. **格式解析**：解析和标准化节点信息
3. **质量验证**：验证节点的连通性和速度
4. **智能去重**：基于多维度的去重算法
5. **分类整理**：按地区、协议、质量等分类
6. **格式输出**：生成统一格式的输出文件

#### 9. `hy2.py` - Hysteria2协议处理器
**功能概述：** 专门处理Hysteria2协议的解析、验证和转换

**主要功能：**
- **链接解析**：解析Hysteria2协议的分享链接
- **参数验证**：验证协议参数的正确性和完整性
- **协议转换**：转换为其他代理工具支持的格式
- **性能优化**：针对Hysteria2的性能优化配置

**特性支持：**
- **UDP加速**：利用UDP协议的高速传输特性
- **多路复用**：支持连接复用，提高效率
- **拥塞控制**：智能的网络拥塞控制算法
- **自适应码率**：根据网络状况自动调整传输速率

#### 10. `ji_github_sync.py` - GitHub同步工具
**功能概述：** 实现与GitHub仓库的数据同步和版本控制

**同步功能：**
- **双向同步**：支持本地到远程和远程到本地的双向同步
- **增量更新**：只同步变更的文件，提高效率
- **冲突解决**：智能的文件冲突检测和解决
- **版本管理**：完整的版本历史和回滚支持

#### 11. `jichang_list.py` - 机场信息管理器
**功能概述：** 维护机场数据库和信息管理系统

**数据管理：**
- **基础信息**：机场名称、URL、描述等基本信息
- **状态跟踪**：注册状态、可用性、最后检查时间
- **历史记录**：完整的可用性历史记录和统计
- **质量评分**：基于多维度的质量评分系统

**信息字段：**
- **机场标识**：唯一标识符和别名
- **访问信息**：URL、备用地址、访问方式
- **面板类型**：自动识别的面板类型和版本
- **注册要求**：注册难度、验证要求、限制条件
- **服务信息**：试用期限、流量限制、节点质量
- **更新记录**：最后更新时间、检查频率、变更历史

#### 12. `apis.py` - API接口服务模块
**功能概述：** 提供RESTful API接口，支持外部系统集成

**API端点详解：**
- `/api/subscriptions` - 订阅管理（增删改查订阅链接）
- `/api/nodes` - 节点查询（按地区、协议、质量查询）
- `/api/convert` - 格式转换（多种配置格式互转）
- `/api/health` - 健康检查（系统状态和服务可用性）
- `/api/stats` - 统计信息（使用统计、性能指标）
- `/api/airports` - 机场管理（机场信息的CRUD操作）
- `/api/test` - 节点测试（批量节点连通性测试）

**功能特性：**
- **JWT认证**：基于JSON Web Token的身份验证
- **限流控制**：API请求频率限制和配额管理
- **缓存机制**：智能的响应缓存，提高性能
- **错误处理**：统一的错误处理和详细的错误信息
- **文档生成**：自动生成API文档和使用示例
- **版本管理**：API版本控制和向后兼容

#### 13. `utils.py` - 通用工具库
**功能概述：** 提供项目中常用的工具函数和辅助方法

**工具分类详解：**
- **网络工具**：HTTP请求、代理支持、重试机制
- **数据解析**：JSON、YAML、Base64、URL解析
- **文件操作**：读写、压缩、加密、备份
- **加密工具**：哈希、对称加密、数字签名
- **日志系统**：结构化日志、日志轮转、远程日志
- **配置管理**：配置文件解析、环境变量、动态配置

**核心函数详解：**
- `fetch_url()` - 增强的网络请求封装，支持重试、代理、超时
- `parse_proxy()` - 智能代理链接解析，支持多种协议格式
- `encode_base64()` - Base64编码处理，支持URL安全编码
- `validate_config()` - 配置文件验证，支持JSON Schema
- `setup_logger()` - 日志系统配置，支持多种输出格式
- `cache_result()` - 结果缓存装饰器，支持TTL和LRU策略

#### 14. `vt.py` - GitHub IPTV资源发现器
**功能概述：** 使用GitHub API搜索和发现IPTV资源的专业工具

**核心功能：**
- **GitHub API集成**：完整的GitHub代码搜索API集成
- **搜索策略优化**：基于关键词和文件类型的智能搜索
- **自动提取验证**：自动提取URL并进行有效性验证
- **多协议支持**：支持HTTP、RTMP、RTP、P3P等多种协议
- **格式转换**：智能的文件格式转换（m3u到txt等）
- **数据合并去重**：高效的IPTV文件合并和去重算法

**搜索策略详解：**
- `extension:m3u8 in:file` - 专门搜索M3U8播放列表文件
- `extension:m3u in:file` - 搜索M3U格式的播放列表
- `iptv playlist` - 通用IPTV播放列表关键词搜索
- `raw.githubusercontent.com` - 专门搜索GitHub原始文件
- `tv channels` - 电视频道相关资源搜索
- `live stream` - 直播流资源搜索

**GitHub API配置：**
- **认证支持**：支持GitHub Token认证，提高API限额
- **分页机制**：智能的分页搜索，最多处理5页结果
- **结果限制**：每页最多100个结果，避免API滥用
- **重试机制**：智能重试和错误处理，应对API限制
- **缓存优化**：搜索结果缓存，减少重复请求

#### 15. `urls.py` - URL有效性批量检测器
**功能概述：** 简单高效的URL批量检测工具

**主要功能：**
- **批量读取**：从trial.cfg文件批量读取URL列表
- **并发检测**：多线程并发检测（默认8线程，可配置）
- **状态验证**：HTTP状态码验证和响应时间测量
- **智能过滤**：自动过滤无效链接和异常响应
- **格式支持**：支持注释行和空行的智能跳过

**使用场景：**
- **机场验证**：批量验证机场URL的可访问性
- **订阅检测**：检测订阅链接的有效性和响应速度
- **健康检查**：定期的批量URL健康检查
- **质量评估**：基于响应时间的质量评估

### subscribe/ 目录专业模块

#### 1. `subscribe/collect.py` - 企业级订阅收集系统
**功能概述：** 订阅收集系统的核心模块，提供企业级的收集和管理功能

**环境变量依赖：**
- `ALL_CLASH_DATA_API` - GitHub仓库API地址，用于数据同步
- `GIST_PAT` - GitHub Personal Access Token，用于API认证

**高级特性：**
- **分布式架构**：支持分布式收集和负载均衡
- **智能重试**：多层次的重试机制和错误恢复
- **数据持久化**：支持多种数据存储后端
- **API集成**：完整的RESTful API接口
- **监控告警**：实时监控和告警系统
- **GitHub集成**：深度集成GitHub仓库管理

**命令行参数详解：**
- `-a, --all` - 生成完整配置，包含所有收集到的节点
- `-c, --chuck` - 丢弃需要人工验证的候选网站，提高自动化程度
- `-e, --easygoing` - 使用Gmail别名处理邮箱白名单，绕过邮箱限制
- `-f, --flow` - 按可用剩余流量过滤订阅（单位：GB）
- `-i, --invisible` - 隐藏检测进度条，适用于后台运行
- `-n, --num` - 处理线程数（默认64，可根据系统性能调整）
- `-o, --overwrite` - 覆盖已存在的域名信息，强制更新
- `-p, --pages` - Telegram爬取最大页数，控制爬取深度
- `-r, --refresh` - 仅刷新现有订阅，不添加新的
- `-t, --targets` - 选择生成的配置类型（clash/v2ray/base64）
- `-v, --vitiate` - 忽略默认代理过滤规则，保留所有节点

**数据处理流程：**
1. **配置加载**：从环境变量和配置文件加载参数
2. **源发现**：自动发现和验证数据源
3. **并发收集**：多线程并发收集订阅数据
4. **质量过滤**：基于多维度的质量过滤
5. **数据清洗**：去重、格式化、标准化
6. **配置生成**：生成多种格式的配置文件
7. **结果推送**：推送到GitHub或其他存储后端

#### 2. `subscribe/ss.py` - Shadowsocks节点专业收集器
**功能概述：** 专门收集和处理Shadowsocks协议节点的高效工具

**环境变量配置：**
- `SOURCE_URLS` - 源URL列表（逗号分隔），支持多个数据源

**处理流程详解：**

**阶段1：节点收集**
- **源解析**：从环境变量读取和解析源URL列表
- **并发获取**：使用线程池并发获取订阅内容
- **数据收集**：收集所有原始节点数据到内存
- **临时存储**：保存到临时文件`data/ss_temp_all_nodes.txt`

**阶段2：去重处理**
- **数据读取**：从临时文件读取所有节点数据
- **关键信息提取**：提取节点的关键标识信息
- **去重算法**：基于Set数据结构的高效去重
- **结果输出**：生成最终的唯一节点列表
- **清理工作**：删除临时文件，释放存储空间

**性能优化策略：**
- **CPU感知**：自动检测CPU核心数，优化线程配置
- **动态调整**：动态调整并发线程数（最多32线程）
- **超时控制**：智能超时控制（30秒），避免长时间等待
- **内存优化**：流式处理，减少内存占用
- **错误处理**：完善的错误处理和日志记录

**去重算法详解：**
- **信息提取**：提取服务器地址、端口、密码、加密方式等关键信息
- **标识生成**：生成节点的唯一标识符
- **快速去重**：基于哈希表的O(1)去重操作
- **格式保持**：保持节点原始格式不变

#### 3. `subscribe/all_clash.py` - Clash节点聚合器
**功能概述：** 专门收集和聚合Clash格式节点的专业工具

**环境变量配置：**
- `URL_SOURCE` - 单一源URL地址，支持动态URL

**命令行参数：**
- `--max_success` - 目标成功数量（默认99999），控制收集规模
- `--timeout` - 请求超时时间（默认60秒），适应网络环境
- `--output` - 输出文件路径（默认data/all_clash.txt），支持自定义

**处理特性：**
- **URL验证**：严格的URL格式验证和过滤
- **并发处理**：16线程并发处理，平衡效率和资源
- **进度显示**：使用tqdm库提供美观的进度条
- **错误记录**：详细的错误日志和统计信息
- **目录管理**：自动创建输出目录结构

**质量控制机制：**
- **格式验证**：验证URL格式的正确性
- **连通性测试**：测试URL的可访问性
- **内容验证**：验证返回内容的有效性
- **成功率统计**：实时统计成功率和失败原因
- **去重处理**：自动去除重复的URL

#### 4. `subscribe/convert_to_base64.py` - Base64转换器
**功能概述：** 将各种格式的代理配置转换为Base64编码格式

**转换功能：**
- **多格式输入**：支持Clash、V2Ray、SS等多种输入格式
- **标准化输出**：生成标准的Base64编码订阅链接
- **批量处理**：支持批量文件转换
- **格式验证**：转换前后的格式验证

#### 5. 其他subscribe/目录核心模块

**基础模块：**
- `subscribe/__init__.py` - 模块初始化，定义包结构和导入路径
- `subscribe/airport.py` - 机场对象模型，定义机场的数据结构和方法
- `subscribe/api.py` - API接口定义，提供统一的接口规范
- `subscribe/cache.py` - 缓存管理系统，提供多级缓存支持

**数据处理模块：**
- `subscribe/all.py` - 全量数据处理，处理大规模数据集
- `subscribe/clash.py` - Clash配置专用处理器
- `subscribe/origin.py` - 原始数据处理和标准化
- `subscribe/process.py` - 数据处理流程管理
- `subscribe/filter_nodes.py` - 高级节点过滤器

**网络和爬虫模块：**
- `subscribe/crawl.py` - 网页爬虫功能，支持多种爬取策略
- `subscribe/mailtm.py` - 临时邮箱服务集成
- `subscribe/urlvalidator.py` - URL验证器，支持多种验证规则
- `subscribe/transporter.py` - 数据传输器，支持多种传输协议

**工具和辅助模块：**
- `subscribe/executable.py` - 可执行文件管理和调用
- `subscribe/location.py` - 地理位置处理和IP定位
- `subscribe/logger.py` - 专业日志记录器
- `subscribe/esc.py` - 转义字符处理工具
- `subscribe/replace.py` - 内容替换和模板处理
- `subscribe/utils.py` - 订阅模块专用工具函数

**业务逻辑模块：**
- `subscribe/push.py` - 数据推送功能，支持多种推送目标
- `subscribe/renewal.py` - 续期管理，自动处理订阅续期
- `subscribe/subconverter.py` - 订阅转换器核心逻辑
- `subscribe/workflow.py` - 工作流管理，协调各模块协作

### tools/ 目录专业工具

#### 1. `tools/auto-checkin.py` - 自动签到系统
**功能概述：** 全自动机场签到获取流量的专业工具

**核心功能：**
- **多面板兼容**：支持V2Board、SSPanel、Sspanel-Uim等主流面板
- **智能登录**：自动登录状态检测和维护
- **流量统计**：自动获取和统计签到流量
- **批量处理**：支持多账号批量自动签到
- **结果记录**：详细的签到结果日志和统计

**配置系统：**
- **JSON配置**：使用JSON格式的配置文件
- **加密存储**：账号密码的安全加密存储
- **代理支持**：支持HTTP/SOCKS5代理服务器
- **自定义请求头**：支持自定义User-Agent和其他请求头
- **重试配置**：可配置的重试次数和间隔

**安全特性：**
- **随机延时**：随机延时机制，避免被检测为机器人
- **User-Agent轮换**：多种真实浏览器User-Agent轮换
- **Cookie管理**：智能的Cookie自动管理和持久化
- **登录验证**：多层次的登录状态验证
- **错误恢复**：智能的错误处理和自动恢复机制

**签到流程：**
1. **配置加载**：加载账号配置和签到参数
2. **登录检测**：检查当前登录状态
3. **自动登录**：如需要则自动执行登录流程
4. **签到执行**：执行签到操作并获取结果
5. **流量统计**：统计签到获得的流量
6. **状态更新**：更新账号状态和签到记录
7. **结果保存**：保存签到结果和统计信息

#### 2. `tools/filter.py` - 高级节点过滤器
**功能概述：** 基于Clash API的高级节点过滤和质量检测工具

**主要功能：**
- **配置解析**：智能解析Clash配置文件结构
- **提供商管理**：代理提供商的分类管理和批量操作
- **健康检查**：全面的节点健康状态检测
- **延迟测试**：精确的节点延迟测试和排序
- **配置备份**：自动配置文件备份和恢复
- **热重载**：支持Clash配置的热重载

**命令行参数详解：**
- `-a, --all` - 检查所有代理提供商，进行全面检测
- `-b, --backup` - 备份旧的提供商文件，防止数据丢失
- `-c, --config` - 指定Clash配置文件名，支持自定义配置
- `-d, --delay` - 设置最大可接受延迟（默认600ms）
- `-i, --iteration` - 健康检查迭代次数（1-10次，提高准确性）
- `-p, --provider` - 指定要检查的特定提供商
- `-w, --workspace` - 设置工作空间绝对路径

**技术特性：**
- **SSL跳过**：跳过SSL证书验证，适应各种环境
- **多进程并行**：利用多进程提高检测效率
- **内存监控**：使用psutil监控内存使用情况
- **YAML解析**：专业的YAML配置文件解析
- **HTTP API**：与Clash核心的HTTP API交互

**过滤算法：**
- **延迟过滤**：基于延迟阈值的节点过滤
- **可用性检测**：检测节点的实际可用性
- **稳定性评估**：多次测试评估节点稳定性
- **质量评分**：综合多个指标的质量评分

#### 3. `tools/scaner.py` - 机场扫描系统
**功能概述：** 全自动机场扫描、注册和节点提取的专业工具

**核心功能：**
- **自动注册**：全自动的机场账号注册流程
- **节点提取**：智能的节点信息提取和解析
- **多协议支持**：支持VMess、SSR、SS、Trojan等协议
- **Telegram集成**：自动爬取Telegram频道的机场信息
- **批量处理**：支持批量域名和机场的处理
- **配置重载**：支持Clash配置的自动重载

**扫描流程详解：**
1. **域名验证**：检查域名的有效性和可访问性
2. **面板识别**：自动识别机场使用的面板类型
3. **注册流程**：模拟真实用户的注册流程
4. **邮箱验证**：自动处理邮箱验证环节
5. **登录获取**：登录账号并获取订阅链接
6. **节点解析**：解析订阅内容，提取节点信息
7. **格式转换**：转换为指定的配置格式
8. **结果保存**：保存扫描结果和节点信息

**命令行参数详解：**
- `-r, --reload` - 重载Clash配置，应用新的节点
- `-s, --skip` - 跳过注册步骤，直接使用现有账号
- `-b, --batch` - 批量处理模式，处理多个目标
- `-k, --keep` - 保存节点列表信息，便于后续使用
- `-a, --address` - 指定机场域名地址
- `-e, --email` - 指定用户名或邮箱
- `-p, --passwd` - 指定登录密码
- `-t, --type` - 指定节点类型（vmess/ssr/all）
- `-f, --file` - 指定订阅文件保存路径
- `-u, --url` - 指定Clash控制器API地址
- `-d, --path` - 指定结果保存目录
- `-c, --config` - 指定Clash配置文件路径

**高级特性：**
- **多进程扫描**：利用多进程提高扫描效率
- **智能域名提取**：从各种源自动提取机场域名
- **Telegram爬虫**：自动爬取Telegram频道的最新信息
- **配置验证**：验证生成的配置文件的正确性
- **错误恢复**：智能的错误检测和恢复机制

**安全和反检测：**
- **真实浏览器模拟**：模拟真实浏览器的行为模式
- **随机化处理**：随机化请求间隔和行为模式
- **代理轮换**：支持代理服务器轮换
- **会话管理**：智能的会话状态管理

#### 4. 其他tools/目录专业工具

**系统维护工具：**
- `tools/clean.py` - 系统清理工具，清理临时文件和缓存
- `tools/renewal.py` - 续期管理工具，自动处理订阅和账号续期

**网络和定位工具：**
- `tools/ip-location.py` - IP地理位置查询，支持多种IP定位服务
- `tools/purefast.py` - 纯净快速节点筛选，基于多维度质量评估

**数据传输工具：**
- `tools/transporter.py` - 数据传输工具，支持多种传输协议和目标

**面板管理工具：**
- `tools/xui.py` - X-UI面板管理，支持X-UI面板的自动化操作

# cloxy.io.yaml 生成流程说明

## 1. 节点数据抓取与处理
- 脚本会从机场订阅链接、API 或本地文件抓取原始节点数据。
- 支持多种协议，自动解析为 Clash 支持的格式。
- 对节点进行去重、清洗（如去除无效、重复、格式错误的节点）。

## 2. 节点分组自动生成
- 根据模板和实际节点，自动生成 proxy-groups。
- 每个分组（如“低延迟”、“AI”、“B站”）自动引用对应的节点集合。
- 支持分组嵌套、分组别名（如 &id001, *id001）。

## 3. 规则集自动合并
- 脚本会自动拉取本地/远程规则集（如广告屏蔽、分流、直连等）。
- 支持自定义规则，自动合并去重。
- 规则与分组自动关联（如广告走“💩 广告”分组）。

## 4. YAML 文件生成与校验
- 所有配置项（基础配置、分组、节点、规则）拼接为完整 YAML。
- 自动格式化，保证 YAML 合法性。
- 生成文件保存到指定路径（如 `trials/https_/cloxy.io.yaml`）。

## 5. 自动化与定时更新
- 支持通过定时任务、GitHub Actions 自动更新节点和规则。
- 可配置机场订阅、规则模板、输出格式等参数。

## 6. 主要相关脚本
- `subscribe/collect.py`：主聚合与生成逻辑。
- `subscribe/replace.py`：节点格式转换与清洗。
- `subconverter.py`：模板渲染与最终输出。

# .github/workflows/ 目录下各 workflow 文件详细功能说明

本项目的 `.github/workflows/` 目录包含多个 GitHub Actions workflow 文件，每个文件实现不同的自动化功能，具体说明如下：

- **auto_update.yml**  
  功能：定时或手动触发，自动拉取机场订阅、聚合节点、清洗并生成 Clash 配置文件，最后自动提交并推送到仓库。  
  作用：保证节点和配置文件的持续更新，无需人工干预，确保订阅内容始终为最新。

- **subconverter.yml**  
  功能：定时或手动触发，调用 subconverter 脚本，将聚合后的节点数据转换为多种订阅格式（如 Clash、Surge、QuantumultX 等），并输出到指定目录，自动推送更新。  
  作用：为不同客户端自动生成兼容的订阅文件，方便多端使用，提升订阅适配性。

- **check.yml**  
  功能：定时或每次推送时触发，自动检测所有节点的可用性，筛除失效节点，仅保留可用节点，更新配置文件并推送。  
  作用：提升节点订阅的可用性和质量，确保用户获取到的都是可用节点。

- **clean.yml**  
  功能：定期自动清理无用文件、临时文件或日志，保持仓库整洁。可扩展为自动归档、备份等辅助功能。  
  作用：防止仓库膨胀，便于维护和管理，减少无关文件对主流程的影响。

- **backup.yml**  
  功能：定时备份关键配置文件和节点数据，防止意外丢失。可将备份上传到指定分支或外部存储。  
  作用：保障数据安全，便于灾难恢复和历史追溯。

- **log_archive.yml**  
  功能：定期归档 workflow 运行日志，便于后续排查和分析历史任务执行情况。  
  作用：方便问题定位和追踪，提升运维效率。

> 说明：实际 workflow 文件名和功能以 `.github/workflows/` 目录下为准，部分功能可根据项目需求增删。

# GitHub Actions Workflow 流程与功能说明

本项目包含多个 GitHub Actions workflow，自动化实现节点聚合、配置生成、定时更新等功能。主要流程和作用如下：

## 1. 自动聚合与配置生成（如 auto_update.yml）

- **触发方式**：定时（如每6小时）、手动触发（workflow_dispatch）。
- **主要步骤**：
  1. **Checkout 代码**：拉取仓库最新代码。
  2. **安装依赖**：自动安装 Python 依赖（如 `pip install -r requirements.txt`）。
  3. **运行聚合脚本**：执行 `subscribe/collect.py` 等脚本，自动抓取、聚合、清洗节点，生成 Clash 配置文件。
  4. **生成/更新配置**：输出如 `trials/https_/cloxy.io.yaml` 等 YAML 文件。
  5. **自动提交并推送**：如有变更，自动 commit 并推送到仓库。

## 2. 订阅转换与多格式输出（如 subconverter.yml）

- **触发方式**：定时或手动。
- **主要步骤**：
  1. **拉取代码与依赖**。
  2. **运行 subconverter 脚本**：将聚合后的节点转换为多种订阅格式（如 Clash、Surge、QuantumultX 等）。
  3. **输出多格式订阅文件**。
  4. **自动推送更新**。

- **作用**：为不同客户端自动生成兼容的订阅文件，方便多端使用。

## 3. 健康检查与可用性检测（如 check.yml）

- **触发方式**：定时或每次推送。
- **主要步骤**：
  1. **运行节点可用性检测脚本**。
  2. **筛选掉失效节点，保留可用节点**。
  3. **更新配置文件并推送**。

- **作用**：保证聚合输出的节点均为可用，提高订阅质量。

## 4. 自动清理与日志归档（如 clean.yml、log_archive.yml）

- **触发方式**：定时。
- **主要步骤**：
  1. **自动清理无用文件、临时文件或日志**。
  2. **归档 workflow 运行日志，便于后续排查和分析**。

- **作用**：保持仓库整洁，便于维护和问题追踪。

## 5. 定期备份（如 backup.yml）

- **触发方式**：定时。
- **主要步骤**：
  1. **备份关键配置文件和节点数据**。
  2. **上传备份到指定分支或外部存储**。

- **作用**：防止数据丢失，便于恢复历史配置。

---

## 典型 workflow 文件示例

```yaml
name: Auto Update

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run aggregator
        run: python subscribe/collect.py

      - name: Commit and push changes
        run: |
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git config --global user.name "github-actions[bot]"
          git add .
          git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
          git push
```

---

## 总结

- 所有 workflow 文件位于 `.github/workflows/` 目录。
- 主要实现自动抓取、聚合、转换、检测、推送等自动化流程。
- 通过 GitHub Actions，无需人工干预即可保持节点和配置的最新与可用。

---

# 使用建议

如需自定义 workflow，可在 `.github/workflows/` 目录下新建或修改 YAML 文件，调整定时、脚本路径、推送策略等参数。

## 项目架构和工作流程

### 整体架构
```
jichangnodes/
├── 核心获取模块 (get_trial.py, apis.py)
├── 配置生成模块 (ClashForge.py, subconverter.py)
├── 数据收集模块 (collectSub.py, hy2.py, jichang_list.py)
├── 订阅处理模块 (subscribe/)
├── 媒体处理模块 (main.py, vt.py)
├── 代理聚合模块 (TG_proxy_main.py)
├── 同步管理模块 (ji_github_sync.py, urls.py)
└── 工具支持模块 (utils.py)
```

### 典型工作流程

1. **数据收集阶段**
   - `jichang_list.py` 抓取机场链接
   - `hy2.py` 从 GitHub 搜索代理
   - `collectSub.py` 收集订阅链接

2. **试用获取阶段**
   - `get_trial.py` 自动注册和获取试用
   - `apis.py` 提供面板和邮箱 API 支持
   - `utils.py` 提供工具函数支持

3. **配置生成阶段**
   - `ClashForge.py` 生成 Clash 配置
   - `subconverter.py` 进行高级转换
   - `subscribe/convert_to_base64.py` 生成 Base64 格式

4. **链接管理阶段**
   - `get_trial_update_url.py` 生成短链接
   - `ji_github_sync.py` 同步到 GitHub

5. **质量保证阶段**
   - `urls.py` 验证链接可用性
   - 各模块内置的连通性测试

## 配置文件说明

### 主要配置文件
- `trial.cfg`：试用机场配置列表
- `subconverters.cfg`：订阅转换器配置
- `config.yaml`：主配置文件
- `trial.cache`：试用缓存文件

### 环境变量
项目大量使用环境变量进行配置，主要包括：
- `GITHUB_REPOSITORY`：GitHub 仓库信息
- `GITHUB_TOKEN`：GitHub API 令牌
- `DDAL_EMAIL` / `DDAL_PASSWORD`：短链接服务凭据
- `ALL_CLASH_DATA_API`：Clash 数据 API
- `GIST_PAT`：GitHub Personal Access Token

## 使用建议

### 新手使用
1. 首先运行 `get_trial.py` 获取基础试用节点
2. 使用 `ClashForge.py` 生成 Clash 配置
3. 通过 `get_trial_update_url.py` 生成分享链接

### 高级使用
1. 配置完整的环境变量
2. 使用 `subscribe/collect.py` 进行企业级收集
3. 结合 GitHub Actions 实现自动化

### 性能优化
- 合理设置并发线程数
- 使用缓存机制避免重复操作
- 定期清理临时文件

## 注意事项

1. **合规使用**：请确保在合法合规的前提下使用本项目
2. **频率控制**：避免过于频繁的请求，以免被目标服务器封禁
3. **数据安全**：妥善保管 API 密钥和敏感信息
4. **资源管理**：注意内存和磁盘空间的使用
5. **错误处理**：关注日志输出，及时处理错误

## 总结

`jichangnodes` 项目是一个功能完整、架构清晰的代理节点管理系统。通过模块化的设计，项目实现了从数据收集、试用获取、配置生成到链接管理的完整流程。每个 Python 脚本都有明确的职责和功能，相互配合形成了一个高效的自动化系统。

项目的核心优势在于：
- **自动化程度高**：最大程度减少人工干预
- **扩展性强**：模块化设计便于功能扩展
- **稳定性好**：完善的错误处理和重试机制
- **效率高**：多线程并发处理提升性能
- **兼容性强**：支持多种协议和格式

无论是个人使用还是企业部署，该项目都能提供可靠的代理节点管理解决方案。

## GitHub Actions 环境配置详细指南

### 概述

本项目使用 GitHub Actions 实现完全自动化的代理节点收集、处理和分发流程。为确保工作流正常运行，需要正确配置相应的 Secrets 和 Variables。

### 必需的 Secrets 配置

#### 核心认证 Secrets

##### 1. GIST_PAT (GitHub Personal Access Token)
- **功能作用**：GitHub 个人访问令牌，用于访问 GitHub API 和 Gist 服务
- **使用场景**：节点数据存储、配置文件更新、仓库操作
- **权限要求**：`repo`（完整仓库访问）、`gist`（Gist 访问）、`workflow`（工作流权限）
- **获取方式**：
  1. 进入 GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
  2. 点击 "Generate new token (classic)"
  3. 选择所需权限范围
  4. 生成并复制令牌（仅显示一次）
- **配置示例**：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **使用工作流**：Collect.yml, get_trial.yml

##### 2. GT_TOKEN (GitHub Token)
- **功能作用**：GitHub 访问令牌，主要用于 Telegram 订阅相关操作
- **使用场景**：仓库文件读写、配置更新、数据同步
- **权限要求**：与 GIST_PAT 相同，可以使用同一个令牌
- **配置示例**：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **使用工作流**：Telegram Subscriptions.yml

#### 数据源配置 Secrets

##### 3. CLASH_API
- **功能作用**：Clash 配置数据源 API 地址
- **使用场景**：获取外部 Clash 配置模板和规则集
- **配置要求**：完整的 HTTP/HTTPS URL，支持直接访问
- **配置示例**：`https://api.example.com/clash/config`
- **使用工作流**：Collect.yml
- **注意事项**：确保 API 地址可访问且返回有效的 Clash 配置数据

##### 4. SOURCE_URLS
- **功能作用**：SS 节点源 URL 列表
- **使用场景**：批量获取 Shadowsocks 节点信息
- **配置格式**：每行一个 URL，支持多个数据源
- **配置示例**：
  ```
  https://example1.com/ss-nodes
  https://example2.com/proxy-list
  https://example3.com/free-nodes
  ```
- **使用工作流**：ss.yml
- **功能特点**：支持并发处理多个数据源，自动去重和验证

#### 通信服务 Secrets

##### 5. BOT (Telegram Bot Token)
- **功能作用**：Telegram 机器人令牌，用于频道监控和消息处理
- **使用场景**：监控 Telegram 频道、获取订阅链接、发送通知
- **获取方式**：
  1. 在 Telegram 中搜索 @BotFather
  2. 发送 `/newbot` 命令
  3. 按提示设置机器人名称和用户名
  4. 获得 Bot Token
- **配置示例**：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
- **使用工作流**：Conversion.yml

### 工作流详细说明和配置

#### 1. Auto_proxy.yml - 自动代理任务
- **触发方式**：手动触发 + 每8小时自动运行
- **核心功能**：
  - 执行 `TG_proxy_main.py` 脚本
  - 处理大规模代理节点收集（700+ 机场支持）
  - 生成多格式配置文件（Clash 和 V2Ray）
  - Base64 编解码处理
- **依赖文件**：`TG_proxy_main.py`, `requirements2.txt`
- **输出结果**：聚合的代理配置文件
- **特点**：海量机场支持，高效并发处理

#### 2. Collect.yml - 订阅数据收集
- **触发方式**：手动触发 + 每3小时自动运行
- **核心功能**：
  - 运行 `subscribe/collect.py` 企业级收集器
  - 聚合多源订阅数据
  - 生成标准化配置文件
  - 支持命令行参数配置
- **所需 Secrets**：`CLASH_API`, `GIST_PAT`
- **处理流程**：
  1. 从配置的 API 获取数据
  2. 解析和验证节点信息
  3. 生成 Clash 配置文件
  4. 上传到 Gist 服务
- **高级特性**：模块化设计、GitHub 集成、日志系统

#### 3. Conversion.yml - Base64 转换
- **触发方式**：手动触发 + 每8小时自动运行
- **核心功能**：
  - Base64 格式转换
  - 节点连通性测试
  - 多格式输出支持
  - 代理指纹生成和去重
- **所需配置**：`BOT`, `URL_LIST_REPO_API`
- **环境变量**：
  - `TIMEOUT_SECONDS=10`：连接超时时间
  - `MAX_RETRIES=3`：最大重试次数
  - `CONCURRENT_LIMIT=50`：并发连接限制
- **支持协议**：VMess, Trojan, Shadowsocks, Hysteria2

#### 4. Telegram Subscriptions.yml - Telegram 频道监控
- **触发方式**：手动触发 + 每8小时自动运行
- **核心功能**：
  - 监控指定 Telegram 频道
  - 提取订阅链接
  - 验证链接有效性
  - 保存到指定仓库
- **所需 Secrets**：`GT_TOKEN`, `SUBSCRIPTION_TARGET_REPO`, `SUBSCRIPTION_SAVE_PATH`, `CONFIG_REPO_NAME`, `CONFIG_FILE_PATH`, `SEARCH_KEYWORDS_ENV`
- **智能特性**：关键词匹配、自动过滤、数据持久化

#### 5. get_trial.yml - 试用节点获取
- **触发方式**：手动触发 + 每3小时自动运行
- **核心功能**：
  - 自动注册机场试用账户
  - 获取试用订阅链接
  - 生成配置文件和短链接
  - 临时邮箱集成
- **所需 Secrets**：`DDAL_EMAIL`, `DDAL_PASSWORD`
- **权限要求**：write-all（用于文件提交）
- **高级特性**：多线程并发、智能注册、缓存机制

#### 6. Node Tester.yml - 节点测试
- **触发方式**：手动触发 + 每小时自动运行
- **核心功能**：
  - 测试节点连通性
  - 评估节点质量
  - 过滤无效节点
  - 性能基准测试
- **依赖文件**：`package.json`, `test_nodes.js`
- **运行环境**：Node.js
- **测试指标**：延迟、稳定性、可用性

#### 7. jichang_list.yml - 机场列表更新
- **触发方式**：手动触发 + 每天凌晨3点运行
- **核心功能**：
  - 更新机场列表
  - 验证机场可用性
  - 更新 `trial.cfg` 配置
  - 多源抓取（Telegram 频道、网页）
- **输出文件**：`trial.cfg`
- **特性**：HTML 解析、并发处理、连通性测试

#### 8. ss.yml - SS 节点收集
- **触发方式**：手动触发 + 每3小时自动运行 + 推送触发
- **核心功能**：
  - 从多个源收集 SS 节点
  - 节点去重和验证
  - 自动提交更新
  - 并发处理优化
- **所需 Secrets**：`ACTIONS_DEPLOY_KEY`, `SOURCE_URLS`
- **权限要求**：contents: write
- **处理特点**：两阶段处理、智能去重、进度监控

#### 9. clashforge.yml - Clash 配置生成
- **触发方式**：仅手动触发
- **核心功能**：
  - 运行 `ClashForge.py` 脚本
  - 生成标准 Clash 配置
  - 节点解析和去重
  - 模板系统支持
- **依赖文件**：`requirements.txt`, `ClashForge.py`
- **支持协议**：Hysteria2, SS, Trojan, Vless, Vmess

### 配置优先级和建议

#### 最小配置（新手推荐）
适合初次使用，可运行基础功能：
```
✅ GITHUB_TOKEN (自动提供)
✅ GIST_PAT = 你的GitHub个人访问令牌
✅ GT_TOKEN = 同上（可复用）
```
**可运行工作流**：clashforge.yml, jichang_list.yml

#### 基础功能配置
支持大部分核心功能：
```
✅ 最小配置 +
✅ CLASH_API = Clash配置API地址
✅ URL_LIST_REPO_API = GitHub API地址
```
**可运行工作流**：Collect.yml, Conversion.yml

#### 完整功能配置
支持所有高级功能：
```
✅ 基础配置 +
✅ BOT = Telegram机器人令牌
✅ ACTIONS_DEPLOY_KEY = SSH私钥
✅ SOURCE_URLS = SS节点源列表
✅ DDAL_EMAIL & DDAL_PASSWORD = 短链接服务凭据
✅ Telegram订阅相关的6个Secrets
```
**可运行工作流**：全部工作流

### 安全最佳实践

#### 1. 敏感信息保护
- **原则**：所有敏感信息必须设置为 Secrets，禁止硬编码
- **范围**：API 密钥、密码、令牌、私钥
- **验证**：定期检查代码中是否有泄露的敏感信息
- **工具**：使用 git-secrets 等工具扫描敏感信息

#### 2. 权限最小化
- **GitHub PAT**：只授予必需的最小权限
- **SSH 密钥**：使用专用密钥，避免复用个人密钥
- **工作流权限**：根据实际需要设置权限范围
- **定期审查**：定期检查和调整权限设置

#### 3. 定期维护
- **令牌轮换**：定期更新和轮换 API 密钥（建议3-6个月）
- **权限审查**：每月检查权限设置
- **日志监控**：监控工作流运行情况和异常
- **安全扫描**：定期进行安全漏洞扫描

#### 4. 备份和恢复
- **密钥备份**：安全保存重要密钥的备份
- **配置文档**：维护详细的配置文档
- **恢复流程**：制定密钥丢失的恢复流程
- **测试恢复**：定期测试备份恢复流程

### 故障排除指南

#### 常见错误类型

##### 1. Secret not found
- **错误信息**：`Error: Secret XXXX not found`
- **原因**：Secret 名称拼写错误或未设置
- **解决方案**：
  1. 检查 Secret 名称拼写
  2. 确认已在仓库设置中正确添加
  3. 验证 Secret 值不为空
- **验证方法**：在工作流中添加调试输出（注意不要泄露敏感信息）

##### 2. Permission denied
- **错误信息**：`Error: Permission denied` 或 `403 Forbidden`
- **原因**：GitHub PAT 权限不足
- **解决方案**：
  1. 检查 PAT 权限范围
  2. 重新生成具有足够权限的令牌
  3. 确认令牌未过期
- **验证方法**：
  ```bash
  curl -H "Authorization: token YOUR_PAT" https://api.github.com/user
  ```

##### 3. SSH key error
- **错误信息**：`Permission denied (publickey)`
- **原因**：SSH 密钥配置错误或权限不足
- **解决方案**：
  1. 重新生成密钥对
  2. 确保正确配置 Deploy key
  3. 检查私钥格式完整性
- **验证方法**：
  ```bash
  ssh -T git@github.com
  ```

##### 4. API rate limit
- **错误信息**：`API rate limit exceeded`
- **原因**：API 调用频率过高
- **解决方案**：
  1. 调整工作流运行频率
  2. 添加延迟机制
  3. 使用认证的 API 调用（更高限额）
- **预防措施**：合理设置定时任务间隔

#### 调试技巧

##### 1. 日志分析
- 查看 Actions 页面的详细运行日志
- 关注错误信息和堆栈跟踪
- 检查环境变量和 Secret 的使用情况
- 使用 `set -x` 启用详细调试输出

##### 2. 本地测试
```bash
# 测试 SSH 连接
ssh -T git@github.com

# 测试 GitHub API
curl -H "Authorization: token YOUR_PAT" https://api.github.com/user

# 测试 Clash API
curl -X GET "YOUR_CLASH_API_URL"

# 测试 Telegram Bot
curl "https://api.telegram.org/botYOUR_BOT_TOKEN/getMe"
```

##### 3. 分步验证
- 从最简单的工作流开始测试（如 clashforge.yml）
- 逐步添加复杂功能
- 每次只修改一个配置项
- 使用手动触发测试新配置

### 性能优化建议

#### 1. 并发控制
- **合理设置并发数**：根据服务器性能调整
- **避免资源竞争**：错开高负载工作流的运行时间
- **使用队列机制**：处理大量任务时使用队列
- **监控资源使用**：定期检查 CPU 和内存使用情况

#### 2. 缓存策略
- **GitHub Actions 缓存**：缓存依赖包和构建结果
- **数据缓存**：缓存频繁访问的数据
- **避免重复计算**：缓存计算结果
- **缓存失效策略**：设置合理的缓存过期时间

#### 3. 资源管理
- **监控运行时间**：优化长时间运行的任务
- **内存优化**：避免内存泄漏和过度使用
- **磁盘清理**：及时清理临时文件
- **网络优化**：减少不必要的网络请求

### 监控和维护

#### 1. 运行监控
- **状态监控**：定期检查工作流运行状态
- **失败通知**：设置失败通知机制
- **性能监控**：监控运行时间和资源使用
- **日志分析**：定期分析运行日志

#### 2. 数据质量
- **完整性检查**：验证输出数据的完整性
- **可用性测试**：检查节点的可用性
- **更新频率**：监控配置文件的更新频率
- **数据一致性**：确保不同格式数据的一致性

#### 3. 系统维护
- **依赖更新**：定期更新依赖包
- **安全补丁**：及时应用安全补丁
- **清理任务**：定期清理过期数据
- **备份策略**：实施定期备份策略

### 快速配置检查清单

#### Secrets 配置检查表
```
□ GIST_PAT = ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
□ GT_TOKEN = ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
□ CLASH_API = https://your-clash-api.com/config
□ BOT = 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
□ DDAL_EMAIL = your-email@example.com
□ DDAL_PASSWORD = your-secure-password
□ ACTIONS_DEPLOY_KEY = -----BEGIN OPENSSH PRIVATE KEY-----...
□ SOURCE_URLS = https://example1.com/ss-nodes\nhttps://example2.com/proxy-list
□ SUBSCRIPTION_TARGET_REPO = moneyfly1/jichangnodes
□ SUBSCRIPTION_SAVE_PATH = data/subscriptions.txt
□ CONFIG_REPO_NAME = moneyfly1/jichangnodes
□ CONFIG_FILE_PATH = config/telegram_config.json
□ SEARCH_KEYWORDS_ENV = 节点,代理,vpn,翻墙
```

#### Variables 配置检查表
```
□ URL_LIST_REPO_API = https://api.github.com/repos/moneyfly1/jichangnodes/contents/urls.txt
```

#### Deploy Keys 配置检查表
```
□ SSH 公钥已添加到仓库 Deploy keys
□ 已勾选 "Allow write access"
□ 私钥已正确设置为 ACTIONS_DEPLOY_KEY Secret
```

#### 工作流测试检查表
```
□ clashforge.yml 手动触发测试通过
□ Collect.yml 运行正常
□ get_trial.yml 试用获取功能正常
□ ss.yml SSH 部署功能正常
□ 所有定时任务按预期运行
```

## 项目总结

`jichangnodes` 是一个功能强大的代理节点聚合和管理平台，通过自动化的 GitHub Actions 工作流，实现了从节点收集、验证、转换到配置生成的完整流程。项目支持多种代理协议，集成了丰富的数据源，并提供了灵活的配置选项，是代理服务管理的理想解决方案。

### 核心优势
- **全自动化**：通过 GitHub Actions 实现完全自动化的节点收集和处理
- **多源聚合**：支持 700+ 机场和多种数据源
- **高可靠性**：内置节点验证、去重和质量检测机制
- **灵活配置**：支持多种输出格式和自定义配置
- **安全可靠**：采用最佳安全实践，保护敏感信息
- **易于维护**：模块化设计，便于扩展和维护

### 适用场景
- 个人代理节点管理
- 企业级代理服务部署
- 代理节点质量监控
- 多源数据聚合分析
- 自动化运维管理

通过合理配置和使用本项目，您可以轻松构建一个稳定、高效的代理节点管理系统。
## 感谢

感谢以下开源项目的贡献：
- https://github.com/awuaaaaa/vless-py
- https://github.com/wzdnzd/aggregator
- https://github.com/0xJins/x.sub
- https://github.com/w1770946466/Auto_proxy
- https://github.com/VPNforWindowsSub/base64
- https://github.com/mojolabs-id/GeoLite2-Database
- https://github.com/midpoint/ClashForge
- https://github.com/mlzlzj/df
