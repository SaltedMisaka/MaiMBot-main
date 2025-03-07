from typing import Dict, List, Any, Optional
import time
import threading
from collections import defaultdict
import asyncio
from .message import Message
from ...common.database import Database

class MessageStorage:
    def __init__(self):
        self.db = Database.get_instance()
        
    async def store_message(self, message: Message, topic: Optional[str] = None) -> None:
        """存储消息到数据库"""
        try:
            if not message.is_emoji:
                message_data = {
                    "group_id": message.group_id,
                    "user_id": message.user_id,
                    "message_id": message.message_id,
                    "raw_message": message.raw_message,
                    "plain_text": message.plain_text,
                    "processed_plain_text": message.processed_plain_text,
                    "time": message.time,
                    "user_nickname": message.user_nickname,
                    "user_cardname": message.user_cardname,
                    "group_name": message.group_name,
                    "topic": topic,
                    "detailed_plain_text": message.detailed_plain_text,
                }
            else:
                message_data = {
                    "group_id": message.group_id,
                    "user_id": message.user_id,
                    "message_id": message.message_id,
                    "raw_message": message.raw_message,
                    "plain_text": message.plain_text,
                    "processed_plain_text": '[表情包]',
                    "time": message.time,
                    "user_nickname": message.user_nickname,
                    "user_cardname": message.user_cardname,
                    "group_name": message.group_name,
                    "topic": topic,
                    "detailed_plain_text": message.detailed_plain_text,
                }
                
            self.db.db.messages.insert_one(message_data)
        except Exception as e:
            print(f"\033[1;31m[错误]\033[0m 存储消息失败: {e}") 

# 如果需要其他存储相关的函数，可以在这里添加 