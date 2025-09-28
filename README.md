# Automotive Business Intelligence (ABI)

这个仓库提供了一个简单的汽车市场质量情报分析样例，用来验证“通过市场表现来推测产品问题并评估对策效果”的建模思路。示例中包含：

- 一份虚构的市场表现数据集，包含不同市场、车型在对策前后的销量、抱怨、满意度及质保成本等指标。
- 一组纯 Python 的分析函数，用于横向比较市场/车型、定位问题热点、以及计算对策实施前后的变化。
- 一个基础的机器学习模型示例（基于特征组合的抱怨率查表模型），用于验证建模可行性并输出 RMSE、R² 指标。
- 单元测试以及命令行报表脚本，帮助研究人员快速得到分析结果。

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

## 将本地修改推送到远程仓库

如果你在本地完成了分析函数或数据的修改，可以按照以下步骤将提交推送到远程 Git 仓库：

1. 查看当前仓库状态，确认需要提交的文件：

   ```bash
   git status
   ```

2. 将修改添加到暂存区并创建提交：

   ```bash
   git add <文件或目录>
   git commit -m "描述此次修改的提交信息"
   ```

3. 如果尚未配置远程仓库地址，可以使用 `git remote add` 命令进行配置。例如：

   ```bash
   git remote add origin https://github.com/your-org/abi.git
   ```

4. 推送到远程仓库的指定分支（如 `main` 或 `work`）：

   ```bash
   git push origin <分支名>
   ```

遵循以上步骤即可将本地的 ABI 分析改动同步到远程仓库，便于团队协作和代码备份。

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
