import tomli
import tomli_w
import sys
from pathlib import Path
import os

def sync_configs():
    # 读取两个配置文件
    try:
        with open('bot_config_dev.toml', 'rb') as f:  # tomli需要使用二进制模式读取
            dev_config = tomli.load(f)
        
        with open('bot_config.toml', 'rb') as f:
            prod_config = tomli.load(f)
    except FileNotFoundError as e:
        print(f"错误：找不到配置文件 - {e}")
        sys.exit(1)
    except tomli.TOMLDecodeError as e:
        print(f"错误：TOML格式解析失败 - {e}")
        sys.exit(1)

    # 递归合并配置
    def merge_configs(source, target):
        for key, value in source.items():
            if key not in target:
                target[key] = value
            elif isinstance(value, dict) and isinstance(target[key], dict):
                merge_configs(value, target[key])

    # 将dev配置的新属性合并到prod配置中
    merge_configs(dev_config, prod_config)

    # 保存更新后的配置
    try:
        with open('bot_config.toml', 'wb') as f:  # tomli_w需要使用二进制模式写入
            tomli_w.dump(prod_config, f)
        print("配置文件同步完成！")
    except Exception as e:
        print(f"错误：保存配置文件失败 - {e}")
        sys.exit(1)

if __name__ == '__main__':
    # 确保在正确的目录下运行
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    sync_configs()
