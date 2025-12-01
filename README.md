# 地下管廊环境检测系统

<img width="2874" height="1366" alt="index" src="https://github.com/user-attachments/assets/c4ef392f-e77d-419f-a36b-26bead72106b" />
<img width="2872" height="1372" alt="index_data" src="https://github.com/user-attachments/assets/9ecb663f-8c0d-4241-add9-3443329bdd0e" />
<img width="2872" height="1368" alt="chart" src="https://github.com/user-attachments/assets/085f03ef-6054-4237-a80a-4f29da2c66b7" />
<img width="2872" height="1370" alt="alert" src="https://github.com/user-attachments/assets/0f87eace-b141-4c8e-812a-4f6a7575f86c" />

## 项目概述

地下管廊环境检测系统是一个基于Django框架的物联网监控平台，用于实时监测地下管廊环境中的多种气体浓度（一氧化碳、硫化氢、甲烷、氨气）和液位高度，并提供远程设备控制功能。系统通过ESP32微控制器采集环境数据，Web界面提供可视化图表和警报管理。

## 技术栈

### 后端
- **Django 3.x/4.x** - Python Web框架
- **SQLite3** - 轻量级数据库
- **Django REST Framework** - 用于API接口
- **Python 3.x** - 主要开发语言

### 前端
- **HTML5/CSS3** - 页面结构
- **JavaScript** - 交互逻辑
- **Bootstrap 5** - 响应式UI框架
- **Chart.js** - 数据可视化图表
- **Font Awesome** - 图标库
- **Simple DataTables** - 表格组件

### 硬件/嵌入式
- **ESP32微控制器** - 数据采集核心
- **MQ系列气体传感器** - 气体浓度检测
- **水位传感器** - 液位检测
- **继电器模块** - 风扇控制
- **LED报警灯** - 视觉报警
- **蜂鸣器** - 声音报警

## 系统架构

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│   ESP32硬件端    │◄───────────────►│   Django服务器   │
│  - 传感器数据采集 │                │  - 数据存储      │
│  - 本地报警判断   │                │  - 用户管理      │
│  - 设备控制执行   │                │  - Web服务      │
└─────────────────┘                └─────────────────┘
                                            │
                                            │ HTTP/WebSocket
                                            ▼
                                  ┌─────────────────┐
                                  │   Web前端界面   │
                                  │  - 实时监控     │
                                  │  - 图表展示     │
                                  │  - 设备控制     │
                                  │  - 警报管理     │
                                  └─────────────────┘
```

## 主要功能模块

### 1. 环境监测模块
- **实时数据采集**: 一氧化碳、硫化氢、甲烷、氨气浓度及液位高度
- **阈值设置**: 可配置各参数的报警阈值
- **自动报警**: 数据超标时自动触发报警机制

### 2. 设备控制模块
- **远程风扇控制**: 通过Web界面开关管廊通风风扇
- **设备状态同步**: 实时同步设备开关状态

### 3. 数据可视化模块
- **实时图表**: 折线图、柱状图展示历史数据趋势
- **数据表格**: 详细展示采集的历史数据
- **仪表盘**: 各参数状态概览

### 4. 用户管理模块
- **用户注册/登录**: 支持多用户账户管理
- **个人信息维护**: 用户可修改个人信息
- **权限控制**: Cookie-based会话管理

### 5. 报警管理模块
- **报警记录**: 记录所有报警事件
- **实时通知**: Web界面实时显示报警信息
- **报警日志**: 查看历史报警记录

## 项目结构

```
underground-pipeline-monitoring/
├── manage.py              # Django管理脚本
├── db.sqlite3             # SQLite数据库文件
├── requirements.txt       # Python依赖包列表
├── urls.py               # 全局URL路由配置
├── views.py              # 视图函数处理逻辑
├── models.py             # 数据库模型定义
├── static/               # 静态资源文件
│   ├── css/              # 样式表
│   │   └── styles.css    # 主样式文件
│   └── js/               # JavaScript文件
│       ├── scripts.js    # 通用脚本
│       └── datatables-simple-demo.js # 表格脚本
├── templates/            # HTML模板文件
│   ├── index.html        # 主仪表盘页面
│   ├── charts.html       # 图表展示页面
│   ├── tables.html       # 报警数据页面
│   ├── fan.html          # 风扇控制页面
│   ├── login.html        # 登录页面
│   ├── register.html     # 注册页面
│   ├── userpages.html    # 用户信息页面
│   └── warn.html         # 报警页面（备用）
└── esp32.py              # ESP32固件代码
```

## 数据库模型

### SensorData（传感器数据表）
- `id`: 主键
- `co_concentration`: 一氧化碳浓度
- `h2s_concentration`: 硫化氢浓度
- `methane_concentration`: 甲烷浓度
- `ammonia_concentration`: 氨气浓度
- `water_level`: 液位高度
- `report_time`: 上报时间（自动生成）

### Alert（报警记录表）
- `Alertid`: 报警ID
- `content`: 报警内容
- `value`: 报警值
- `datetime`: 报警时间（自动生成）

### webuser（用户表）
- `userid`: 用户ID
- `username`: 用户名
- `password`: 密码
- `email`: 邮箱
- `age`: 年龄
- `hobby`: 爱好
- `kind`: 用户类型

### Threshold（阈值配置表）
- `threshold`: 阈值数值
- `indicator`: 指标名称

### Fan（风扇控制表）
- `id`: 主键
- `zt`: 状态（open/close）

## API接口

### 数据接口
1. **GET /upload** - ESP32上传传感器数据
   - 方法: POST
   - 数据格式: JSON
   - 参数: `co`, `h2s`, `ch4`, `nh3`, `height`

2. **GET /getMax** - 获取报警阈值
   - 方法: GET
   - 返回: JSON格式阈值数据

3. **POST /alert** - 提交报警信息
   - 方法: POST
   - 参数: `content`, `value`

### 设备控制接口
1. **GET /FanZT** - 获取风扇状态
2. **GET /FanStart** - 开启风扇
3. **GET /FanStop** - 关闭风扇

### 用户接口
1. **GET/POST /login** - 用户登录
2. **GET/POST /register** - 用户注册
3. **GET/POST /userpage** - 用户信息管理
4. **GET /outlogin** - 用户登出

## 安装部署

### 环境要求
- Python 3.8+
- Django 3.2+
- SQLite3

### 后端部署步骤
1. 克隆项目到本地
2. 安装依赖包：
   ```bash
   pip install django djangorestframework
   ```
3. 数据库迁移：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. 创建超级用户：
   ```bash
   python manage.py createsuperuser
   ```
5. 启动开发服务器：
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### ESP32部署步骤
1. 安装MicroPython固件到ESP32
2. 上传`esp32.py`到设备
3. 修改代码中的Wi-Fi配置：
   ```python
   wlan.connect('Kee', '17368601723')  # 替换为你的Wi-Fi信息
   ```
4. 修改服务器地址：
   ```python
   serverip = 'http://192.168.123.2:8000'  # 替换为你的服务器IP
   ```
5. 连接传感器到指定GPIO引脚

## 硬件连接指南

### ESP32引脚分配
- GPIO39: 水位传感器（ADC）
- GPIO33: 一氧化碳传感器（ADC）
- GPIO32: 硫化氢传感器（ADC）
- GPIO35: 甲烷传感器（ADC）
- GPIO34: 氨气传感器（ADC）
- GPIO15: 风扇继电器控制
- GPIO12: LED报警灯
- GPIO13: 蜂鸣器控制

### 传感器连接注意事项
1. 所有气体传感器使用3.3V供电
2. ADC引脚需配置为11dB衰减（0-3.3V测量范围）
3. 继电器模块需要外部电源供电
4. 蜂鸣器使用PWM控制音调

## 使用说明

### 管理员操作
1. 访问 `http://服务器IP:8000/admin` 进入管理后台
2. 配置阈值参数：
   - 进入Threshold模型
   - 设置各气体的报警阈值
