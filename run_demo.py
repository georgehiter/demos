#!/usr/bin/env python3
"""
LCEL演示程序主入口（简化版本）

展示LangChain LCEL核心特性的管道工作流程。
"""

from demo_pipeline import create_analysis_pipeline
from sample_data import get_sample_data


def main():
    """主程序入口"""
    print("🚀 LCEL演示程序")
    print("=" * 40)

    # 获取示例数据
    data = get_sample_data()
    content = data.get("theory_text", "") + "\n\n" + data.get("table_data", "")

    print(f"📝 输入内容长度: {len(content)} 字符")

    # 创建并运行管道
    pipeline = create_analysis_pipeline()
    result = pipeline.invoke({"content": content})

    print(f"\n✅ 管道执行完成！")

    # 打印管道返回的结果
    print("\n📊 管道返回结果:")
    print("=" * 40)

    if "theory" in result:
        print(f"📚 理论提取结果:")
        print(f"   {result['theory']}")
        print()

    if "tables" in result:
        print(f"📋 表格提取结果:")
        print(f"   {result['tables']}")
        print()

    if "report" in result:
        print(f"📝 报告生成结果:")
        print(f"   {result['report']}")
        print()

    print("=" * 40)


if __name__ == "__main__":
    main()
