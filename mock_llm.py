"""
Mock LLM管理器 - 模拟真实的LLM调用行为

提供预定义的响应模板，支持异步调用，用于LCEL演示程序。
"""

import asyncio
import time
from typing import Dict, List, Any


class MockLLMManager:
    """
    Mock LLM管理器 - 模拟真实的LLM调用行为

    硬编码参数：
    - max_concurrent_calls: 3
    - mock_delay: 0.1秒
    """

    def __init__(self):
        """初始化Mock LLM管理器"""
        self.max_concurrent_calls = 3
        self.mock_delay = 0.1
        self._semaphore = asyncio.Semaphore(self.max_concurrent_calls)
        self._call_count = 0

        # 预定义的响应模板
        self._response_templates = {
            "theory_extraction": {
                "研究背景": [
                    "基于现有研究，该理论探讨了...",
                    "在相关领域，学者们发现...",
                ],
                "核心假设": ["主要假设包括...", "理论基于以下假设..."],
                "研究方法": ["采用定量分析方法", "结合定性和定量研究"],
                "主要发现": ["研究发现支持了理论假设", "数据表明理论模型有效"],
                "结论": [
                    "该理论为相关研究提供了新视角",
                    "研究结果具有重要的理论和实践意义",
                ],
            },
            "table_enhancement": {
                "interpretation": "该表格显示了重要的数据趋势，支持了研究假设。",
                "key_findings": "数据表明存在显著的相关性，p值小于0.05。",
                "implications": "这些发现对理论发展具有重要意义。",
            },
            "report_generation": {
                "summary": "基于理论分析和表格数据，本研究得出以下结论：",
                "background": "研究背景清晰，理论基础扎实。",
                "methodology": "研究方法科学，数据分析合理。",
                "results": "研究结果支持了理论假设。",
                "conclusion": "研究结论具有重要的理论和实践意义。",
            },
        }

    async def invoke_with_retry(self, prompt: str, max_retries: int = 1) -> str:
        """
        异步调用Mock LLM，支持重试机制

        Args:
            prompt: 输入提示词
            max_retries: 最大重试次数（硬编码为1）

        Returns:
            str: 模拟的LLM响应
        """
        async with self._semaphore:
            self._call_count += 1
            call_id = self._call_count

            # 模拟网络延迟
            await asyncio.sleep(self.mock_delay)

            # 根据提示词类型返回相应的响应
            response = self._generate_response(prompt)

            return response

    def _generate_response(self, prompt: str) -> str:
        """
        根据提示词生成响应

        Args:
            prompt: 输入提示词

        Returns:
            str: 生成的响应
        """
        prompt_lower = prompt.lower()

        if "理论" in prompt_lower or "theory" in prompt_lower:
            return self._format_theory_response()
        elif "表格" in prompt_lower or "table" in prompt_lower:
            return self._format_table_response()
        elif "报告" in prompt_lower or "report" in prompt_lower:
            return self._format_report_response()
        else:
            return "这是一个通用的Mock LLM响应，用于演示LCEL功能。"

    def _format_theory_response(self) -> str:
        """格式化理论提取响应"""
        template = self._response_templates["theory_extraction"]

        response = "## 理论框架分析\n\n"
        for section, content in template.items():
            response += f"### {section}\n"
            for item in content:
                response += f"- {item}\n"
            response += "\n"

        return response

    def _format_table_response(self) -> str:
        """格式化表格增强响应"""
        template = self._response_templates["table_enhancement"]

        response = "## 表格数据分析\n\n"
        for key, value in template.items():
            response += f"**{key.title()}**: {value}\n\n"

        return response

    def _format_report_response(self) -> str:
        """格式化报告生成响应"""
        template = self._response_templates["report_generation"]

        response = "# 分析报告\n\n"
        for section, content in template.items():
            response += f"## {section.title()}\n{content}\n\n"

        return response

    async def batch_invoke(self, prompts: List[str]) -> List[str]:
        """
        批量异步调用Mock LLM

        Args:
            prompts: 提示词列表

        Returns:
            List[str]: 响应列表
        """
        tasks = [self.invoke_with_retry(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(f"[处理失败] {prompts[i][:50]}...")
            else:
                processed_results.append(result)

        return processed_results

    def get_stats(self) -> Dict[str, Any]:
        """获取Mock LLM统计信息"""
        return {
            "type": "MockLLMManager",
            "max_concurrent_calls": self.max_concurrent_calls,
            "mock_delay": self.mock_delay,
            "total_calls": self._call_count,
            "current_available": self._semaphore._value,
        }
