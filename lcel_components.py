"""
核心LCEL组件 - 实现Runnable接口的简化版本

包含理论提取器、表格提取器和报告生成器，所有组件都支持异步调用。
"""

import asyncio
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from langchain_core.runnables import Runnable


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
    
    使用Mock LLM提取理论框架，支持异步调用。
    """
    
    def __init__(self, llm_manager):
        """初始化理论提取器"""
        self.llm_manager = llm_manager
    
    async def ainvoke(self, inputs: Dict[str, Any], config: Any = None) -> Dict[str, List[str]]:
        """
        异步调用接口 - 符合LCEL Runnable标准
        
        Args:
            inputs: 输入参数字典，必须包含content键
            config: 配置参数（LCEL标准参数）
            
        Returns:
            Dict[str, List[str]]: 提取的理论框架
        """
        if "content" not in inputs:
            raise ValueError("输入必须包含content键")
        
        content = inputs["content"]
        return await self.extract_theory(content)
    
    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> Dict[str, List[str]]:
        """
        同步调用接口 - 符合LCEL Runnable标准
        
        Args:
            inputs: 输入参数字典，必须包含content键
            config: 配置参数（LCEL标准参数）
            
        Returns:
            Dict[str, List[str]]: 提取的理论框架
        """
        return asyncio.run(self.ainvoke(inputs, config))
    
    async def extract_theory(self, content: str) -> Dict[str, List[str]]:
        """
        提取理论框架的核心逻辑
        
        Args:
            content: 理论文本内容
            
        Returns:
            Dict[str, List[str]]: 提取的理论框架
        """
        try:
            # 构建提示词
            prompt = f"请从以下理论文本中提取理论框架：\n\n{content}"
            
            # 调用Mock LLM
            response = await self.llm_manager.invoke_with_retry(prompt)
            
            # 解析响应
            return self.parse_response(response)
            
        except Exception as e:
            print(f"❌ [Theory] 理论框架提取失败: {e}")
            return self.get_default_framework()
    
    def parse_response(self, response: str) -> Dict[str, List[str]]:
        """
        解析LLM响应
        
        Args:
            response: LLM响应文本
            
        Returns:
            Dict[str, List[str]]: 解析后的理论框架
        """
        try:
            lines = response.strip().split("\n")
            framework = {}
            current_section = None
            current_content = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith("##") or line.startswith("#"):
                    # 保存之前的章节
                    if current_section and current_content:
                        framework[current_section] = current_content
                    
                    # 开始新章节
                    current_section = line.lstrip("#").strip()
                    current_content = []
                elif current_section:
                    current_content.append(line)
            
            # 保存最后一个章节
            if current_section and current_content:
                framework[current_section] = current_content
            
            return framework if framework else self.get_default_framework()
            
        except Exception as e:
            print(f"⚠️ [Theory] 解析响应失败: {e}")
            return self.get_default_framework()
    
    def get_default_framework(self) -> Dict[str, List[str]]:
        """获取默认理论框架"""
        return {
            "研究背景": ["需要进一步分析"],
            "研究方法": ["基于文献分析的研究方法"],
            "主要发现": ["需要进一步分析"],
            "结论": ["需要进一步分析"]
        }


class TableExtractor(Runnable):
    """
    表格提取器 - 实现Runnable接口
    
    识别和解析Markdown表格，使用Mock LLM增强表格数据。
    """
    
    def __init__(self, llm_manager):
        """初始化表格提取器"""
        self.llm_manager = llm_manager
    
    async def ainvoke(self, inputs: Dict[str, Any], config: Any = None) -> List[TableData]:
        """
        异步调用接口 - 符合LCEL Runnable标准
        
        Args:
            inputs: 输入参数字典，必须包含content键
            config: 配置参数（LCEL标准参数）
            
        Returns:
            List[TableData]: 提取的表格列表
        """
        if "content" not in inputs:
            raise ValueError("输入必须包含content键")
        
        content = inputs["content"]
        return await self.extract_tables(content)
    
    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> List[TableData]:
        """
        同步调用接口 - 符合LCEL Runnable标准
        
        Args:
            inputs: 输入参数字典，必须包含content键
            config: 配置参数（LCEL标准参数）
            
        Returns:
            List[TableData]: 提取的表格列表
        """
        return asyncio.run(self.ainvoke(inputs, config))
    
    async def extract_tables(self, content: str) -> List[TableData]:
        """
        提取表格
        
        Args:
            content: 文件内容
            
        Returns:
            List[TableData]: 提取的表格列表
        """
        tables = self.extract_tables_manually(content)
        
        if not tables:
            return []
        
        # 异步增强表格
        enhanced_tables = await self.enhance_tables(tables)
        return enhanced_tables
    
    def extract_tables_manually(self, content: str) -> List[TableData]:
        """
        手动提取表格（不依赖LLM）
        
        Args:
            content: 文件内容
            
        Returns:
            List[TableData]: 提取的表格列表
        """
        lines = content.split("\n")
        tables = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 检查是否是表格开始
            if self.is_table_start(line, lines, i):
                table = self.parse_table_content(lines, i)
                if table:
                    tables.append(table)
                    i = table.end_line + 1
                else:
                    i += 1
            else:
                i += 1
        
        return tables
    
    def is_table_start(self, line: str, lines: List[str], line_index: int) -> bool:
        """检查是否是表格开始"""
        if "|" in line:
            # 检查下一行是否包含分隔符
            if line_index + 1 < len(lines):
                next_line = lines[line_index + 1].strip()
                if re.match(r"^\|[\s\-:|]+\|$", next_line):
                    return True
        return False
    
    def parse_table_content(self, lines: List[str], start_line: int) -> Optional[TableData]:
        """
        解析表格内容
        
        Args:
            lines: 文件行列表
            start_line: 表格开始行
            
        Returns:
            Optional[TableData]: 解析后的表格对象
        """
        try:
            # 找到表格结束行
            end_line = start_line
            for i in range(start_line, len(lines)):
                line = lines[i].strip()
                if not line or not line.startswith("|"):
                    end_line = i - 1
                    break
                end_line = i
            
            # 提取表格内容
            table_lines = lines[start_line:end_line + 1]
            headers, rows = self.parse_table_lines(table_lines)
            
            if not headers:
                return None
            
            # 创建表格对象
            table = TableData(
                title=f"表格 {start_line}",
                headers=headers,
                rows=rows,
                interpretation=""
            )
            
            return table
            
        except Exception as e:
            print(f"⚠️ [Table] 解析表格失败: {e}")
            return None
    
    def parse_table_lines(self, table_lines: List[str]) -> tuple[List[str], List[List[str]]]:
        """
        解析表格行内容
        
        Args:
            table_lines: 表格行列表
            
        Returns:
            tuple[List[str], List[List[str]]]: 表头和数据行
        """
        if len(table_lines) < 2:
            return [], []
        
        # 第一行是表头
        header_line = table_lines[0]
        headers = [cell.strip() for cell in header_line.split("|")[1:-1]]
        
        # 跳过分隔行（第二行）
        data_lines = table_lines[2:] if len(table_lines) > 2 else []
        
        # 解析数据行
        rows = []
        for line in data_lines:
            if line.strip() and line.strip().startswith("|"):
                row = [cell.strip() for cell in line.split("|")[1:-1]]
                if len(row) == len(headers):
                    rows.append(row)
        
        return headers, rows
    
    async def enhance_tables(self, tables: List[TableData]) -> List[TableData]:
        """
        使用Mock LLM增强表格数据
        
        Args:
            tables: 原始表格列表
            
        Returns:
            List[TableData]: 增强后的表格列表
        """
        # 创建所有表格的异步任务
        tasks = [self.enhance_single_table(table) for table in tables]
        
        # 使用asyncio.gather并发执行
        enhanced_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果，过滤掉异常
        enhanced_tables = []
        for i, result in enumerate(enhanced_results):
            if isinstance(result, Exception):
                print(f"⚠️ [Table] 表格 {i+1} 处理失败: {result}")
                # 保留原始表格
                enhanced_tables.append(tables[i])
            else:
                enhanced_tables.append(result)
        
        return enhanced_tables
    
    async def enhance_single_table(self, table: TableData) -> TableData:
        """
        增强单个表格
        
        Args:
            table: 表格对象
            
        Returns:
            TableData: 增强后的表格
        """
        try:
            # 构建增强提示词
            prompt = f"""
