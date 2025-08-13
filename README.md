# LCEL演示程序

这是一个展示LangChain LCEL（LangChain Expression Language）核心特性的演示程序，采用串行管道设计，支持真实的LLM调用。

## 🎯 项目目标

- 展示LCEL的核心设计理念和管道组合能力
- 演示串行管道处理流程（理论提取 → 表格提取 → 报告生成）
- 展示类型安全的管道构建和Runnable接口实现
- 提供可运行的代码示例，支持真实LLM调用

## 🏗️ 架构设计

### 核心组件

1. **TongyiLLMManager** - 通义千问LLM管理器，提供真实的LLM调用
2. **TheoryExtractor** - 理论框架提取器，提取文本中的理论内容
3. **TableExtractor** - 表格数据提取器，解析Markdown表格
4. **ReportGenerator** - 分析报告生成器，综合前序结果生成报告

### LCEL管道

```python
# 串行处理管道
final_pipeline = (
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

## 🚀 快速开始

### 环境要求

- Python 3.9+
- 通义千问API密钥（DASHSCOPE_API_KEY）

### 安装依赖

#### 使用Poetry（推荐）
```bash
cd demos
poetry install
```

#### 使用pip
```bash
cd demos
pip install -r requirements.txt
```

### 配置环境变量

创建`.env`文件并添加您的通义千问API密钥：

```bash
# .env
DASHSCOPE_API_KEY=your_api_key_here
```

### 运行演示

```bash
# 基本运行
python run_demo.py

# 或者使用Poetry
poetry run python run_demo.py
```

## 📋 项目结构

```
demos/
├── __init__.py              # 包初始化文件
├── pyproject.toml           # Poetry项目配置
├── requirements.txt          # pip依赖列表
├── tongyi_llm.py           # 通义千问LLM管理器
├── lcel_components.py      # 核心LCEL组件
├── demo_pipeline.py        # LCEL管道定义
├── sample_data.py          # 示例数据
├── run_demo.py             # 主程序入口
└── README.md               # 本文档
```

## 🔧 核心特性

### 1. 串行管道设计
- 理论提取 → 表格提取 → 报告生成
- 使用`RunnablePassthrough.assign`进行数据传递
- 支持中间结果的累积和传递

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

## 🔍 代码示例

### 使用完整管道

```python
from demo_pipeline import create_analysis_pipeline

# 创建分析管道
pipeline = create_analysis_pipeline()

# 执行管道
result = pipeline.invoke({"content": "您的文本内容"})

# 获取结果
theory = result["theory"]
tables = result["tables"]
report = result["report"]
```

### 使用单个组件

```python
from lcel_components import TheoryExtractor, TableExtractor
from tongyi_llm import TongyiLLMManager

# 创建LLM管理器
llm_manager = TongyiLLMManager()

# 创建理论提取器
theory_extractor = TheoryExtractor()
theory_result = theory_extractor.invoke({"content": "理论文本"})

# 创建表格提取器
table_extractor = TableExtractor()
table_result = table_extractor.invoke({"content": "表格数据"})
```

### 自定义管道

```python
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# 创建自定义管道
custom_pipeline = (
    RunnablePassthrough.assign(
        theory=TheoryExtractor(),
        tables=TableExtractor()
    )
    | RunnableLambda(lambda x: {
        "summary": f"理论: {x['theory']['content']}, 表格: {x['tables']['content']}"
    })
)
```

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
from sample_data import get_sample_data, get_simple_data

# 获取完整示例数据
full_data = get_sample_data()

# 获取简化数据（用于快速测试）
simple_data = get_simple_data()
```

## 📊 性能特点

- **LLM调用**: 使用通义千问3.5B模型
- **处理方式**: 串行顺序处理
- **内存使用**: 轻量级设计
- **执行流程**: 理论提取 → 表格提取 → 报告生成

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

## 📚 学习资源

- [LangChain LCEL文档](https://python.langchain.com/docs/expression_language/)
- [LangChain Core文档](https://python.langchain.com/docs/core/)
- [通义千问API文档](https://help.aliyun.com/zh/dashscope/)
- [Python类型提示文档](https://docs.python.org/3/library/typing.html)

## 📄 许可证

本项目遵循MIT许可证。

---

**注意**: 这是一个演示程序，展示了LCEL的核心特性和真实LLM集成，适合学习和理解LCEL概念。

