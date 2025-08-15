"""
核心LCEL组件 - 实现Runnable接口的同步版本

包含理论提取器、表格提取器和报告生成器，所有组件都支持同步调用。
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass

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

    def __init__(self, llm_manager=None):
        """初始化理论提取器"""
        self.llm_manager = llm_manager

    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> Dict[str, Any]:
        """
        同步调用接口 - 符合LCEL Runnable标准

        Args:
            inputs: 输入参数字典，必须包含content键
            config: 配置参数（LCEL标准参数）

        Returns:
            Dict[str, Any]: 提取的理论框架，包含结构化信息
        """
        if "content" not in inputs:
            raise ValueError("输入必须包含content键")

        content = inputs["content"]
        theory_data = self.extract_theory(content)

        # 返回统一结构的字典
        return {
            "type": "theory_framework",
            "content": theory_data,
            "status": "success",
            "summary": "理论框架提取完成",
            "metadata": {"line_count": len(theory_data.get("前20行内容", []))},
        }

    def extract_theory(self, content: str) -> Dict[str, List[str]]:
        """
        提取理论框架的核心逻辑

        Args:
            content: 理论文本内容

        Returns:
            Dict[str, List[str]]: 提取的理论框架
        """
        try:
            # 获取前20行内容
            lines = content.split("\n")
            first_20_lines = lines[:20]

            print(f"📝 [Theory] 使用前20行内容进行分析，共{len(first_20_lines)}行")

            # 直接获取前20行内容
            return self.get_first_20_lines(first_20_lines)

        except Exception as e:
            print(f"❌ [Theory] 理论框架提取失败: {e}")
            return self.get_default_framework()

    def get_first_20_lines(self, lines: List[str]) -> Dict[str, List[str]]:
        """
        获取前20行内容信息

        Args:
            lines: 前20行内容列表

        Returns:
            Dict[str, List[str]]: 前20行内容
        """
        # 提取非空行
        non_empty_lines = [line.strip() for line in lines if line.strip()]

        return {"前20行内容": non_empty_lines}

    def get_default_framework(self) -> Dict[str, List[str]]:
        """获取默认的理论框架"""
        return {"前20行内容": []}


class TableExtractor(Runnable):
    """
    简化表格提取器 - 只提取表格内容
    """

    def extract_tables(self, content: str) -> List[List[List[str]]]:
        """
        提取所有表格内容

        Returns:
            List[List[List[str]]]: 表格列表，每个表格是行的列表，每行是单元格的列表
        """
        lines = content.split("\n")
        tables = []
        i = 0

        while i < len(lines):
            if self.is_table_line(lines[i]):
                table_data = self.extract_single_table(lines, i)
                if table_data:
                    tables.append(table_data["content"])
                    i = table_data["end_line"] + 1
                else:
                    i += 1
            else:
                i += 1

        return tables

    def is_table_line(self, line: str) -> bool:
        """检查是否是表格行"""
        return "|" in line.strip() and line.strip().count("|") >= 2

    def extract_single_table(self, lines: List[str], start: int) -> dict:
        """提取单个表格"""
        table_content = []
        i = start

        # 找到所有连续的表格行
        while i < len(lines) and self.is_table_line(lines[i]):
            line = lines[i].strip()
            # 跳过分隔符行（包含 --- 的行）
            if not re.match(r"^\|[\s\-:|]+\|$", line):
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                if cells:  # 确保不是空行
                    table_content.append(cells)
            i += 1

        if table_content:
            return {"content": table_content, "end_line": i - 1}
        return None

    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> Dict[str, Any]:
        """
        同步调用接口 - 符合LCEL Runnable标准

        Args:
            inputs: 输入参数字典，必须包含content键
            config: 配置参数（LCEL标准参数）

        Returns:
            Dict[str, Any]: 提取的表格数据，包含结构化信息
        """
        if "content" not in inputs:
            raise ValueError("输入必须包含content键")

        content = inputs["content"]
        tables_data = self.extract_tables(content)

        # 返回统一结构的字典
        return {
            "type": "table_data",
            "content": tables_data,
            "status": "success",
            "summary": "表格提取完成",
            "metadata": {"table_count": len(tables_data)},
        }


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
1. 研究背景和目的
2. 主要理论观点
3. 数据分析和发现
4. 结论和建议

请使用Markdown格式，确保报告逻辑清晰、内容完整。"""
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

        # 使用 LCEL 管道生成报告
        response = self.chain.invoke(inputs)

        # 返回统一结构的字典
        return {
            "type": "report",
            "content": response,
            "status": "success",
            "summary": "报告生成完成",
            "metadata": {
                "word_count": len(response.split()),
                "char_count": len(response),
            },
        }
