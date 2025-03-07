import os
import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from dotenv import load_dotenv
from loguru import logger

'''彩蛋'''
from colorama import init, Fore

init()
text = "多年以后，面对行刑队，张三将会回想起他2023年在会议上讨论人工智能的那个下午"
rainbow_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
rainbow_text = ""
for i, char in enumerate(text):
    rainbow_text += rainbow_colors[i % len(rainbow_colors)] + char
print(rainbow_text)
'''彩蛋'''

# 初次启动检测
if not os.path.exists("config/bot_config.toml") or not os.path.exists(".env"):
    logger.info("检测到bot_config.toml不存在，正在从模板复制")
    import shutil

    shutil.copy("config/bot_config_template.toml", "config/bot_config.toml")
    logger.info("复制完成，请修改config/bot_config.toml和.env.prod中的配置后重新启动")

# 初始化.env 默认ENVIRONMENT=prod
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("ENVIRONMENT=prod")

    # 检测.env.prod文件是否存在
    if not os.path.exists(".env.prod"):
        logger.error("检测到.env.prod文件不存在")
        shutil.copy("template.env", "./.env.prod")

# 首先加载基础环境变量.env
if os.path.exists(".env"):
    load_dotenv(".env")
    logger.success("成功加载基础环境变量配置")

# 根据 ENVIRONMENT 加载对应的环境配置
if os.getenv("ENVIRONMENT") == "prod":
    logger.success("加载生产环境变量配置")
    load_dotenv(".env.prod", override=True)  # override=True 允许覆盖已存在的环境变量
elif os.getenv("ENVIRONMENT") == "dev":
    logger.success("加载开发环境变量配置")
    load_dotenv(".env.dev", override=True)  # override=True 允许覆盖已存在的环境变量
elif os.path.exists(f".env.{os.getenv('ENVIRONMENT')}"):
    logger.success(f"加载{os.getenv('ENVIRONMENT')}环境变量配置")
    load_dotenv(f".env.{os.getenv('ENVIRONMENT')}", override=True)  # override=True 允许覆盖已存在的环境变量
else:
    logger.error(f"ENVIRONMENT配置错误，请检查.env文件中的ENVIRONMENT变量对应的.env.{os.getenv('ENVIRONMENT')}是否存在")
    exit(1)

# 检测Key是否存在
if not os.getenv("SILICONFLOW_KEY"):
    logger.error("缺失必要的API KEY")
    logger.error(f"请至少在.env.{os.getenv('ENVIRONMENT')}文件中填写SILICONFLOW_KEY后重新启动")
    exit(1)

# 获取所有环境变量
env_config = {key: os.getenv(key) for key in os.environ}

# 设置基础配置
base_config = {
    "websocket_port": int(env_config.get("PORT", 8080)),
    "host": env_config.get("HOST", "127.0.0.1"),
    "log_level": "INFO",
}

# 合并配置
nonebot.init(**base_config, **env_config)

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 加载插件
nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run()
