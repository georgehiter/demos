"""
LCEL管道演示 - 展示LangChain LCEL的核心特性

包含并行处理、管道组合、类型安全等LCEL核心功能。
"""

from typing import TypedDict, List, Dict, Any
from langchain_core.runnables import (
    RunnableParallel,
    Runnable,
)
from langchain_core.output_parsers import StrOutputParser

from mock_llm import MockLLMManager
from lcel_components import TheoryExtractor, TableExtractor, ReportGenerator


# 定义类型契约，提高代码可读性和类型安全性
class PipelineInput(TypedDict):
    """管道输入类型"""
    content: str


class PipelineOutput(TypedDict):
    """管道输出类型"""
    theory: Dict[str, List[str]]
    tables: List[Any]
    report: str


def create_analysis_pipeline() -> Runnable[PipelineInput, str]:
    """
    创建分析管道 - 优化的 LCEL 构建
    
    Returns:
        Runnable[PipelineInput, str]: 完整的分析管道，输入为PipelineInput，输出为字符串
    """
    # 初始化Mock LLM管理器
    llm_manager = MockLLMManager()
    
    # 初始化LCEL组件
    theory_extractor = TheoryExtractor(llm_manager)
    table_extractor = TableExtractor(llm_manager)
    report_generator = ReportGenerator(llm_manager)
    
    # 构建优化的 LCEL 管道 - 减少数据包装，提高可读性
    return (
        RunnableParallel({
            "theory": theory_extractor,
            "tables": table_extractor,
        })
        | report_generator
        | StrOutputParser()
    )


def create_theory_only_pipeline() -> Runnable[PipelineInput, Dict[str, List[str]]]:
    """
    创建仅理论提取的管道
    
    Returns:
        Runnable[PipelineInput, Dict[str, List[str]]]: 理论提取管道
    """
    llm_manager = MockLLMManager()
    theory_extractor = TheoryExtractor(llm_manager)
    
    return theory_extractor


def create_table_only_pipeline() -> Runnable[PipelineInput, List[Any]]:
    """
    创建仅表格提取的管道
    
    Returns:
        Runnable[PipelineInput, List[Any]]: 表格提取管道
    """
    llm_manager = MockLLMManager()
    table_extractor = TableExtractor(llm_manager)
    
    return table_extractor


def create_parallel_pipeline() -> Runnable[PipelineInput, Dict[str, Any]]:
    """
    创建并行处理管道（不包含报告生成）
    
    Returns:
        Runnable[PipelineInput, Dict[str, Any]]: 并行处理管道
    """
    llm_manager = MockLLMManager()
    
    theory_extractor = TheoryExtractor(llm_manager)
    table_extractor = TableExtractor(llm_manager)
    
    # 仅并行处理，不生成报告
    return RunnableParallel({
        "theory": theory_extractor,
        "tables": table_extractor,
    })


def create_custom_pipeline(*components: Runnable) -> Runnable:
    """
    创建自定义管道
    
    Args:
        *components: 要组合的LCEL组件
        
    Returns:
        Runnable: 自定义管道
    """
    if not components:
        raise ValueError("至少需要一个组件")
    
    # 使用管道操作符组合组件
    pipeline = components[0]
    for component in components[1:]:
        pipeline = pipeline | component
    
    return pipeline


def get_pipeline_info(pipeline: Runnable) -> Dict[str, Any]:
    """
    获取管道信息
    
    Args:
        pipeline: LCEL管道
        
    Returns:
        Dict[str, Any]: 管道信息
    """
    return {
        "type": type(pipeline).__name__,
        "input_schema": getattr(pipeline, "input_schema", "未知"),
        "output_schema": getattr(pipeline, "output_schema", "未知"),
        "config_schema": getattr(pipeline, "config_schema", "未知"),
    }


def demonstrate_pipeline_flow():
    """
    演示管道流程
    
    展示LCEL管道的构建和使用方法
    """
    print("🔧 LCEL管道演示")
    print("=" * 50)
    
    # 1. 创建完整管道
    print("\n1️⃣ 创建完整分析管道")
    full_pipeline = create_analysis_pipeline()
    print(f"   管道类型: {type(full_pipeline).__name__}")
    
    # 2. 创建理论提取管道
    print("\n2️⃣ 创建理论提取管道")
    theory_pipeline = create_theory_only_pipeline()
    print(f"   管道类型: {type(theory_pipeline).__name__}")
    
    # 3. 创建表格提取管道
    print("\n3️⃣ 创建表格提取管道")
    table_pipeline = create_table_only_pipeline()
    print(f"   管道类型: {type(table_pipeline).__name__}")
    
    # 4. 创建并行处理管道
    print("\n4️⃣ 创建并行处理管道")
    parallel_pipeline = create_parallel_pipeline()
    print(f"   管道类型: {type(parallel_pipeline).__name__}")
    
    # 5. 管道信息
    print("\n5️⃣ 管道信息")
    pipelines = [
        ("完整管道", full_pipeline),
        ("理论管道", theory_pipeline),
        ("表格管道", table_pipeline),
        ("并行管道", parallel_pipeline),
    ]
    
    for name, pipeline in pipelines:
        info = get_pipeline_info(pipeline)
        print(f"   {name}: {info['type']}")
    
    print("\n✅ 管道演示完成！")


if __name__ == "__main__":
    demonstrate_pipeline_flow()
