"""
简化的通义千问LLM调用器
"""

import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi

load_dotenv()


class TongyiLLM:
    def __init__(self):
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("未设置环境变量 DASHSCOPE_API_KEY")

        self.llm = Tongyi(
            dashscope_api_key=api_key,
            model_name="qwen3-235b-a22b-instruct-2507",
            temperature=0.2,
            max_tokens=2000,
        )

    def call(self, prompt: str) -> str:
        """调用LLM获取响应"""
        return self.llm.invoke(prompt)


def main():
    llm = TongyiLLM()
    response = llm.call("你好，请简单介绍一下你自己")
    print(response)


if __name__ == "__main__":
    main()