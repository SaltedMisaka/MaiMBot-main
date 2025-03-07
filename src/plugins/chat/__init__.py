from loguru import logger
from nonebot import on_message, on_command, require, get_driver
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageSegment
from nonebot.typing import T_State
from ...common.database import Database
from .config import global_config
import os
import asyncio
import random
from .relationship_manager import relationship_manager
from ..schedule.schedule_generator import bot_schedule
from .willing_manager import willing_manager
from nonebot.rule import to_me
from .bot import chat_bot
from .emoji_manager import emoji_manager
import time


# 获取驱动器
driver = get_driver()
config = driver.config

Database.initialize(
        host= config.MONGODB_HOST,
        port= int(config.MONGODB_PORT),
        db_name= config.DATABASE_NAME,
        #username= config.MONGODB_USERNAME,
        #password= config.MONGODB_PASSWORD,
        #auth_source= config.MONGODB_AUTH_SOURCE
)
print("\033[1;32m[初始化数据库完成]\033[0m")


# 导入其他模块
from .bot import ChatBot
from .emoji_manager import emoji_manager
# from .message_send_control import message_sender
from .relationship_manager import relationship_manager
from .message_sender import message_manager,message_sender
from ..memory_system.memory import memory_graph,hippocampus

# 初始化表情管理器
emoji_manager.initialize()

print(f"\033[1;32m正在唤醒{global_config.BOT_NICKNAME}......\033[0m")
# 创建机器人实例
chat_bot = ChatBot()
# 注册群消息处理器
group_msg = on_message(priority=5)
# 创建定时任务
scheduler = require("nonebot_plugin_apscheduler").scheduler



@driver.on_startup
async def start_background_tasks():
    """启动后台任务"""
    # 只启动表情包管理任务
    asyncio.create_task(emoji_manager.start_periodic_check(interval_MINS=global_config.EMOJI_CHECK_INTERVAL))
    await bot_schedule.initialize()
    bot_schedule.print_schedule()
    
@driver.on_startup
async def init_relationships():
    """在 NoneBot2 启动时初始化关系管理器"""
    print("\033[1;32m[初始化]\033[0m 正在加载用户关系数据...")
    await relationship_manager.load_all_relationships()
    asyncio.create_task(relationship_manager._start_relationship_manager())

@driver.on_bot_connect
async def _(bot: Bot):
    """Bot连接成功时的处理"""
    print(f"\033[1;38;5;208m-----------{global_config.BOT_NICKNAME}成功连接！-----------\033[0m")
    await willing_manager.ensure_started()
    
    
    message_sender.set_bot(bot)
    print("\033[1;38;5;208m-----------消息发送器已启动！-----------\033[0m")
    asyncio.create_task(message_manager.start_processor())
    print("\033[1;38;5;208m-----------消息处理器已启动！-----------\033[0m")
    
    asyncio.create_task(emoji_manager._periodic_scan(interval_MINS=global_config.EMOJI_REGISTER_INTERVAL))
    print("\033[1;38;5;208m-----------开始偷表情包！-----------\033[0m")
    # 启动消息发送控制任务
    
@group_msg.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await chat_bot.handle_message(event, bot)

# 添加build_memory定时任务
@scheduler.scheduled_job("interval", seconds=global_config.build_memory_interval, id="build_memory")
async def build_memory_task():
    """每30秒执行一次记忆构建"""
    print("\033[1;32m[记忆构建]\033[0m -------------------------------------------开始构建记忆-------------------------------------------")
    start_time = time.time()
    await hippocampus.operation_build_memory(chat_size=20)
    end_time = time.time()
    print(f"\033[1;32m[记忆构建]\033[0m -------------------------------------------记忆构建完成：耗时: {end_time - start_time:.2f} 秒-------------------------------------------")
    
@scheduler.scheduled_job("interval", seconds=global_config.forget_memory_interval, id="forget_memory") 
async def forget_memory_task():
    """每30秒执行一次记忆构建"""
    # print("\033[1;32m[记忆遗忘]\033[0m 开始遗忘记忆...")
    # await hippocampus.operation_forget_topic(percentage=0.1)
    # print("\033[1;32m[记忆遗忘]\033[0m 记忆遗忘完成")

@scheduler.scheduled_job("interval", seconds=global_config.build_memory_interval + 10, id="merge_memory")
async def merge_memory_task():
    """每30秒执行一次记忆构建"""
    # print("\033[1;32m[记忆整合]\033[0m 开始整合")
    # await hippocampus.operation_merge_memory(percentage=0.1)
    # print("\033[1;32m[记忆整合]\033[0m 记忆整合完成")
  
