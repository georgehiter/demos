"""
核心LCEL组件 - 实现Runnable接口的同步版本

包含理论提取器、表格提取器和报告生成器，所有组件都支持同步调用。
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


@dataclass
class TableData:
    """表格数据结构"""

    title: str
    headers: List[str]
    rows: List[List[str]]
    start_line: int = 0
    end_line: int = 0
    interpretation: str = ""


class TheoryExtractor(Runnable):
    """
    理论框架提取器 - 实现Runnable接口

    使用Mock LLM提取理论框架，支持同步调用。
    """

    def __init__(self, llm_manager=None, enable_llm_summary: bool = True):
        """初始化理论提取器"""
        self.llm_manager = llm_manager
        self.enable_llm_summary = enable_llm_summary

    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> Dict[str, Any]:
        """
        同步调用接口 - 符合LCEL Runnable标准

        Args:
            inputs: 输入参数字典，必须包含content键
            config: 配置参数（LCEL标准参数）

        Returns:
            Dict[str, Any]: 提取的理论框架，包含结构化信息
        """
        content = inputs.get("content", "")
        theory_data = self.extract_theory(content)

        # 返回统一结构的字典
        return {
            "type": "theory_framework",
            "content": theory_data,
            "status": "success",
            "summary": "理论框架提取完成",
            "metadata": {
                "llm_summary_used": "LLM总结" in theory_data,
                "has_content": len(theory_data) > 0,
            },
        }

    def extract_theory(self, content: str) -> Dict[str, List[str]]:
        """
        提取理论框架的核心逻辑

        Args:
            content: 理论文本内容

        Returns:
            Dict[str, List[str]]: 提取的理论框架
        """
        # 获取前20行内容用于LLM分析
        lines = content.split("\n")
        first_20_lines = lines[:20]

        print(f"📝 [Theory] 使用前20行内容进行分析，共{len(first_20_lines)}行")

        # 尝试使用LLM进行总结
        if self.enable_llm_summary and self.llm_manager:
            print(f"🤖 [Theory] 尝试使用LLM进行内容总结...")
            summary = self._summarize_with_llm(content)
            if summary:
                print(f"✅ [Theory] LLM总结完成")
                return {"LLM总结": summary}
            else:
                print(f"ℹ️ [Theory] 使用原有逻辑，未进行LLM总结")

        # 如果没有LLM总结，返回空结果
        return {}

    def _create_summary_prompt(self, content: str) -> str:
        """
        创建总结提示词

        Args:
            content: 需要总结的内容

        Returns:
            str: 格式化的提示词
        """
        return f"""你是一个专业的理论分析专家。请对以下理论内容进行简洁的总结，提取核心观点和关键概念：

{content}

