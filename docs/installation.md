# 🔧 安装与配置指南

## 部署方式

如果你不知道Docker是什么，建议寻找相关教程或使用手动部署

### 🐳 Docker部署（推荐，但不一定是最新）

1. 获取配置文件：
```bash
wget https://raw.githubusercontent.com/SengokuCola/MaiMBot/main/docker-compose.yml
```

2. 启动服务：
```bash
NAPCAT_UID=$(id -u) NAPCAT_GID=$(id -g) docker compose up -d
```

3. 修改配置后重启：
```bash
NAPCAT_UID=$(id -u) NAPCAT_GID=$(id -g) docker compose restart
```

### 📦 手动部署

1. **环境准备**
```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\\Scripts\\activate   # Windows
# 安装依赖
pip install -r requirements.txt
```

2. **配置MongoDB**
- 安装并启动MongoDB服务
- 默认连接本地27017端口

3. **配置NapCat**
- 安装并登录NapCat
- 添加反向WS：`ws://localhost:8080/onebot/v11/ws`

4. **配置文件设置**
- 修改环境配置文件：`.env.prod`
- 修改机器人配置文件：`bot_config.toml`

5. **启动麦麦机器人**
- 打开命令行，cd到对应路径
```bash
nb run
```

6. **其他组件**
- `run_thingking.bat`: 启动可视化推理界面（未完善）

- ~~`knowledge.bat`: 将`/data/raw_info`下的文本文档载入数据库~~
- 直接运行 knowledge.py生成知识库

## ⚙️ 配置说明

### 环境配置 (.env.prod)
```ini
# API配置,你可以在这里定义你的密钥和base_url
# 你可以选择定义其他服务商提供的KEY，完全可以自定义
SILICONFLOW_KEY=your_key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1/
DEEP_SEEK_KEY=your_key
DEEP_SEEK_BASE_URL=https://api.deepseek.com/v1

# 服务配置,如果你不知道这是什么，保持默认
HOST=127.0.0.1
PORT=8080

# 数据库配置,如果你不知道这是什么，保持默认
MONGODB_HOST=127.0.0.1
MONGODB_PORT=27017
DATABASE_NAME=MegBot
```

### 机器人配置 (bot_config.toml)
```toml
[bot]
qq = "你的机器人QQ号"
nickname = "麦麦"

[message]
min_text_length = 2
max_context_size = 15
emoji_chance = 0.2

[emoji]
check_interval = 120
register_interval = 10

[cq_code]
enable_pic_translate = false

[response]
#现已移除deepseek或硅基流动选项，可以直接切换分别配置任意模型
model_r1_probability = 0.8 #推理模型权重
model_v3_probability = 0.1 #非推理模型权重
model_r1_distill_probability = 0.1

[memory]
build_memory_interval = 300

[others]
enable_advance_output = true  # 是否启用详细日志输出

[groups]
talk_allowed = []      # 允许回复的群号列表
talk_frequency_down = []   # 降低回复频率的群号列表
ban_user_id = []      # 禁止回复的用户QQ号列表

[model.llm_reasoning]
name = "Pro/deepseek-ai/DeepSeek-R1"
base_url = "SILICONFLOW_BASE_URL"
key = "SILICONFLOW_KEY"

[model.llm_reasoning_minor]
name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
base_url = "SILICONFLOW_BASE_URL"
key = "SILICONFLOW_KEY"

[model.llm_normal]
name = "Pro/deepseek-ai/DeepSeek-V3"
base_url = "SILICONFLOW_BASE_URL"
key = "SILICONFLOW_KEY"

[model.llm_normal_minor]
name = "deepseek-ai/DeepSeek-V2.5"
base_url = "SILICONFLOW_BASE_URL"
key = "SILICONFLOW_KEY"

[model.vlm]
name = "deepseek-ai/deepseek-vl2"
base_url = "SILICONFLOW_BASE_URL"
key = "SILICONFLOW_KEY"
```

## ⚠️ 注意事项

- 目前部署方案仍在测试中，可能存在未知问题
- 配置文件中的API密钥请妥善保管，不要泄露
- 建议先在测试环境中运行，确认无误后再部署到生产环境 