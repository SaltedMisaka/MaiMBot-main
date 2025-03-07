from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message as EventMessage, Bot
from .message import Message, MessageSet, Message_Sending
from .config import BotConfig, global_config
from .storage import MessageStorage
from .llm_generator import ResponseGenerator
# from .message_stream import MessageStream, MessageStreamContainer
from .topic_identifier import topic_identifier
from random import random, choice
from .emoji_manager import emoji_manager  # 导入表情包管理器
import time
import os
from .cq_code import CQCode  # 导入CQCode模块
from .message_sender import message_manager  # 导入新的消息管理器
from .message import Message_Thinking  # 导入 Message_Thinking 类
from .relationship_manager import relationship_manager
from .willing_manager import willing_manager  # 导入意愿管理器
from .utils import is_mentioned_bot_in_txt, calculate_typing_time
from ..memory_system.memory import memory_graph
from loguru import logger

class ChatBot:
    def __init__(self):
        self.storage = MessageStorage()
        self.gpt = ResponseGenerator()
        self.bot = None  # bot 实例引用
        self._started = False
        
        self.emoji_chance = 0.2  # 发送表情包的基础概率
        # self.message_streams = MessageStreamContainer()
        
    async def _ensure_started(self):
        """确保所有任务已启动"""
        if not self._started:
            self._started = True

    async def handle_message(self, event: GroupMessageEvent, bot: Bot) -> None:
        """处理收到的群消息"""
        
        if event.group_id not in global_config.talk_allowed_groups:
            return
        self.bot = bot  # 更新 bot 实例
        
        if event.user_id in global_config.ban_user_id:
            return

        group_info = await bot.get_group_info(group_id=event.group_id)
        sender_info = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id, no_cache=True)
        
        await relationship_manager.update_relationship(user_id = event.user_id, data = sender_info)
        await relationship_manager.update_relationship_value(user_id = event.user_id, relationship_value = 0.5)
        
        message = Message(
            group_id=event.group_id,
            user_id=event.user_id,
            message_id=event.message_id,
            user_cardname=sender_info['card'],
            raw_message=str(event.original_message), 
            plain_text=event.get_plaintext(),
            reply_message=event.reply,
        )

        # 过滤词
        for word in global_config.ban_words:
            if word in message.detailed_plain_text:
                logger.info(f"\033[1;32m[{message.group_name}]{message.user_nickname}:\033[0m {message.processed_plain_text}")
                logger.info(f"\033[1;32m[过滤词识别]\033[0m 消息中含有{word}，filtered")
                return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(message.time))



        topic=await topic_identifier.identify_topic_llm(message.processed_plain_text)


        # topic1 = topic_identifier.identify_topic_jieba(message.processed_plain_text)
        # topic2 = await topic_identifier.identify_topic_llm(message.processed_plain_text)
        # topic3 = topic_identifier.identify_topic_snownlp(message.processed_plain_text)
        logger.info(f"\033[1;32m[主题识别]\033[0m 使用{global_config.topic_extract}主题: {topic}")
        
        all_num = 0
        interested_num = 0
        if topic:
            for current_topic in topic:
                all_num += 1
                first_layer_items, second_layer_items = memory_graph.get_related_item(current_topic, depth=2)
                if first_layer_items:
                    interested_num += 1
                    print(f"\033[1;32m[前额叶]\033[0m 对|{current_topic}|有印象")
        interested_rate = interested_num / all_num if all_num > 0 else 0
        
        await self.storage.store_message(message, topic[0] if topic else None)

        is_mentioned = is_mentioned_bot_in_txt(message.processed_plain_text)
        reply_probability = willing_manager.change_reply_willing_received(
            event.group_id, 
            topic[0] if topic else None,
            is_mentioned,
            global_config,
            event.user_id,
            message.is_emoji,
            interested_rate
        )
        current_willing = willing_manager.get_willing(event.group_id)
        
        
        print(f"\033[1;32m[{current_time}][{message.group_name}]{message.user_nickname}:\033[0m {message.processed_plain_text}\033[1;36m[回复意愿:{current_willing:.2f}][概率:{reply_probability * 100:.1f}%]\033[0m")

        response = ""
        
        if random() < reply_probability:
            
            
            tinking_time_point = round(time.time(), 2)
            think_id = 'mt' + str(tinking_time_point)
            thinking_message = Message_Thinking(message=message,message_id=think_id)
            
            message_manager.add_message(thinking_message)

            willing_manager.change_reply_willing_sent(thinking_message.group_id)
            
            response, emotion = await self.gpt.generate_response(message)

            # if response is None:
                # thinking_message.interupt=True
            
        if response:
            # print(f"\033[1;32m[思考结束]\033[0m 思考结束，已得到回复，开始回复")
            # 找到并删除对应的thinking消息
            container = message_manager.get_container(event.group_id)
            thinking_message = None
            # 找到message,删除
            for msg in container.messages:
                if isinstance(msg, Message_Thinking) and msg.message_id == think_id:
                    thinking_message = msg
                    container.messages.remove(msg)
                    print(f"\033[1;32m[思考消息删除]\033[0m 已找到思考消息对象，开始删除")
                    break
            
            #记录开始思考的时间，避免从思考到回复的时间太久
            thinking_start_time = thinking_message.thinking_start_time
            message_set = MessageSet(event.group_id, global_config.BOT_QQ, think_id) # 发送消息的id和产生发送消息的message_thinking是一致的
            #计算打字时间，1是为了模拟打字，2是避免多条回复乱序
            accu_typing_time = 0
            
            # print(f"\033[1;32m[开始回复]\033[0m 开始将回复1载入发送容器")
            for msg in response:
                # print(f"\033[1;32m[回复内容]\033[0m {msg}")
                #通过时间改变时间戳
                typing_time = calculate_typing_time(msg)
                accu_typing_time += typing_time
                timepoint = tinking_time_point + accu_typing_time
                
                bot_message = Message_Sending(
                    group_id=event.group_id,
                    user_id=global_config.BOT_QQ,
                    message_id=think_id,
                    raw_message=msg,
                    plain_text=msg,
                    processed_plain_text=msg,
                    user_nickname=global_config.BOT_NICKNAME,
                    group_name=message.group_name,
                    time=timepoint, #记录了回复生成的时间
                    thinking_start_time=thinking_start_time, #记录了思考开始的时间
                    reply_message_id=message.message_id
                )
                message_set.add_message(bot_message)
                
            #message_set 可以直接加入 message_manager
            print(f"\033[1;32m[回复]\033[0m 将回复载入发送容器")
            message_manager.add_message(message_set)
            
            bot_response_time = tinking_time_point
            if random() < global_config.emoji_chance:
                emoji_path = await emoji_manager.get_emoji_for_emotion(emotion)
                if emoji_path:
                    emoji_cq = CQCode.create_emoji_cq(emoji_path)
                    
                    if random() < 0.5:
                        bot_response_time = tinking_time_point - 1
                    else:
                        bot_response_time = bot_response_time + 1
                        
                    bot_message = Message_Sending(
                        group_id=event.group_id,
                        user_id=global_config.BOT_QQ,
                        message_id=0,
                        raw_message=emoji_cq,
                        plain_text=emoji_cq,
                        processed_plain_text=emoji_cq,
                        user_nickname=global_config.BOT_NICKNAME,
                        group_name=message.group_name,
                        time=bot_response_time,
                        is_emoji=True,
                        translate_cq=False,
                        thinking_start_time=thinking_start_time,
                        # reply_message_id=message.message_id
                    )
                    message_manager.add_message(bot_message)
        
        willing_manager.change_reply_willing_after_sent(event.group_id)

# 创建全局ChatBot实例
chat_bot = ChatBot()