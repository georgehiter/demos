#!/usr/bin/env python3
"""
异步架构性能对比演示

展示并行异步执行与串行执行的性能差异
"""

import asyncio
import time
from demo_pipeline import create_analysis_pipeline
from lcel_components import TheoryExtractor, TableExtractor
from tongyi_llm import TongyiLLMManager


async def read_sample_data():
    """读取示例数据"""
    try:
        with open("sample_data.md", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return """# 示例数据
        
社会懈怠理论（Social Loafing Theory）是组织行为学中的重要理论框架。
该理论探讨了在团队工作中，个体成员倾向于减少努力投入的现象。

## 实验数据

| 组别 | 样本数 | 前测得分 | 后测得分 |
|------|--------|----------|----------|
| 实验组 | 30 | 72.1 | 85.6 |
| 对照组 | 30 | 71.8 | 78.2 |

## 统计分析

| 指标 | 实验组 | 对照组 | P值 |
|------|--------|--------|-----|
| 前测 | 72.1 | 71.8 | 0.89 |
| 后测 | 85.6 | 78.2 | 0.02 |"""


async def parallel_execution_demo():
    """并行执行演示"""
    print("🚀 并行异步执行演示")
    print("=" * 50)

    content = await read_sample_data()
    print(f"📝 输入内容长度: {len(content)} 字符")

    # 创建并行异步管道
    pipeline = create_analysis_pipeline()

    # 记录开始时间
    start_time = time.time()

    # 执行并行异步管道
    result = await pipeline.ainvoke({"content": content})

    # 计算执行时间
    execution_time = time.time() - start_time

    print(f"⏱️  并行异步执行时间: {execution_time:.2f} 秒")
    print(f"✅ 理论提取状态: {result['theory']['status']}")
    print(f"✅ 表格提取状态: {result['tables']['status']}")
    print(f"✅ 报告生成状态: {result['report']['status']}")

    return execution_time, result


async def serial_execution_demo():
    """串行执行演示（模拟）"""
    print("\n🐌 串行执行演示（模拟）")
    print("=" * 50)

    content = await read_sample_data()
    print(f"📝 输入内容长度: {len(content)} 字符")

    # 创建组件
    theory_extractor = TheoryExtractor()
    table_extractor = TableExtractor()
    llm_manager = TongyiLLMManager()

    # 记录开始时间
    start_time = time.time()

    # 串行执行（模拟原有架构）
    print("🔄 执行理论提取...")
    theory_result = await theory_extractor.ainvoke({"content": content})

    print("🔄 执行表格提取...")
    tables_result = await table_extractor.ainvoke({"content": content})

    print("🔄 执行报告生成...")
    from lcel_components import ReportGenerator

    report_generator = ReportGenerator(llm_manager)
    report_result = await report_generator.ainvoke(
        {"theory": theory_result, "tables": tables_result}
    )

    # 计算执行时间
    execution_time = time.time() - start_time

    print(f"⏱️  串行执行时间: {execution_time:.2f} 秒")
    print(f"✅ 理论提取状态: {theory_result['status']}")
    print(f"✅ 表格提取状态: {tables_result['status']}")
    print(f"✅ 报告生成状态: {report_result['status']}")

    return execution_time, {
        "theory": theory_result,
        "tables": tables_result,
        "report": report_result,
    }


async def performance_comparison():
    """性能对比分析"""
    print("📊 异步架构性能对比分析")
    print("=" * 60)

    # 并行执行
    parallel_time, parallel_result = await parallel_execution_demo()

    # 串行执行
    serial_time, serial_result = await serial_execution_demo()

    # 性能分析
    print("\n📈 性能分析结果")
    print("=" * 40)

    time_saved = serial_time - parallel_time
    improvement_percentage = (time_saved / serial_time) * 100

    print(f"⏱️  并行异步执行时间: {parallel_time:.2f} 秒")
    print(f"⏱️  串行执行时间: {serial_time:.2f} 秒")
    print(f"🚀 节省时间: {time_saved:.2f} 秒")
    print(f"📈 性能提升: {improvement_percentage:.1f}%")

    if improvement_percentage > 0:
        print("🎉 并行异步架构性能更优！")
    else:
        print("⚠️  并行异步架构性能需要进一步优化")

    # 结果一致性验证
    print("\n🔍 结果一致性验证")
    print("=" * 30)

    theory_consistent = (
        parallel_result["theory"]["status"] == serial_result["theory"]["status"]
        and parallel_result["tables"]["status"] == serial_result["tables"]["status"]
        and parallel_result["report"]["status"] == serial_result["report"]["status"]
    )

    if theory_consistent:
        print("✅ 并行和串行执行结果一致")
    else:
        print("❌ 并行和串行执行结果不一致")

    return parallel_time, serial_time, improvement_percentage


async def main():
    """主函数"""
    print("🎯 LCEL异步架构性能对比演示")
    print("=" * 60)
    print("本演示将对比并行异步执行与串行执行的性能差异")
    print("并行执行：理论提取和表格提取同时进行")
    print("串行执行：理论提取 → 表格提取 → 报告生成")
    print()

    try:
        await performance_comparison()
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("请检查环境配置和依赖安装")


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
