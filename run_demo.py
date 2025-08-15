#!/usr/bin/env python3
"""
LCEL演示程序主入口（简化版本）

展示LangChain LCEL核心特性的管道工作流程。
"""

from demo_pipeline import create_analysis_pipeline
from datetime import datetime
from typing import Dict, Any


def read_markdown_data(file_path="sample_data.md"):
    """
    读取Markdown文档中的示例数据

    Args:
        file_path (str): Markdown文件路径

    Returns:
        str: 文档内容
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content

    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {file_path}")
        return ""
    except Exception as e:
        print(f"❌ 错误：读取文件时出现问题 - {e}")
        return ""


def main():
    """主程序入口"""
    print("🚀 LCEL演示程序")
    print("=" * 40)

    # 从Markdown文档读取示例数据
    content = read_markdown_data()

    if not content:
        print("❌ 无法读取示例数据，程序退出")
        return

    print(f"📝 输入内容长度: {len(content)} 字符")

    # 创建并运行管道
    pipeline = create_analysis_pipeline()
    result = pipeline.invoke({"content": content})

    print(f"\n✅ 管道执行完成！")

    # 将管道结果保存到 Markdown 文档
    save_results_to_md(result, "pipeline_results.md")

    print("📄 结果已保存到 pipeline_results.md")


def save_results_to_md(result: Dict[str, Any], filename: str):
    """
    将管道结果保存到 Markdown 文档

    Args:
        result: 管道返回的结果
        filename: 保存的文件名
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# LCEL 管道分析结果\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if "theory" in result:
            f.write("## 📚 理论提取结果\n\n")
            f.write(f"**状态**: {result['theory'].get('status', 'N/A')}\n\n")
            f.write(f"**摘要**: {result['theory'].get('summary', 'N/A')}\n\n")
            f.write("**内容**:\n\n")

            theory_content = result["theory"].get("content", {})
            if isinstance(theory_content, dict):
                # 只显示LLM总结
                if "LLM总结" in theory_content:
                    f.write("**LLM智能总结**:\n\n")
                    f.write(f"{theory_content['LLM总结']}\n\n")
                else:
                    f.write("⚠️ 未生成LLM总结内容\n\n")
            else:
                f.write(f"{theory_content}\n")
            f.write("\n")

        if "tables" in result:
            f.write("## 📋 表格提取结果\n\n")
            f.write(f"**状态**: {result['tables'].get('status', 'N/A')}\n\n")
            f.write(f"**摘要**: {result['tables'].get('summary', 'N/A')}\n\n")
            f.write(
                f"**表格数量**: {result['tables'].get('metadata', {}).get('table_count', 'N/A')}\n\n"
            )
            f.write("**内容**:\n\n")

            tables_content = result["tables"].get("content", [])
            for i, table in enumerate(tables_content, 1):
                f.write(f"### 表格 {i}\n\n")

                # 检查是否是LLM格式化的表格
                if isinstance(table, dict) and "LLM格式化表格" in table:
                    f.write("**LLM格式化表格**:\n\n")
                    f.write(f"{table['LLM格式化表格']}\n\n")
                    f.write("**原始表格**:\n\n")
                    # 显示原始表格
                    for row in table["原始表格"]:
                        f.write("| " + " | ".join(row) + " |\n")
                else:
                    # 显示普通表格
                    for row in table:
                        f.write("| " + " | ".join(row) + " |\n")
                f.write("\n")

        if "report" in result:
            f.write("## 📝 报告生成结果\n\n")
            f.write(f"**状态**: {result['report'].get('status', 'N/A')}\n\n")
            f.write(f"**摘要**: {result['report'].get('summary', 'N/A')}\n\n")
            f.write(
                f"**字数统计**: {result['report'].get('metadata', {}).get('word_count', 'N/A')} 字\n\n"
            )
            f.write("**内容**:\n\n")
            f.write(result["report"].get("content", "N/A"))
            f.write("\n")


if __name__ == "__main__":
    main()