请提供简洁明了的总结，重点突出理论的核心内容和主要观点。"""

    def _summarize_with_llm(self, content: str) -> str:
        """
        使用LLM进行内容总结

        Args:
            content: 需要总结的内容

        Returns:
            str: 总结结果，失败时返回空字符串
        """
        if not self.llm_manager or not self.enable_llm_summary:
            return ""

        try:
            return self.llm_manager.invoke(self._create_summary_prompt(content)) or ""
        except:
            return ""


class TableExtractor(Runnable):
    """
    极简表格提取器 - 支持表格提取和并行LLM格式化

    使用ThreadPoolExecutor实现并行处理，代码简洁易维护。
    """

    def __init__(self, llm_manager=None):
        """初始化表格提取器"""
        self.llm_manager = llm_manager

    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> Dict[str, Any]:
        """
        同步调用接口 - 符合LCEL Runnable标准
        """
        if "content" not in inputs:
            raise ValueError("输入必须包含content键")

        content = inputs["content"]
        tables = self._extract_tables(content)

        if self.llm_manager:
            print(f"🤖 [Table] 识别到{len(tables)}个表格，开始并行LLM格式化...")
            # 并行LLM格式化
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self._format_table, table) for table in tables
                ]
                results = [f.result() for f in futures]
            print(f"✅ [Table] 所有表格LLM格式化完成")
            return {
                "content": results,
                "status": "success",
                "metadata": {"table_count": len(results)},
            }
        else:
            return {
                "content": tables,
                "status": "success",
                "metadata": {"table_count": len(tables)},
            }

    def _extract_tables(self, content: str) -> List[List[List[str]]]:
        """提取所有表格内容"""
        lines = content.split("\n")
        tables = []
        i = 0

        while i < len(lines):
            if self._is_table_line(lines[i]):
                table_data = self._extract_single_table(lines, i)
                if table_data:
                    tables.append(table_data["content"])
                    i = table_data["end_line"] + 1
                else:
                    i += 1
            else:
                i += 1

        return tables

    def _is_table_line(self, line: str) -> bool:
        """检查是否是表格行"""
        return "|" in line.strip() and line.strip().count("|") >= 2

    def _extract_single_table(self, lines: List[str], start: int) -> dict:
        """提取单个表格"""
        table_content = []
        i = start

        while i < len(lines) and self._is_table_line(lines[i]):
            line = lines[i].strip()
            # 跳过分隔符行
            if not re.match(r"^\|[\s\-:|]+\|$", line):
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                if cells:
                    table_content.append(cells)
            i += 1

        if table_content:
            return {"content": table_content, "end_line": i - 1}
        return None

    def _format_table(self, table_content: List[List[str]]) -> dict:
        """格式化单个表格"""
        try:
            prompt = self._create_formatting_prompt(table_content)
            formatted_table = self.llm_manager.invoke(prompt)
            if formatted_table:
                return {
                    "原始表格": table_content,
                    "LLM格式化表格": formatted_table,
                }
            else:
                return {"原始表格": table_content}
        except Exception as e:
            print(f"⚠️ [Table] 表格格式化失败: {e}")
            return {"原始表格": table_content}

    def _create_formatting_prompt(self, table_content: List[List[str]]) -> str:
        """创建表格格式化提示词"""
        table_str = "\n".join(["| " + " | ".join(row) + " |" for row in table_content])

        return f"""你是一个专业的表格分析专家。请对以下表格进行结构整理和格式化：

{table_str}

请重新组织表格结构，优化列的顺序和内容，使其更加清晰易读。保持数据的完整性，输出格式化的表格内容。请使用Markdown表格格式。"""


class ReportGenerator(Runnable):
    """
    报告生成器 - 实现Runnable接口

    基于理论和表格数据生成分析报告，使用完全LCEL化的管道。
    """

    def __init__(self, llm_manager):
        """初始化报告生成器"""
        self.llm_manager = llm_manager

        # 创建 PromptTemplate 提示词模板
        self.prompt_template = PromptTemplate.from_template(
            """你是一个专业的论文分析专家，擅长基于理论和数据生成分析报告。

请基于以下信息生成一份详细的论文分析报告：

## 理论框架
{theory_content}

## 表格数据
{tables_content}

请生成一份结构清晰、内容详实的分析报告，包括：
1. 主要理论观点
2. 数据分析和发现

回答仅需要以上两个部分，不需要总结。"""
        )

        # 创建完整的 LCEL 管道
        self.chain = (
            RunnablePassthrough.assign(
                theory_content=lambda x: x["theory"].get("content", "暂无理论框架数据"),
                tables_content=lambda x: x["tables"].get("content", "暂无表格数据"),
            )
            | self.prompt_template
            | self.llm_manager
            | StrOutputParser()
        )

    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> Dict[str, Any]:
        """
        同步调用接口 - 符合LCEL Runnable标准

        Args:
            inputs: 输入参数字典，包含theory和tables键
            config: 配置参数（LCEL标准参数）

        Returns:
            Dict[str, Any]: 生成的报告，包含结构化信息
        """
        # 检查输入内容
        theory_framework = inputs.get("theory", {})
        tables = inputs.get("tables", {})

        # 检查是否都为空
        if not theory_framework.get("content") and not tables.get("content"):
            return {
                "type": "report",
                "content": "⚠️ 警告：理论框架和表格数据都为空，无法生成有意义的分析报告。",
                "status": "warning",
                "summary": "数据不足，无法生成报告",
                "metadata": {},
            }

        # 尝试使用LLM进行报告生成
        print(f"🤖 [Report] 尝试使用LLM进行报告生成...")
        response = self.chain.invoke(inputs)
        print(f"✅ [Report] LLM报告生成完成")

        # 返回统一结构的字典
        return {
            "type": "report",
            "content": response,
            "status": "success",
            "summary": "报告生成完成",
            "metadata": {
                "word_count": len(response.split()),
                "char_count": len(response),
                "llm_report_used": True,
            },
        }
