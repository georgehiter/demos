"""
LangChain + 通义千问(Qwen) LLM 链式调用示例
结合你提供的TongyiLLM类和LangChain的链式操作

环境变量设置说明：
在运行此程序之前，需要设置 DASHSCOPE_API_KEY 环境变量。

Windows 系统设置环境变量步骤：
方法1 - 通过系统设置（推荐）：
1. 右键点击"此电脑"或"我的电脑" → 选择"属性"
2. 点击"高级系统设置"
3. 在"系统属性"窗口中点击"环境变量"按钮
4. 在"用户变量"区域点击"新建"
5. 变量名输入：DASHSCOPE_API_KEY
6. 变量值输入：你的通义千问API密钥
7. 点击"确定"保存
8. 重启命令提示符或PowerShell，使环境变量生效

方法2 - 通过命令行（临时设置）：
1. 打开命令提示符或PowerShell
2. 输入命令：set DASHSCOPE_API_KEY=你的API密钥
3. 在同一会话中运行程序

方法3 - 创建 .env 文件：
1. 在项目根目录创建 .env 文件
2. 在文件中添加：DASHSCOPE_API_KEY=你的API密钥
3. 确保 .env 文件不会被提交到版本控制系统

获取通义千问API密钥：
1. 访问 https://dashscope.aliyun.com/
2. 注册/登录阿里云账号
3. 开通通义千问服务
4. 在控制台获取API密钥

库安装说明：
在运行此程序之前，需要安装以下Python库：

方法1 - 使用pip安装（推荐）：
1. 打开命令提示符或PowerShell
2. 确保已安装Python（建议Python 3.8+）
3. 执行以下命令安装所需库：
   pip install langchain
   pip install langchain-core
   pip install langchain-community
   pip install python-dotenv

方法2 - 使用requirements.txt安装：
1. 在项目根目录创建requirements.txt文件，内容如下：
   langchain
   langchain-core
   langchain-community
   python-dotenv
2. 执行命令：pip install -r requirements.txt

方法3 - 使用conda安装（如果使用Anaconda）：
1. 打开Anaconda Prompt
2. 执行以下命令：
   conda install -c conda-forge langchain
   conda install -c conda-forge python-dotenv
   pip install langchain-core langchain-community

验证安装：
安装完成后，可以在Python中测试导入：
   python -c "import langchain; import langchain_core; import langchain_community; import dotenv; print('所有库安装成功！')"

注意：设置环境变量后需要重启终端或IDE才能生效
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
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
    # 初始化Qwen LLM
    try:
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            print("请设置环境变量 DASHSCOPE_API_KEY")
            return

        # 直接使用LangChain的Tongyi
        model = TongyiLLM().call

        # 创建提示模板
        prompt = PromptTemplate.from_template(
            "请告诉我一个关于{topic}的笑话，要求幽默有趣。"
        )

        # 创建输出解析器
        output_parser = StrOutputParser()

        # 创建链 - 使用管道操作符连接
        chain = prompt | model | output_parser

        # 示例1: 编程笑话
        print("=== 示例1: 编程笑话 ===")
        result = chain.invoke({"topic": "编程"})
        print(result)
        print("\n" + "=" * 50 + "\n")

        # 示例2: 人工智能笑话
        print("=== 示例2: 人工智能笑话 ===")
        result = chain.invoke({"topic": "人工智能"})
        print(result)
        print("\n" + "=" * 50 + "\n")

        # 示例3: 更复杂的提示模板
        complex_prompt = PromptTemplate.from_template(
            """作为一个{role}，请用{style}的风格回答以下问题：
            
问题: {question}

请确保回答简洁明了，不超过100字。"""
        )

        # 创建新的链
        complex_chain = complex_prompt | model | output_parser

        print("=== 示例3: 复杂提示模板 ===")
        result = complex_chain.invoke(
            {
                "role": "资深程序员",
                "style": "幽默诙谐",
                "question": "为什么程序员喜欢用黑色主题的IDE？",
            }
        )
        print(result)
        print("\n" + "=" * 50 + "\n")

        # 示例4: 使用你原有的TongyiLLM类
        print("=== 示例4: 使用封装的TongyiLLM类 ===")
        tongyi_llm = TongyiLLM()
        simple_response = tongyi_llm.call("请用一句话介绍什么是LangChain")
        print(simple_response)

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已正确设置DASHSCOPE_API_KEY环境变量")


if __name__ == "__main__":
    main()
