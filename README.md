# 通用 AI Agent 自动化框架模板

这是一个轻量级 AI Agent 项目框架模板，用于展示如何把“任务理解、任务拆解、执行规划、风险评估、结果生成、Token 成本控制”串联成一个可复现的 Agent 工作流。

本模板不绑定具体业务项目名称，适合用于申报、比赛、评估表单或 GitHub 展示。你可以把它理解为一个通用的 Agent 框架骨架：输入任务描述，Agent 自动判断任务类型、拆解执行步骤、给出风险等级、生成建议输出，并保存为结构化 CSV。

## 项目目标

传统 AI 使用方式通常停留在单轮问答，缺少稳定的任务流和可验证输出。本项目将常见 Agent 流程抽象为一个可运行的模板，重点展示以下能力：

- 自动识别任务类型。
- 自动拆解任务执行链路。
- 自动生成 Agent 执行计划。
- 自动评估复杂度和风险。
- 自动输出结构化结果文件。
- 说明 Token plan 优化策略。

## 核心痛点

1. 复杂任务只靠聊天记录难以复盘。
2. 多步骤任务容易遗漏验证、日志和交付材料。
3. 长上下文任务会浪费 Token，影响稳定性。
4. 评估材料需要可解释、可复现、可上传的证据。

## Agent 工作流

```text
输入任务 CSV
  ->
任务理解 Agent：读取任务描述，判断任务类型
  ->
规划 Agent：拆解执行阶段和关键动作
  ->
风险评估 Agent：判断复杂度、风险等级和验证需求
  ->
执行建议 Agent：生成推荐输出格式和操作步骤
  ->
Token Plan Agent：给出上下文压缩与成本控制策略
  ->
生成 CSV 结果文件
```

## 目录结构

```text
agent_framework_template/
├── README.md
├── main.py
├── sample_tasks.csv
├── sample_submission.csv
├── 04_form_answer.txt
└── .gitignore
```

## 快速运行

```bash
python main.py --input sample_tasks.csv --output generated_submission.csv
```

运行后会生成：

```text
[+] Agent framework task planner
[+] Loaded tasks: 6
[+] Generated output: generated_submission.csv
```

## 输入格式

`sample_tasks.csv`

```csv
id,task_description,input_type,complexity_hint
1,整理一个 AI Agent 项目提交材料,document,medium
2,扫描代码仓库并生成重构计划,code,high
```

## 输出格式

`sample_submission.csv`

```csv
id,task_type,risk_level,agent_chain,recommended_output,token_plan,reason
1,submission_material,medium,Understanding->Planning->Writing->Review,README + form answer + evidence checklist,scan first; summarize stages; read on demand,matched keywords: 提交|材料
```

## Agent 模块说明

| 模块 | 作用 |
| --- | --- |
| Task Understanding Agent | 识别任务属于材料整理、代码分析、安全检查、数据处理或自动化运维 |
| Planning Agent | 将任务拆成可执行阶段 |
| Risk Agent | 根据复杂度和输入类型判断风险 |
| Output Agent | 推荐最终交付物 |
| Token Plan Agent | 给出上下文控制策略 |

## Token Plan 优化策略

- 先扫描目录或输入摘要，再读取关键内容。
- 对每个阶段生成短摘要，避免重复读取长上下文。
- 优先结构化输出 CSV、Markdown、JSON，便于复盘。
- 对高风险任务增加验证步骤，例如测试、日志、人工复核。
- 将 Agent 链路固定为模板，减少每次重新规划的 Token 消耗。

## 可用于表单第 04 项的描述

见 `04_form_answer.txt`。

## 可用于第 05 项的证明材料建议

建议上传以下材料：

1. 运行 `python main.py --input sample_tasks.csv --output generated_submission.csv` 的终端截图。
2. GitHub 仓库主页截图，展示 README、代码和样例 CSV。
3. `generated_submission.csv` 结果截图。
4. 如果有 AI 平台使用记录，可补充近 30 天账单或 Token 用量截图。
5. 如果有录屏，可展示从输入任务到生成 CSV 的完整流程。

## 项目亮点

- 框架通用，不依赖具体业务项目。
- 文件结构轻量，便于上传 GitHub。
- 输出结构化，方便评审验证。
- 明确展示多 Agent 链路和 Token plan 思路。
- 可扩展到代码重构、安全分析、材料生成、数据处理等多类任务。

