#Broca's Area
# 功能：语言产生、语法处理和言语运动控制。
# 损伤后果：布洛卡失语症（表达困难，但理解保留）。

import time


class Thinking_Idea:
    def __init__(self, message_id: str):
        self.messages = []  # 消息列表集合
        self.current_thoughts = []  # 当前思考内容列表
        self.time = time.time()  # 创建时间
        self.id = str(int(time.time() * 1000))  # 使用时间戳生成唯一标识ID
        