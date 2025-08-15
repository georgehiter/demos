"""
智能文本分析LLM管理器 - 通义千问LLM调用实现

基于langchain_community.llms.Tongyi，提供同步调用接口。
"""

import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi
from langchain_core.runnables import Runnable

# 加载.env文件中的环境变量
load_dotenv()


class TongyiLLMManager(Runnable):
    """
    通义千问LLM管理器 - 真实的LLM调用实现，兼容LCEL管道
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

    def invoke(self, prompt: str, config=None) -> str:
        """
        调用通义千问LLM

        Args:
            prompt: 输入提示词
            config: 配置参数（LCEL标准参数）

        Returns:
            str: LLM响应结果

        Raises:
            Exception: 当API调用失败时抛出异常
        """
        try:
            response = self.llm.invoke(prompt)
            # 直接返回原始响应，让管道中的 StrOutputParser 处理
            return response
        except Exception as e:
            print(f"❌ 通义千问LLM调用失败: {e}")
            raise
