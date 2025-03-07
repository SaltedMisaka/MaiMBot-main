from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Set
import os
import configparser
import tomli
import sys
from loguru import logger
from nonebot import get_driver



@dataclass
class BotConfig:
    """机器人配置类"""    
    BOT_QQ: Optional[int] = 1
    BOT_NICKNAME: Optional[str] = None
    
    # 消息处理相关配置
    MIN_TEXT_LENGTH: int = 2  # 最小处理文本长度
    MAX_CONTEXT_SIZE: int = 15  # 上下文最大消息数
    emoji_chance: float = 0.2  # 发送表情包的基础概率
    
    ENABLE_PIC_TRANSLATE: bool = True  # 是否启用图片翻译
    
    talk_allowed_groups = set()
    talk_frequency_down_groups = set()
    ban_user_id = set()
    
    build_memory_interval: int = 30  # 记忆构建间隔（秒）
    forget_memory_interval: int = 300  # 记忆遗忘间隔（秒）
    EMOJI_CHECK_INTERVAL: int = 120  # 表情包检查间隔（分钟）
    EMOJI_REGISTER_INTERVAL: int = 10  # 表情包注册间隔（分钟）

    ban_words = set()
    
    # 模型配置
    llm_reasoning: Dict[str, str] = field(default_factory=lambda: {})
    llm_reasoning_minor: Dict[str, str] = field(default_factory=lambda: {})
    llm_normal: Dict[str, str] = field(default_factory=lambda: {})
    llm_normal_minor: Dict[str, str] = field(default_factory=lambda: {})
    embedding: Dict[str, str] = field(default_factory=lambda: {})
    vlm: Dict[str, str] = field(default_factory=lambda: {})

    # 主题提取配置
    topic_extract: str = 'snownlp' # 只支持jieba,snownlp,llm
    llm_topic_extract: Dict[str, str] = field(default_factory=lambda: {})
    
    API_USING: str = "deepseek"  # 使用的API
    API_PAID: bool = False  # 是否使用付费API
    MODEL_R1_PROBABILITY: float = 0.8  # R1模型概率
    MODEL_V3_PROBABILITY: float = 0.1  # V3模型概率
    MODEL_R1_DISTILL_PROBABILITY: float = 0.1  # R1蒸馏模型概率
    
    enable_advance_output: bool = False  # 是否启用高级输出
    enable_kuuki_read: bool = True # 是否启用读空气功能

    # 默认人设
    PROMPT_PERSONALITY=[
        "曾经是一个学习地质的女大学生，现在学习心理学和脑科学，你会刷贴吧",
        "是一个女大学生，你有黑色头发，你会刷小红书"
    ]
    PROMPT_SCHEDULE_GEN="一个曾经学习地质,现在学习心理学和脑科学的女大学生，喜欢刷qq，贴吧，知乎和小红书"
    
    @staticmethod
    def get_config_dir() -> str:
        """获取配置文件目录"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        config_dir = os.path.join(root_dir, 'config')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return config_dir

    
    @classmethod
    def load_config(cls, config_path: str = None) -> "BotConfig":
        """从TOML配置文件加载配置"""
        config = cls()
        if os.path.exists(config_path):
            with open(config_path, "rb") as f:
                toml_dict = tomli.load(f)
            
            if 'personality' in toml_dict:
                personality_config=toml_dict['personality']
                personality=personality_config.get('prompt_personality')
                if len(personality) >= 2:
                    logger.info(f"载入自定义人格:{personality}")
                    config.PROMPT_PERSONALITY=personality_config.get('prompt_personality',config.PROMPT_PERSONALITY)
                logger.info(f"载入自定义日程prompt:{personality_config.get('prompt_schedule',config.PROMPT_SCHEDULE_GEN)}")
                config.PROMPT_SCHEDULE_GEN=personality_config.get('prompt_schedule',config.PROMPT_SCHEDULE_GEN)

            if "emoji" in toml_dict:
                emoji_config = toml_dict["emoji"]
                config.EMOJI_CHECK_INTERVAL = emoji_config.get("check_interval", config.EMOJI_CHECK_INTERVAL)
                config.EMOJI_REGISTER_INTERVAL = emoji_config.get("register_interval", config.EMOJI_REGISTER_INTERVAL)
            
            if "cq_code" in toml_dict:
                cq_code_config = toml_dict["cq_code"]
                config.ENABLE_PIC_TRANSLATE = cq_code_config.get("enable_pic_translate", config.ENABLE_PIC_TRANSLATE)
            
            # 机器人基础配置
            if "bot" in toml_dict:
                bot_config = toml_dict["bot"]
                bot_qq = bot_config.get("qq")
                config.BOT_QQ = int(bot_qq)
                config.BOT_NICKNAME = bot_config.get("nickname", config.BOT_NICKNAME)
                
            if "response" in toml_dict:
                response_config = toml_dict["response"]
                config.MODEL_R1_PROBABILITY = response_config.get("model_r1_probability", config.MODEL_R1_PROBABILITY)
                config.MODEL_V3_PROBABILITY = response_config.get("model_v3_probability", config.MODEL_V3_PROBABILITY)
                config.MODEL_R1_DISTILL_PROBABILITY = response_config.get("model_r1_distill_probability", config.MODEL_R1_DISTILL_PROBABILITY)
                config.API_USING = response_config.get("api_using", config.API_USING)
                config.API_PAID = response_config.get("api_paid", config.API_PAID)
                
            # 加载模型配置
            if "model" in toml_dict:
                model_config = toml_dict["model"]
                
                if "llm_reasoning" in model_config:
                    config.llm_reasoning = model_config["llm_reasoning"]
                
                if "llm_reasoning_minor" in model_config:
                    config.llm_reasoning_minor = model_config["llm_reasoning_minor"]
                
                if "llm_normal" in model_config:
                    config.llm_normal = model_config["llm_normal"]
                    config.llm_topic_extract = config.llm_normal
                
                if "llm_normal_minor" in model_config:
                    config.llm_normal_minor = model_config["llm_normal_minor"]
                
                if "vlm" in model_config:
                    config.vlm = model_config["vlm"]
                    
                if "embedding" in model_config:
                    config.embedding = model_config["embedding"]
                
            if 'topic' in toml_dict:
                topic_config=toml_dict['topic']
                if 'topic_extract' in topic_config:
                    config.topic_extract=topic_config.get('topic_extract',config.topic_extract)
                    logger.info(f"载入自定义主题提取为{config.topic_extract}")
                if config.topic_extract=='llm' and 'llm_topic' in topic_config:
                    config.llm_topic_extract=topic_config['llm_topic']
                    logger.info(f"载入自定义主题提取模型为{config.llm_topic_extract['name']}")
                
            # 消息配置
            if "message" in toml_dict:
                msg_config = toml_dict["message"]
                config.MIN_TEXT_LENGTH = msg_config.get("min_text_length", config.MIN_TEXT_LENGTH)
                config.MAX_CONTEXT_SIZE = msg_config.get("max_context_size", config.MAX_CONTEXT_SIZE)
                config.emoji_chance = msg_config.get("emoji_chance", config.emoji_chance)
                config.ban_words=msg_config.get("ban_words",config.ban_words)

            if "memory" in toml_dict:
                memory_config = toml_dict["memory"]
                config.build_memory_interval = memory_config.get("build_memory_interval", config.build_memory_interval)
                config.forget_memory_interval = memory_config.get("forget_memory_interval", config.forget_memory_interval)
            
            # 群组配置
            if "groups" in toml_dict:
                groups_config = toml_dict["groups"]
                config.talk_allowed_groups = set(groups_config.get("talk_allowed", []))
                config.talk_frequency_down_groups = set(groups_config.get("talk_frequency_down", []))
                config.ban_user_id = set(groups_config.get("ban_user_id", []))
            
            if "others" in toml_dict:
                others_config = toml_dict["others"]
                config.enable_advance_output = others_config.get("enable_advance_output", config.enable_advance_output)
                config.enable_kuuki_read = others_config.get("enable_kuuki_read", config.enable_kuuki_read)
            
            logger.success(f"成功加载配置文件: {config_path}")
                
        return config 
    
# 获取配置文件路径

bot_config_floder_path = BotConfig.get_config_dir()
print(f"正在品鉴配置文件目录: {bot_config_floder_path}")
bot_config_path = os.path.join(bot_config_floder_path, "bot_config_dev.toml")
if not os.path.exists(bot_config_path):
    # 如果开发环境配置文件不存在，则使用默认配置文件
    bot_config_path = os.path.join(bot_config_floder_path, "bot_config.toml")
    logger.info("使用bot配置文件")
else:
    logger.info("已找到开发bot配置文件")

global_config = BotConfig.load_config(config_path=bot_config_path)


if not global_config.enable_advance_output:
    logger.remove()
    pass

