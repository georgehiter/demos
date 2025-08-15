"""
LCEL核心管道 - LangChain LCEL并行处理管道

提供完整的分析管道，支持理论提取和表格提取并行执行，报告生成串行处理。
"""

from typing import Dict, Any
from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
    RunnableParallel,
)

from tongyi_llm import TongyiLLMManager
from lcel_components import TheoryExtractor, TableExtractor, ReportGenerator


def create_analysis_pipeline() -> Runnable[Dict[str, str], Dict[str, Any]]:
    """
    分析管道 - 理论提取和表格提取并行执行 → 报告生成 → 输出完整内容

    支持并行处理，提升执行效率。理论提取和表格提取同时进行，
    报告生成基于并行结果串行执行。
    """
    llm_manager = TongyiLLMManager()

    return RunnableParallel(
        {"theory": TheoryExtractor(llm_manager), "tables": TableExtractor(llm_manager)}
    ) | RunnablePassthrough.assign(report=ReportGenerator(llm_manager))