3. 监控系统状态：
   - 查看实时数据
   - 管理报警记录
   - 监控设备状态

### 用户操作
1. **注册登录**：
   - 首次使用需注册账户
   - 使用用户名密码登录

2. **监控仪表盘**：
   - 首页查看各参数实时状态
   - 数据表格显示最新采集数据
   - 图表展示历史趋势

3. **设备控制**：
   - 进入"风扇"页面
   - 使用开关控制通风设备
   - 查看设备工作状态

4. **报警管理**：
   - 进入"警报"页面
   - 查看历史报警记录
   - 了解报警详情

## 故障排除

### 常见问题
1. **ESP32无法连接Wi-Fi**
   - 检查Wi-Fi密码是否正确
   - 确认信号强度
   - 查看ESP32的Wi-Fi模块是否正常

2. **传感器数据异常**
   - 检查传感器供电（3.3V）
   - 确认ADC引脚配置正确
   - 校准传感器参考值

3. **Web界面无法访问**
   - 确认Django服务器正在运行
   - 检查防火墙设置
   - 确认端口8000未被占用

4. **数据库操作错误**
   - 执行数据库迁移
   - 检查models.py定义
   - 查看SQLite数据库文件权限

### 调试建议
1. 启用Django调试模式（DEBUG=True）
2. 查看ESP32串口输出
3. 使用浏览器开发者工具查看网络请求
4. 检查数据库连接状态

## 安全注意事项

1. **密码安全**：
   - 建议实现密码加密存储
   - 添加密码复杂度验证
   - 定期更换密码

2. **API安全**：
   - 添加API访问限制
   - 实现请求频率限制
   - 考虑使用HTTPS加密传输

3. **数据安全**：
   - 定期备份数据库
   - 保护敏感配置信息
   - 实现操作日志记录

## 性能优化建议

1. **数据库优化**：
   - 为常用查询字段添加索引
   - 定期清理历史数据
   - 使用数据库连接池

2. **前端优化**：
   - 压缩静态资源
   - 使用CDN加速
   - 实现懒加载

3. **硬件优化**：
   - 调整数据采集频率
   - 优化ESP32休眠模式
   - 降低不必要的外设功耗

## 扩展开发

### 功能扩展建议
1. **移动端适配**：开发响应式移动界面
2. **多语言支持**：添加国际化支持
3. **数据导出**：支持Excel/PDF格式导出
4. **短信/邮件报警**：添加多渠道报警通知
5. **视频监控集成**：结合摄像头监控

### 技术升级方向
1. **数据库迁移**：从SQLite迁移到MySQL/PostgreSQL
2. **实时通信**：引入WebSocket实现实时推送
3. **容器化部署**：使用Docker容器化部署
4. **微服务架构**：将功能模块拆分为微服务

## 许可证

本项目采用MIT许可证，详情见LICENSE文件。

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。提交代码前请确保：
1. 代码符合PEP 8规范
2. 添加适当的注释
3. 更新相关文档
4. 通过现有测试
