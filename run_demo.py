#!/usr/bin/env python3
"""
LCEL演示程序主入口

展示LangChain LCEL核心特性的简化实现，支持同步和异步模式。
"""

import asyncio
import sys
import argparse
from pathlib import Path
from typing import Dict, Any

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from mock_llm import MockLLMManager
from lcel_components import TheoryExtractor, TableExtractor, ReportGenerator
from demo_pipeline import create_analysis_pipeline, create_parallel_pipeline
from sample_data import get_sample_data, get_simple_data


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="LCEL演示程序 - 展示LangChain LCEL核心特性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_demo.py                    # 使用默认数据，异步模式
  python run_demo.py --sync             # 同步模式
  python run_demo.py --simple           # 使用简化数据
  python run_demo.py --pipeline-only    # 仅演示管道构建
        """,
    )
    
    parser.add_argument("--sync", action="store_true", help="使用同步模式")
    parser.add_argument("--simple", action="store_true", help="使用简化数据")
    parser.add_argument("--pipeline-only", action="store_true", help="仅演示管道构建")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细输出")
    
    return parser.parse_args()


def demonstrate_pipeline_building():
    """演示管道构建过程"""
    print("🔧 LCEL管道构建演示")
    print("=" * 50)
    
    # 1. 创建Mock LLM管理器
    print("\n1️⃣ 创建Mock LLM管理器")
    llm_manager = MockLLMManager()
    print(f"   最大并发调用数: {llm_manager.max_concurrent_calls}")
    print(f"   Mock延迟: {llm_manager.mock_delay}秒")
    
    # 2. 创建LCEL组件
    print("\n2️⃣ 创建LCEL组件")
    theory_extractor = TheoryExtractor(llm_manager)
    table_extractor = TableExtractor(llm_manager)
    report_generator = ReportGenerator(llm_manager)
    
    print(f"   理论提取器: {type(theory_extractor).__name__}")
    print(f"   表格提取器: {type(table_extractor).__name__}")
    print(f"   报告生成器: {type(report_generator).__name__}")
    
    # 3. 构建并行管道
    print("\n3️⃣ 构建并行处理管道")
    parallel_pipeline = create_parallel_pipeline()
    print(f"   并行管道类型: {type(parallel_pipeline).__name__}")
    
    # 4. 构建完整管道
    print("\n4️⃣ 构建完整分析管道")
    full_pipeline = create_analysis_pipeline()
    print(f"   完整管道类型: {type(full_pipeline).__name__}")
    
    print("\n✅ 管道构建演示完成！")


async def demonstrate_async_processing():
    """演示异步处理流程"""
    print("🚀 LCEL异步处理演示")
    print("=" * 50)
    
    # 获取示例数据
    data = get_simple_data() if args.simple else get_sample_data()
    content = data.get("theory", data.get("theory_text", ""))
    
    print(f"\n📝 输入内容长度: {len(content)} 字符")
    
    # 创建管道
    print("\n🔧 创建LCEL管道...")
    pipeline = create_analysis_pipeline()
    
    # 执行异步处理
    print("\n⚡ 开始异步处理...")
    start_time = asyncio.get_event_loop().time()
    
    try:
        result = await pipeline.ainvoke({"content": content})
        end_time = asyncio.get_event_loop().time()
        
        print(f"✅ 异步处理完成！耗时: {end_time - start_time:.2f}秒")
        print(f"📊 输出结果长度: {len(result)} 字符")
        
        if args.verbose:
            print("\n📄 输出结果预览:")
            print("-" * 40)
            print(result[:500] + "..." if len(result) > 500 else result)
            print("-" * 40)
        
    except Exception as e:
        print(f"❌ 异步处理失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


def demonstrate_sync_processing():
    """演示同步处理流程"""
    print("🔄 LCEL同步处理演示")
    print("=" * 50)
    
    # 获取示例数据
    data = get_simple_data() if args.simple else get_sample_data()
    content = data.get("theory", data.get("theory_text", ""))
    
    print(f"\n📝 输入内容长度: {len(content)} 字符")
    
    # 创建管道
    print("\n🔧 创建LCEL管道...")
    pipeline = create_analysis_pipeline()
    
    # 执行同步处理
    print("\n⚡ 开始同步处理...")
    start_time = asyncio.get_event_loop().time()
    
    try:
        result = pipeline.invoke({"content": content})
        end_time = asyncio.get_event_loop().time()
        
        print(f"✅ 同步处理完成！耗时: {end_time - start_time:.2f}秒")
        print(f"📊 输出结果长度: {len(result)} 字符")
        
        if args.verbose:
            print("\n📄 输出结果预览:")
            print("-" * 40)
            print(result[:500] + "..." if len(result) > 500 else result)
            print("-" * 40)
        
    except Exception as e:
        print(f"❌ 同步处理失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


async def demonstrate_component_workflow():
    """演示组件工作流程"""
    print("🔍 LCEL组件工作流程演示")
    print("=" * 50)
    
    # 获取示例数据
    data = get_simple_data() if args.simple else get_sample_data()
    theory_content = data.get("theory", data.get("theory_text", ""))
    table_content = data.get("table", data.get("table_data", ""))
    
    # 创建Mock LLM管理器
    llm_manager = MockLLMManager()
    
    print(f"\n📝 理论文本长度: {len(theory_content)} 字符")
    print(f"📊 表格内容长度: {len(table_content)} 字符")
    
    # 1. 理论提取
    print("\n1️⃣ 理论框架提取")
    theory_extractor = TheoryExtractor(llm_manager)
    theory_result = await theory_extractor.ainvoke({"content": theory_content})
    print(f"   提取的理论框架章节数: {len(theory_result)}")
    
    # 2. 表格提取
    print("\n2️⃣ 表格数据提取")
    table_extractor = TableExtractor(llm_manager)
    table_result = await table_extractor.ainvoke({"content": table_content})
    print(f"   提取的表格数量: {len(table_result)}")
    
    # 3. 报告生成
    print("\n3️⃣ 分析报告生成")
    report_generator = ReportGenerator(llm_manager)
    report_result = await report_generator.ainvoke({
        "theory": theory_result,
        "tables": table_result
    })
    print(f"   生成的报告长度: {len(report_result)} 字符")
    
    if args.verbose:
        print("\n📄 理论框架预览:")
        for section, content in list(theory_result.items())[:3]:
            print(f"   {section}: {len(content)} 项")
        
        print(f"\n📊 表格数据预览:")
        for i, table in enumerate(table_result[:2]):
            print(f"   表格 {i+1}: {len(table.headers)} 列 × {len(table.rows)} 行")
        
        print(f"\n📄 报告预览:")
        print("-" * 40)
        print(report_result[:300] + "..." if len(report_result) > 300 else report_result)
        print("-" * 40)
    
    print("\n✅ 组件工作流程演示完成！")


def main():
    """主函数"""
    print("🚀 LCEL演示程序")
    print("=" * 60)
    print("展示LangChain LCEL核心特性的简化实现")
    print("=" * 60)
    
    try:
        # 解析命令行参数
        global args
        args = parse_arguments()
        
        if args.verbose:
            print("📋 参数信息:")
            print(f"  - 同步模式: {args.sync}")
            print(f"  - 简化数据: {args.simple}")
            print(f"  - 仅管道演示: {args.pipeline_only}")
            print(f"  - 详细模式: {args.verbose}")
        
        # 根据参数选择演示模式
        if args.pipeline_only:
            demonstrate_pipeline_building()
        elif args.sync:
            demonstrate_sync_processing()
        else:
            # 默认异步模式
            if args.verbose:
                # 详细模式：演示组件工作流程
                asyncio.run(demonstrate_component_workflow())
            else:
                # 标准模式：演示异步处理
                asyncio.run(demonstrate_async_processing())
        
        print("\n🎉 演示程序运行完成！")
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
        return 1
    except Exception as e:
        print(f"❌ 程序运行失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

