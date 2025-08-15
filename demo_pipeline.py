"""
LCEL核心管道 - LangChain LCEL串行处理管道

提供完整的分析管道，支持理论提取、表格提取和报告生成。
"""

from typing import Dict, Any
from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
    RunnableLambda,
)

from tongyi_llm import TongyiLLMManager
from lcel_components import TheoryExtractor, TableExtractor, ReportGenerator


def create_analysis_pipeline() -> Runnable[Dict[str, str], Dict[str, Any]]:
    """
    分析管道 - 理论提取 → 表格提取 → 报告生成 → 输出完整内容
    """
    llm_manager = TongyiLLMManager()

    return (
        RunnablePassthrough.assign(theory=TheoryExtractor(llm_manager))
        | RunnablePassthrough.assign(tables=TableExtractor(llm_manager))
        | RunnablePassthrough.assign(report=ReportGenerator(llm_manager))
    )
