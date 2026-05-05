import argparse
import csv
from pathlib import Path


TASK_RULES = [
    {
        "task_type": "submission_material",
        "keywords": ["提交", "材料", "表单", "README", "证明", "上传", "申报"],
        "agent_chain": "Understanding->Planning->Writing->Review",
        "recommended_output": "README + form answer + evidence checklist",
    },
    {
        "task_type": "code_analysis",
        "keywords": ["代码", "仓库", "重构", "测试", "PR", "脚本", "bug"],
        "agent_chain": "Scanner->Planner->Worker->Verifier->Reviewer",
        "recommended_output": "analysis report + patch plan + verification log",
    },
    {
        "task_type": "security_analysis",
        "keywords": ["安全", "漏洞", "日志", "异常", "攻击", "CTF", "审计"],
        "agent_chain": "Triage->Feature Extraction->Reasoning->Report",
        "recommended_output": "risk report + anomaly table + reproduction steps",
    },
    {
        "task_type": "data_processing",
        "keywords": ["数据", "CSV", "统计", "建模", "清洗", "预测", "指标"],
        "agent_chain": "Loader->Cleaner->Analyzer->Reporter",
        "recommended_output": "cleaned data + metrics table + summary report",
    },
    {
        "task_type": "automation_ops",
        "keywords": ["自动化", "部署", "运行", "监控", "日志", "CI", "流程"],
        "agent_chain": "Scheduler->Executor->Monitor->Notifier",
        "recommended_output": "automation script + run log + status report",
    },
]


DEFAULT_RULE = {
    "task_type": "general_agent_task",
    "agent_chain": "Understanding->Planning->Execution->Verification->Report",
    "recommended_output": "task plan + result report + verification notes",
}


def read_tasks(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def classify_task(description):
    matched = []
    for rule in TASK_RULES:
        hits = [keyword for keyword in rule["keywords"] if keyword.lower() in description.lower()]
        if hits:
            matched.append((len(hits), rule, hits))

    if not matched:
        return DEFAULT_RULE, []

    matched.sort(key=lambda item: item[0], reverse=True)
    _, rule, hits = matched[0]
    return rule, hits


def estimate_risk(input_type, complexity_hint, task_type):
    score = 0
    if input_type in {"code", "security", "system", "repo"}:
        score += 2
    elif input_type in {"document", "csv", "text"}:
        score += 1

    if complexity_hint == "high":
        score += 2
    elif complexity_hint == "medium":
        score += 1

    if task_type in {"security_analysis", "code_analysis"}:
        score += 1

    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    return "low"


def build_token_plan(risk_level):
    base = "scan first; summarize stages; read on demand"
    if risk_level == "high":
        return base + "; add verification checkpoint; keep rollback notes"
    if risk_level == "medium":
        return base + "; cache intermediate decisions"
    return base + "; use concise structured output"


def run_agent(input_path, output_path):
    rows = read_tasks(input_path)
    output_rows = []

    for index, row in enumerate(rows, start=1):
        task_id = row.get("id") or str(index)
        description = row.get("task_description", "")
        input_type = row.get("input_type", "text").lower()
        complexity_hint = row.get("complexity_hint", "medium").lower()

        rule, hits = classify_task(description)
        risk_level = estimate_risk(input_type, complexity_hint, rule["task_type"])
        token_plan = build_token_plan(risk_level)
        reason = "matched keywords: " + "|".join(hits) if hits else "default general Agent workflow"

        output_rows.append(
            {
                "id": task_id,
                "task_type": rule["task_type"],
                "risk_level": risk_level,
                "agent_chain": rule["agent_chain"],
                "recommended_output": rule["recommended_output"],
                "token_plan": token_plan,
                "reason": reason,
            }
        )

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        fieldnames = [
            "id",
            "task_type",
            "risk_level",
            "agent_chain",
            "recommended_output",
            "token_plan",
            "reason",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print("[+] Agent framework task planner")
    print(f"[+] Loaded tasks: {len(rows)}")
    print(f"[+] Generated output: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generic AI Agent Framework Template")
    parser.add_argument("--input", default="sample_tasks.csv", help="Input CSV path")
    parser.add_argument("--output", default="generated_submission.csv", help="Output CSV path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    run_agent(input_path, args.output)


if __name__ == "__main__":
    main()

