"""
通义千问LLM管理器 - 真实的LLM调用实现

基于langchain_community.llms.Tongyi，提供同步调用接口。
"""

import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi
from langchain_core.output_parsers import StrOutputParser

# 加载.env文件中的环境变量
load_dotenv()


class TongyiLLMManager:
    """
    通义千问LLM管理器 - 真实的LLM调用实现
    """

    def __init__(self):
        """初始化LLM管理器"""
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("未设置环境变量 DASHSCOPE_API_KEY")

        self.llm = Tongyi(
            dashscope_api_key=api_key,
            model_name="qwen3-235b-a22b-instruct-2507",
            temperature=0.2,
            max_tokens=2000,
        )
        self.parser = StrOutputParser()

    def invoke(self, prompt: str) -> str:
        """
        调用通义千问LLM

        Args:
            prompt: 输入提示词

        Returns:
            str: LLM响应结果

        Raises:
            Exception: 当API调用失败时抛出异常
        """
        try:
            response = self.llm.invoke(prompt)
            result = self.parser.parse(response)
            return result
        except Exception as e:
            print(f"❌ 通义千问LLM调用失败: {e}")
            raise
