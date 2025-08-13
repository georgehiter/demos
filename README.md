# LCEL演示程序

这是一个展示LangChain LCEL（LangChain Expression Language）核心特性的简化演示程序。

## 🎯 项目目标

- 展示LCEL的核心设计理念
- 演示异步并行处理能力
- 展示管道组合和类型安全
- 提供可运行的代码示例

## 🏗️ 架构设计

### 核心组件

1. **MockLLMManager** - 模拟LLM调用行为
2. **TheoryExtractor** - 理论框架提取器
3. **TableExtractor** - 表格数据提取器
4. **ReportGenerator** - 分析报告生成器

### LCEL管道

```python
# 并行处理阶段
parallel_pipeline = RunnableParallel({
    "theory": theory_extractor,
    "tables": table_extractor,
})

# 串行聚合阶段
final_pipeline = (
    parallel_pipeline 
    | report_generator 
    | StrOutputParser()
)
```

## 🚀 快速开始

### 安装依赖

```bash
cd demos
poetry install
```

**注意**: 确保已安装Poetry。如果未安装，请先运行 `pip install poetry`

### 运行演示

#### 1. 管道构建演示
```bash
poetry run python run_demo.py --pipeline-only
```

#### 2. 异步处理演示（默认）
```bash
poetry run python run_demo.py
```

#### 3. 同步处理演示
```bash
poetry run python run_demo.py --sync
```

#### 4. 详细模式演示
```bash
poetry run python run_demo.py --verbose
```

#### 5. 使用简化数据
```bash
poetry run python run_demo.py --simple
```

## 📋 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--sync` | 使用同步模式 | 异步模式 |
| `--simple` | 使用简化数据 | 完整数据 |
| `--pipeline-only` | 仅演示管道构建 | 完整演示 |
| `--verbose`, `-v` | 显示详细输出 | 简洁输出 |

## 🔧 核心特性

### 1. 异步优先设计
- 所有组件都实现`Runnable`接口
- 支持`ainvoke`和`invoke`方法
- 真正的异步并发处理

### 2. 管道组合
- 使用`|`操作符组合组件
- 支持并行和串行处理
- 类型安全的管道构建

### 3. 并行处理
- `RunnableParallel`实现真正的并行
- 理论和表格提取同时进行
- 异步并发控制

### 4. 类型安全
- 使用`TypedDict`定义输入输出类型
- 明确的类型契约
- 提高代码可读性和安全性

## 📁 文件结构

```
demos/
├── __init__.py              # 包初始化文件
├── requirements.txt          # 依赖列表
├── mock_llm.py             # Mock LLM实现
├── lcel_components.py      # 核心LCEL组件
├── demo_pipeline.py        # LCEL管道演示
├── sample_data.py          # 示例数据
├── run_demo.py             # 主程序入口
└── README.md               # 本文档
```

## 🔍 代码示例

### 创建自定义管道

```python
from demo_pipeline import create_custom_pipeline
from lcel_components import TheoryExtractor, ReportGenerator

# 创建自定义管道
custom_pipeline = create_custom_pipeline(
    TheoryExtractor(llm_manager),
    ReportGenerator(llm_manager)
)

# 执行管道
result = await custom_pipeline.ainvoke({"content": "理论文本"})
```

### 使用单个组件

```python
from lcel_components import TheoryExtractor

# 创建理论提取器
extractor = TheoryExtractor(llm_manager)

# 异步调用
theory = await extractor.ainvoke({"content": "理论文本"})

# 同步调用
theory = extractor.invoke({"content": "理论文本"})
```

## 🧪 测试数据

### 理论文本
- 社会懈怠理论（Social Loafing Theory）
- 组织行为学相关概念
- 适合LCEL处理的文本长度

### 表格数据
- Markdown格式的表格
- 包含数值和文本数据
- 支持表格提取器处理

## 📊 性能特点

- **Mock LLM延迟**: 100ms（可配置）
- **最大并发调用**: 3个（硬编码）
- **异步处理**: 真正的非阻塞处理
- **内存使用**: 轻量级设计

## 🔧 技术细节

### 依赖版本
- 使用Poetry管理依赖
- 具体版本请查看`pyproject.toml`文件
- 主要依赖包括langchain、langchain-core、langchain-community等

### 硬编码参数
- 最大并发调用数: 3
- Mock延迟: 0.1秒
- 重试次数: 1次

## 🚨 注意事项

1. **Mock LLM**: 这是一个演示程序，使用模拟的LLM响应
2. **硬编码配置**: 所有配置参数都硬编码在代码中
3. **简化实现**: 相比原项目，移除了复杂的错误处理和监控
4. **示例数据**: 使用预定义的示例数据，不支持外部文件输入

## 🤝 贡献指南

这是一个演示项目，主要用于学习和理解LCEL概念。如需改进：

1. 保持代码简洁性
2. 遵循LCEL最佳实践
3. 确保异步兼容性
4. 维护类型安全

## 📚 学习资源

- [LangChain LCEL文档](https://python.langchain.com/docs/expression_language/)
- [LangChain Core文档](https://python.langchain.com/docs/core/)
- [异步编程最佳实践](https://docs.python.org/3/library/asyncio.html)

## 📄 许可证

本项目遵循与原项目相同的许可证。

---

**注意**: 这是一个演示程序，展示了LCEL的核心特性，但不包含完整的生产环境功能。

