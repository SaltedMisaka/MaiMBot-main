from typing import Optional, Dict, List
from openai import OpenAI
from .message import Message
import jieba
from nonebot import get_driver
from .config import global_config
from snownlp import SnowNLP
from ..models.utils_model import LLM_request

driver = get_driver()
config = driver.config  

class TopicIdentifier:
    def __init__(self):
        self.llm_client = LLM_request(model=global_config.llm_topic_extract)
        self.select=global_config.topic_extract

        
    async def identify_topic_llm(self, text: str) -> Optional[List[str]]:
        """识别消息主题，返回主题列表"""

        prompt = f"""判断这条消息的主题，如果没有明显主题请回复"无主题"，要求：
1. 主题通常2-4个字，必须简短，要求精准概括，不要太具体。
2. 建议给出多个主题，之间用英文逗号分割。只输出主题本身就好，不要有前后缀。

消息内容：{text}"""

        # 使用 LLM_request 类进行请求
        topic, _ = await self.llm_client.generate_response(prompt)
        
        if not topic:
            print(f"\033[1;31m[错误]\033[0m LLM API 返回为空")
            return None
            
        # 直接在这里处理主题解析
        if not topic or topic == "无主题":
            return None
            
        # 解析主题字符串为列表
        topic_list = [t.strip() for t in topic.split(",") if t.strip()]
        
        print(f"\033[1;32m[主题识别]\033[0m 主题: {topic_list}")
        return topic_list if topic_list else None

    def identify_topic_snownlp(self, text: str) -> Optional[List[str]]:
        """使用 SnowNLP 进行主题识别
        
        Args:
            text (str): 需要识别主题的文本
            
        Returns:
            Optional[List[str]]: 返回识别出的主题关键词列表，如果无法识别则返回 None
        """
        if not text or len(text.strip()) == 0:
            return None
            
        try:
            s = SnowNLP(text)
            # 提取前3个关键词作为主题
            keywords = s.keywords(5)
            return keywords if keywords else None
        except Exception as e:
            print(f"\033[1;31m[错误]\033[0m SnowNLP 处理失败: {str(e)}")
            return None

topic_identifier = TopicIdentifier()