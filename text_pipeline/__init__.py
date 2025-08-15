"""
智能文本分析管道

这是一个基于LangChain LCEL的智能文本分析工具，支持理论提取、表格分析和报告生成。
"""

__version__ = "1.0.0"
__author__ = "GeorgeHit"
__email__ = "noricerice@gmail.com"

from .components import TheoryExtractor, TableExtractor, ReportGenerator
from .pipeline import create_analysis_pipeline
from .llm_manager import TongyiLLMManager

__all__ = [
    "TheoryExtractor",
    "TableExtractor",
    "ReportGenerator",
    "create_analysis_pipeline",
    "TongyiLLMManager",
]
