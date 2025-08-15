"""
使用原生DashScope API调用通义千问LLM
"""

import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

load_dotenv()


class TongyiLLM:
    def __init__(self):
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("未设置环境变量 DASHSCOPE_API_KEY")

        dashscope.api_key = api_key
        self.model_name = "qwen3-235b-a22b-instruct-2507"

    def call(self, prompt: str) -> str:
        """调用LLM获取响应"""
        response = Generation.call(
            model=self.model_name,
            prompt=prompt,
            temperature=0.2,
            max_tokens=2000,
        )
        return response.output.text


def main():
    llm = TongyiLLM()
    response = llm.call("你好，请简单介绍一下你自己")
    print(response)


if __name__ == "__main__":
    main()
