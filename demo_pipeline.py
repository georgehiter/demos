"""
LCEL核心管道 - LangChain LCEL串行处理管道

提供完整的分析管道，支持理论提取、表格提取和报告生成。
"""

from typing import TypedDict, Dict, Any
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnablePassthrough,
)

from tongyi_llm import TongyiLLMManager
from lcel_components import TheoryExtractor, TableExtractor, ReportGenerator


# 定义类型契约，提高代码可读性和类型安全性
class PipelineInput(TypedDict):
    """管道输入类型"""

    content: str


def create_analysis_pipeline() -> Runnable[PipelineInput, Dict[str, Any]]:
    """
    串行分析管道 - 理论提取 → 表格提取 → 报告生成 → 输出完整内容
    """
    llm_manager = TongyiLLMManager()

    return (
        # 确保输入格式正确
        RunnableLambda(lambda x: {"content": x["content"]})
        # 步骤1: 理论提取
        | RunnablePassthrough.assign(theory=TheoryExtractor())
        # 步骤2: 表格提取
        | RunnablePassthrough.assign(tables=TableExtractor())
        # 步骤3: 报告生成
        | RunnablePassthrough.assign(report=ReportGenerator(llm_manager))
        # 最后一步：返回包含所有内容的字典
        | RunnableLambda(
            lambda x: {
                "theory": x["theory"]["content"],
                "tables": x["tables"]["content"],
                "report": x["report"]["content"],
            }
        )
    )