请分析以下表格数据并提供解读：

## 表格标题
{table.title}

## 表格结构
表头: {', '.join(table.headers)}
行数: {len(table.rows)}

## 表格数据
{self.format_table_for_prompt(table)}

请提供数据分析和关键发现。
            """.strip()
            
            # 异步调用Mock LLM
            response = await self.llm_manager.invoke_with_retry(prompt)
            
            # 应用增强
            table.interpretation = response.strip()
            return table
            
        except Exception as e:
            print(f"⚠️ [Table] LLM增强失败: {e}")
            return table
    
    def format_table_for_prompt(self, table: TableData) -> str:
        """格式化表格用于提示词"""
        if not table.headers or not table.rows:
            return "表格数据不完整"
        
        formatted = "| " + " | ".join(table.headers) + " |\n"
        formatted += "| " + " | ".join(["---"] * len(table.headers)) + " |\n"
        
        for row in table.rows:
            formatted += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        
        return formatted


class ReportGenerator(Runnable):
    """
    报告生成器 - 实现Runnable接口
    
    基于理论和表格数据生成分析报告，使用Mock LLM。
    """
    
    def __init__(self, llm_manager):
        """初始化报告生成器"""
        self.llm_manager = llm_manager
    
    def invoke(self, inputs: Dict[str, Any], config: Any = None) -> str:
        """
        同步调用接口 - 符合LCEL Runnable标准
        
        Args:
            inputs: 输入参数字典，包含theory和tables键
            config: 配置参数（LCEL标准参数）
            
        Returns:
            str: 生成的报告内容
        """
        return asyncio.run(self.ainvoke(inputs, config))
    
    async def ainvoke(self, inputs: Dict[str, Any], config: Any = None) -> str:
        """
        异步调用接口 - 符合LCEL Runnable标准
        
        Args:
            inputs: 输入参数字典，包含theory和tables键
            config: 配置参数（LCEL标准参数）
            
        Returns:
            str: 生成的报告内容
        """
        # 检查输入内容
        theory_framework = inputs.get("theory", [])
        tables = inputs.get("tables", [])
        
        # 检查是否都为空
        if not theory_framework and not tables:
            return "⚠️ 警告：理论框架和表格数据都为空，无法生成有意义的分析报告。"
        
        # 构建提示词
        prompt = f"""
请基于以下信息生成一份详细的论文分析报告：

## 理论框架
{theory_framework if theory_framework else "暂无理论框架数据"}

## 表格数据
{tables if tables else "暂无表格数据"}

请生成一份结构清晰、内容详实的分析报告，包括：
1. 研究背景和目的
2. 主要理论观点
3. 数据分析和发现
4. 结论和建议

请使用Markdown格式，确保报告逻辑清晰、内容完整。
        """.strip()
        
        # 异步调用Mock LLM
        response = await self.llm_manager.invoke_with_retry(prompt)
        return response.strip()
