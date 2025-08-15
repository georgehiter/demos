# 智能文本分析管道

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-orange.svg)](https://python.langchain.com/docs/expression_language/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/text-pipeline)
[![Version](https://img.shields.io/badge/Version-V1.0.0-blue.svg)](https://github.com/yourusername/text-pipeline/releases)

这是一个基于LangChain LCEL（LangChain Expression Language）的智能文本分析工具，采用串行管道设计，支持真实的LLM调用。

## 🎯 项目目标

- 展示LCEL的核心设计理念和管道组合能力
- 演示**并行处理管道**（理论提取 + 表格提取同时执行 → 报告生成）
- 展示类型安全的管道构建和Runnable接口实现
- 提供可运行的代码示例，支持真实LLM调用
- 提供渐进式学习路径，从基础LLM调用到复杂LCEL并行管道
- 展示多种LLM集成方式，满足不同技术需求
- 突出并行处理在提升性能和资源利用率方面的优势

## 🏗️ 架构设计

### 核心组件

1. **TongyiLLMManager** - 通义千问LLM管理器，提供真实的LLM调用
2. **TheoryExtractor** - 理论框架提取器，提取文本中的理论内容
3. **TableExtractor** - 表格数据提取器，解析Markdown表格，支持并行LLM处理
4. **ReportGenerator** - 分析报告生成器，综合前序结果生成报告

### LCEL管道架构

#### 并行处理管道（当前实现）

```python
# 并行处理管道 - 理论提取和表格提取同时执行
pipeline = RunnableParallel({
    "theory": TheoryExtractor(llm_manager), 
    "tables": TableExtractor(llm_manager)
}) | RunnablePassthrough.assign(report=ReportGenerator(llm_manager))
```

**并行优势**：
- 🚀 **性能提升**：理论提取和表格提取同时进行，减少总执行时间
- 🔄 **资源利用**：充分利用多核CPU和并发能力
- 📊 **效率优化**：适合处理大量文本和复杂表格数据

#### 串行处理管道（可选实现）

```python
# 串行处理管道 - 顺序执行各组件
serial_pipeline = (
    RunnableLambda(lambda x: {"content": x["content"]})
    | RunnablePassthrough.assign(theory=TheoryExtractor())
    | RunnablePassthrough.assign(tables=TableExtractor())
    | RunnablePassthrough.assign(report=ReportGenerator(llm_manager))
    | RunnableLambda(lambda x: {
        "theory": x["theory"]["content"],
        "tables": x["tables"]["content"],
        "report": x["report"]["content"],
    })
)
```

**串行优势**：
- 🎯 **顺序依赖**：适合有明确依赖关系的处理流程
- 🧠 **内存友好**：减少内存占用，适合资源受限环境
- 🔍 **调试简单**：便于跟踪和调试处理流程

## 🚀 快速开始

[![Quick Start](https://img.shields.io/badge/Quick%20Start-Easy-brightgreen.svg)](https://github.com/yourusername/text-pipeline)

### 环境要求

- Python 3.9+
- 通义千问API密钥（DASHSCOPE_API_KEY）

### 安装依赖

#### 使用Poetry（推荐）
```bash
# 在项目根目录下
poetry install
```

#### 使用pip
```bash
# 在项目根目录下
pip install -r requirements.txt
```

### 环境变量配置

#### 方法一：使用模板文件（推荐）

1. 复制环境变量模板文件：
```bash
cp env.template .env
```

2. 编辑 `.env` 文件，填入您的通义千问API密钥：
```bash
# .env
DASHSCOPE_API_KEY=your_actual_api_key_here
```

#### 方法二：手动创建

创建 `.env` 文件并添加以下内容：
```bash
# .env
DASHSCOPE_API_KEY=your_actual_api_key_here
```

#### 获取API密钥

1. 访问 [通义千问控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 创建API密钥
4. 复制密钥到 `.env` 文件

### 运行演示

#### 主程序运行
```bash
# 基本运行
python text_pipeline/main.py

# 或者使用Poetry
poetry run python text_pipeline/main.py
```

#### 示例程序运行
```bash
# 基础LLM调用示例
python utils/llm_tongyi.py

# 原生API调用示例
python utils/llm_dashscope.py

# 链式调用示例
python utils/demo_pipeline.py
```

**注意**：运行示例程序前请确保已设置 `DASHSCOPE_API_KEY` 环境变量

## 📋 项目结构

[![Structure](https://img.shields.io/badge/Structure-Organized-brightgreen.svg)](https://github.com/yourusername/text-pipeline)
[![Architecture](https://img.shields.io/badge/Architecture-Modular-blue.svg)](https://github.com/yourusername/text-pipeline)

```
demos/                       # 项目根目录
├── text_pipeline/           # 主包目录
│   ├── __init__.py         # 包初始化文件
│   ├── main.py             # 主程序入口
│   ├── pipeline.py         # LCEL并行管道定义
│   ├── components.py       # 核心LCEL组件
│   └── llm_manager.py      # 通义千问LLM管理器
│
├── utils/                   # 示例和教程目录
│   ├── demo_pipeline.py    # LangChain链式调用示例
│   ├── llm_dashscope.py    # 原生DashScope API示例
│   └── llm_tongyi.py      # 简化LLM调用器示例
│
├── sample_data.md           # 示例数据文件
├── results.md               # 结果输出文件
├── env.template             # 环境变量配置模板
├── pyproject.toml           # Poetry项目配置
├── poetry.lock              # Poetry依赖锁定文件
├── requirements.txt          # pip依赖列表
├── .python-version          # Python版本配置
├── LICENSE                  # MIT许可证文件
├── .gitignore               # Git忽略文件
└── README.md                # 本文档
```

**目录说明**：
- 📁 **`text_pipeline/`** - 核心LCEL并行管道实现
- 📁 **`utils/`** - 学习示例和教程代码
- 📄 **`sample_data.md`** - 预定义的测试数据
- 📄 **`results.md`** - 管道执行结果示例
- ⚙️ **配置文件** - Poetry、Python版本、环境变量等配置

## 🔧 核心特性

[![Features](https://img.shields.io/badge/Features-Advanced-yellow.svg)](https://github.com/yourusername/text-pipeline)
[![AI](https://img.shields.io/badge/AI-Powered-red.svg)](https://github.com/yourusername/text-pipeline)
[![Parallel](https://img.shields.io/badge/Parallel-Processing-blue.svg)](https://github.com/yourusername/text-pipeline)

### 1. 并行处理架构 🚀
- **并行执行**：理论提取和表格提取同时进行，提升处理效率
- **智能调度**：使用`RunnableParallel`实现真正的并行处理
- **资源优化**：充分利用多核CPU和并发能力
- **混合模式**：并行提取 + 串行报告生成，平衡性能和依赖关系

### 2. 真实LLM集成
- 集成通义千问3.5B模型
- 支持环境变量配置API密钥
- 提供错误处理和异常管理

### 3. 类型安全
- 使用`TypedDict`定义输入输出类型
- 明确的类型契约和接口定义
- 提高代码可读性和维护性

### 4. 模块化组件
- 所有组件实现`Runnable`接口
- 支持独立测试和重用
- 清晰的职责分离

### 5. 并行处理优势 📊
- **性能提升**：理论提取和表格提取并行执行，减少总处理时间
- **资源利用**：充分利用系统并发能力，提高CPU利用率
- **扩展性**：支持添加更多并行组件，轻松扩展处理能力
- **灵活性**：可根据需求选择并行或串行处理模式

## 📚 示例和教程

[![Examples](https://img.shields.io/badge/Examples-Tutorials-purple.svg)](https://github.com/yourusername/text-pipeline)
[![Learning](https://img.shields.io/badge/Learning-Guides-blue.svg)](https://github.com/yourusername/text-pipeline)

项目提供了丰富的示例和教程，帮助您从不同角度理解LLM集成：

### 🎯 学习路径

**初学者** → **进阶用户** → **高级开发者**

1. **基础入门** (`utils/llm_tongyi.py`)
   - 最简单的LLM调用方式
   - 基于LangChain的Tongyi类
   - 适合快速上手和测试

2. **原生API** (`utils/llm_dashscope.py`)
   - 直接使用DashScope API
   - 不依赖LangChain框架
   - 更轻量级，性能更好

3. **链式调用** (`utils/demo_pipeline.py`)
   - LangChain链式操作示例
   - 包含详细的环境配置说明
   - 适合学习LangChain概念

4. **完整管道** (`text_pipeline/`)
   - 基于LCEL的**并行处理**智能分析管道
   - 生产级别的架构设计，支持并行执行
   - 完整的理论提取和分析流程，性能优化

### 🔧 技术栈对比

| 实现方式 | 复杂度 | 性能 | 灵活性 | 学习价值 | 并行能力 |
|---------|--------|------|--------|----------|----------|
| 简化调用器 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ❌ |
| 原生API | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ |
| 链式调用 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ |
| LCEL串行管道 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| **LCEL并行管道** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |

## 🔍 代码示例

### 使用并行处理管道

```python
from pipeline import create_analysis_pipeline

# 创建并行分析管道
pipeline = create_analysis_pipeline()

# 执行管道 - 理论提取和表格提取并行执行
result = pipeline.invoke({"content": "您的文本内容"})

# 获取并行处理结果
theory = result["theory"]      # 理论提取结果
tables = result["tables"]      # 表格提取结果  
report = result["report"]      # 基于并行结果生成的报告
```

**并行执行流程**：
1. 🚀 **并行阶段**：`TheoryExtractor` 和 `TableExtractor` 同时启动
2. ⏳ **等待完成**：等待两个并行任务都完成
3. 📝 **串行生成**：`ReportGenerator` 基于并行结果生成最终报告

### 使用单个组件

```python
from components import TheoryExtractor, TableExtractor
from llm_manager import TongyiLLMManager

# 创建LLM管理器
llm_manager = TongyiLLMManager()

# 创建理论提取器
theory_extractor = TheoryExtractor()
theory_result = theory_extractor.invoke({"content": "理论文本"})

# 创建表格提取器
table_extractor = TableExtractor()
table_result = table_extractor.invoke({"content": "表格数据"})
```

### 自定义并行管道

```python
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel

# 创建自定义并行管道
custom_parallel_pipeline = (
    RunnableParallel({
        "theory": TheoryExtractor(),
        "tables": TableExtractor(),
        "custom_analysis": CustomAnalyzer()  # 可以添加更多并行组件
    })
    | RunnableLambda(lambda x: {
        "summary": f"理论: {x['theory']['content']}, 表格: {x['tables']['content']}, 分析: {x['custom_analysis']['content']}"
    })
)

# 创建混合管道（部分并行，部分串行）
hybrid_pipeline = (
    RunnableParallel({
        "theory": TheoryExtractor(),
        "tables": TableExtractor()
    })
    | RunnablePassthrough.assign(
        summary=SummaryGenerator(),
        report=ReportGenerator()
    )
)
```

**并行管道设计模式**：
- 🚀 **完全并行**：使用 `RunnableParallel` 同时执行多个独立任务
- 🔄 **混合模式**：并行执行 + 串行后处理，平衡性能和依赖关系
- 📈 **可扩展性**：轻松添加新的并行组件，提升处理能力

## 🧪 测试数据

项目包含预定义的示例数据，涵盖：

### 理论文本
- 社会懈怠理论（Social Loafing Theory）
- 组织行为学相关概念
- 适合LCEL处理的文本长度

### 表格数据
- Markdown格式的表格
- 包含数值和文本数据
- 支持表格提取器处理

### 数据获取

```python
# 示例数据直接读取 sample_data.md 文件

# 读取示例数据文件
with open("sample_data.md", "r", encoding="utf-8") as f:
    full_data = f.read()
```

## 📊 性能特点

- **LLM调用**: 使用通义千问3.5B模型
- **处理方式**: 并行 + 串行混合处理
- **并行能力**: 理论提取和表格提取同时执行
- **内存使用**: 轻量级设计，支持并发处理
- **执行流程**: 并行提取 → 串行报告生成
- **性能提升**: 相比串行处理，可显著减少总执行时间

## 🔧 技术细节

### 依赖版本
- `langchain>=0.3.27,<0.4.0`
- `langchain-core>=0.3.0,<0.4.0`
- `langchain-community>=0.3.0,<0.4.0`
- `dashscope>=1.24.1,<2.0.0`
- `python-dotenv>=1.1.1,<2.0.0`

### 模型配置
- 模型: `qwen3-235b-a22b-instruct-2507`
- 温度: 0.2
- 最大token: 2000

## 🚨 注意事项

1. **API密钥**: 必须设置`DASHSCOPE_API_KEY`环境变量
2. **网络连接**: 需要稳定的网络连接访问通义千问API
3. **API限制**: 注意通义千问API的调用频率和配额限制
4. **错误处理**: 程序包含基本的错误处理，但建议在生产环境中增强
5. **数据安全**: 示例数据仅用于演示，生产环境请使用真实数据
6. **环境变量**: 确保`.env`文件已添加到`.gitignore`中，避免提交敏感信息

## 🤝 贡献指南

欢迎贡献代码和改进建议：

1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 开发规范
- 保持代码简洁性和可读性
- 遵循LCEL最佳实践
- 确保类型安全
- 添加适当的文档和注释

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   ```
   ValueError: 未设置环境变量 DASHSCOPE_API_KEY
   ```
   解决：检查`.env`文件中的API密钥设置

2. **网络连接问题**
   ```
   ❌ 通义千问LLM调用失败: [网络错误]
   ```
   解决：检查网络连接和防火墙设置

3. **依赖安装问题**
   ```
   ModuleNotFoundError: No module named 'langchain'
   ```
   解决：重新安装依赖 `pip install -r requirements.txt`

4. **环境变量问题**
   ```
   ModuleNotFoundError: No module named 'dotenv'
   ```
   解决：安装python-dotenv `pip install python-dotenv`

5. **示例程序运行问题**
   ```
   ModuleNotFoundError: No module named 'dashscope'
   ```
   解决：安装dashscope `pip install dashscope`

6. **LangChain导入问题**
   ```
   ModuleNotFoundError: No module named 'langchain'
   ```
   解决：安装langchain `pip install langchain langchain-core langchain-community`

## 📚 学习资源

### 官方文档
- [LangChain LCEL文档](https://python.langchain.com/docs/expression_language/)
- [LangChain Core文档](https://python.langchain.com/docs/core/)
- [通义千问API文档](https://help.aliyun.com/zh/dashscope/)
- [Python类型提示文档](https://docs.python.org/3/library/typing.html)

### 项目示例
- **基础入门**：`utils/llm_tongyi.py` - 最简单的LLM调用
- **原生API**：`utils/llm_dashscope.py` - 直接API调用
- **链式操作**：`utils/demo_pipeline.py` - LangChain链式调用
- **完整管道**：`text_pipeline/` - LCEL智能分析管道

### 学习建议
1. 从 `utils/llm_tongyi.py` 开始，理解基本的LLM调用
2. 尝试 `utils/llm_dashscope.py`，了解原生API的使用
3. 学习 `utils/demo_pipeline.py`，掌握LangChain概念
4. 最后深入 `text_pipeline/`，理解**LCEL并行管道架构**和性能优化策略

## 📄 许可证

本项目遵循MIT许可证。

---

**注意**: 这是一个演示程序，展示了LCEL的**并行处理能力**和真实LLM集成，适合学习和理解LCEL并行管道架构概念。
