# Automotive Business Intelligence (ABI)

这个仓库提供了一个简单的汽车市场质量情报分析样例，用来验证“通过市场表现来推测产品问题并评估对策效果”的建模思路。示例中包含：

- 一份虚构的市场表现数据集，包含不同市场、车型在对策前后的销量、抱怨、满意度及质保成本等指标。
- 一组纯 Python 的分析函数，用于横向比较市场/车型、定位问题热点、以及计算对策实施前后的变化。
- 一个基础的机器学习模型示例（基于特征组合的抱怨率查表模型），用于验证建模可行性并输出 RMSE、R² 指标。
- 单元测试以及命令行报表脚本，帮助研究人员快速得到分析结果。

此外，`docs/dynamic_tool_agent_system.md` 描述了一个可自我进化的动态工具代理系统的项目说明与架构设计，可作为扩展智能分析能力的长期规划参考。

## 快速开始

1. 创建虚拟环境并安装测试依赖（可选，项目本身只依赖 Python 标准库）：

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install pytest
   ```

2. 运行分析报表：

   ```bash
   python -m src.report
   ```

   报表会输出市场/车型对比、问题热点、对策效果以及抱怨率模型的评估指标。

3. 运行测试：

   ```bash
   pytest
   ```

## 项目结构

```
├── data
│   └── sample_market_performance.csv  # 虚构示例数据
├── src
│   ├── analysis.py                    # 市场与对策分析函数
│   ├── data_loader.py                 # 数据加载与预处理
│   ├── modeling.py                    # 抱怨率预测模型（查表法）
│   └── report.py                      # 命令行分析报表
└── tests
    ├── test_analysis.py               # 分析函数单元测试
    └── test_modeling.py               # 模型训练测试
```

可以基于此示例扩展真实的数据源、指标体系与模型，以支撑日常的市场质量诊断工作。
