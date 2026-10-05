Here is the complete, self-contained solution for Part 4 — Agentic Workflow Spec & Mock Agent Runner, fully adhering to all specifications and acceptance criteria outlined in the project requirements.   Folder & File Structure for Part 4Ensure your repository contains the following files in part4_agent/:   Plaintextmeesho-growth-pipeline/
└── part4_agent/
    ├── agent_spec.md
    └── mock_agent_runner.py
Step 1: Agent Specification (part4_agent/agent_spec.md)Create part4_agent/agent_spec.md with all five core architecture components, guardrails, failure modes, subtasks, schema descriptions, and Given-When-Then specifications:   Markdown# Part 4: Agentic Workflow Spec — Reseller Growth Monitoring Agent

## 4.1 Agent Architecture Components

- **Goal:** Keep Meesho category managers informed of any category whose month-on-month (MoM) revenue moves beyond the 8.0% threshold, with a human approving every message before it goes out[cite: 14].
- **Tools:**
  - `validate_feed(csv_path)`: Part 2 function verifying CSV schema and data types[cite: 14, 15].
  - `mom_growth(previous_revenue, current_revenue)`: Part 2 function computing signed percentage change[cite: 14, 15].
  - `is_flagged(mom_pct)`: Part 2 function returning `"flagged"`, `"not_flagged"`, or `"escalate_exact_boundary"`[cite: 14, 15].
  - Prompt-pack template-fill draft generator: Part 3 logic generating structured narrative messages[cite: 14, 15].
- **Memory / State:** Remembers the previous month's revenue per category to compute the next run's MoM growth metrics[cite: 14, 15].
- **Planner:** Ordered sequence of subtasks 1 through 8 detailed in Section 4.2[cite: 14, 15].
- **Feedback Loop:** Human-approval checkpoint where drafted messages are held with `action_taken = "drafted_and_held_for_approval"` before any delivery (simulated flag in output, no actual email/SMTP integration required)[cite: 14, 15, 16].

### System Guardrails:
1. **Input Guardrail:** `validate_feed` must pass (`True`) before any MoM or growth logic runs[cite: 15].
2. **Action Guardrail:** No message is ever auto-sent; all generated drafts are held for human review[cite: 15].
3. **Output Guardrail:** Every numeric figure in a drafted message must strictly trace back to Part 1 / Part 2 calculated numbers (zero hallucinated figures).

### Failure Handling:
- If `validate_feed` evaluates to `False`, the agent halts immediately in a **Hard Stop**, populating `validation_errors` with the exact error strings and setting `action_taken = "hard_stop"`[cite: 15, 16].

---

## 4.2 Ordered Subtasks (Planner Execution Sequence)

1. Load the monthly revenue feed CSV and execute `validate_feed`[cite: 15].
2. If invalid, **Hard Stop** immediately and report error strings[cite: 15].
3. If valid, compute `mom_growth` for every category against the previous month's baseline revenue[cite: 15].
4. Run `is_flagged` for every category against the 8.0% threshold[cite: 15].
5. Sort flagged categories descending by absolute growth magnitude `abs(mom_pct)`[cite: 15].
6. Draft template messages using Part 3's template logic for **at most the top 3** flagged categories by magnitude[cite: 15].
7. Log any remaining flagged categories beyond the top 3 cap into `suppressed_categories` as `"suppressed, review manually"` without drafting a message[cite: 15].
   - **Note (7b):** Categories with `is_flagged == "escalate_exact_boundary"` are logged into `escalated_categories`[cite: 15]. Categories with `is_flagged == "not_flagged"` are ignored and never placed in either suppressed or flagged lists[cite: 15].
8. Emit one structured JSON object per execution run containing complete execution telemetry[cite: 15, 16].

---

## 4.3 Specifications (Given-When-Then Format)

### Spec 1: Standard May Monitoring Run
- **GIVEN** valid April baseline revenue and valid May current revenue feeds[cite: 16].
- **WHEN** the agent runner executes for May[cite: 16].
- **THEN** `validation_status` is `"valid"`, `flagged_categories` contains exactly 3 drafted entries ordered by `abs(mom_pct)` descending (Ethnic Wear +77.1%, Western Wear -23.6%, Kids Wear -23.48%), `suppressed_categories` contains 2 categories (Beauty & Personal Care, Home & Kitchen), and `action_taken` is `"drafted_and_held_for_approval"`[cite: 16].

### Spec 2: Standard June Monitoring Run
- **GIVEN** valid May baseline revenue and valid June current revenue feeds[cite: 16].
- **WHEN** the agent runner executes for June[cite: 16].
- **THEN** `validation_status` is `"valid"`, `flagged_categories` contains exactly 3 drafted entries ordered by `abs(mom_pct)` descending (Ethnic Wear -58.74%, Home & Kitchen 42.59%, Kids Wear 23.9%), `suppressed_categories` contains Western Wear (11.97%), Beauty & Personal Care (5.67%) does not appear in either list, and `action_taken` is `"drafted_and_held_for_approval"`[cite: 16].

### Spec 3: Corrupted Input Data (Hard Stop)
- **GIVEN** `corrupted_feed.csv` provided as the current month input feed[cite: 10, 16].
- **WHEN** the agent runner executes validation[cite: 16].
- **THEN** `validation_status` is `"invalid"`, `action_taken` is `"hard_stop"`, `validation_errors` contains exactly the 3 validation error strings, and both `flagged_categories` and `suppressed_categories` are empty[cite: 10, 16].

### Spec 4: Exact Boundary Condition Handling
- **GIVEN** a revenue feed containing a category with exactly 8.0% growth[cite: 10, 16].
- **WHEN** the agent runner evaluates category flags[cite: 16].
- **THEN** `is_flagged` returns `"escalate_exact_boundary"` and the category is added to `escalated_categories` without drafting a message[cite: 10, 15, 16].
Step 2: Mock Agent Runner (part4_agent/mock_agent_runner.py)Create part4_agent/mock_agent_runner.py to execute subtasks 1–8 and output the compliant JSON schema[cite: 15, 16]:Pythonimport os
import sys
import json
import csv

# Import Part 2 growth engine functions un-modified
PART2_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "part2_engine"))
sys.path.append(PART2_DIR)

from growth_engine import validate_feed, mom_growth, is_flagged


def load_category_revenue(csv_path: str) -> dict[str, float]:
    """Helper function to load category revenue mapping from a validated CSV file."""
    revenue_map = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["category"].strip()
            rev = float(row["revenue"].strip())
            revenue_map[cat] = rev
    return revenue_map


def draft_message(category: str, mom_pct: float) -> str:
    """Drafts narrative message matching Part 3 requirements without external LLM calls."""
    sign = "+" if mom_pct > 0 else ""
    return (
        f"Category '{category}' recorded a MoM revenue shift of {sign}{mom_pct}%. "
        f"Context: Category performance evaluation. "
        f"Insight: Revenue shifted by {sign}{mom_pct}% (Fact). "
        f"Implication: Review category allocation and promotion strategies."
    )


def run(run_month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """
    Executes subtasks 1-8 of the monitoring agent and returns structured JSON output.
    """
    # Subtask 1 & 2: Validate input feed and handle Hard Stop
    is_valid, errors = validate_feed(current_month_csv)
    if not is_valid:
        return {
            "run_month": run_month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }

    # Load validated monthly revenue feeds
    prev_revenue = load_category_revenue(previous_month_csv)
    curr_revenue = load_category_revenue(current_month_csv)

    flagged_candidates = []
    escalated_categories = []

    # Subtasks 3, 4 & 7b: Compute growth, evaluate flags & handle exact boundaries
    for category, curr_rev in curr_revenue.items():
        if category in prev_revenue:
            prev_rev = prev_revenue[category]
            pct = mom_growth(prev_rev, curr_rev)
            flag_status = is_flagged(pct)

            if flag_status == "escalate_exact_boundary":
                escalated_categories.append(category)
            elif flag_status == "flagged":
                flagged_candidates.append({
                    "category": category,
                    "mom_pct": pct,
                    "previous_revenue": prev_rev,
                    "current_revenue": curr_rev,
                    "abs_mom": abs(pct)
                })

    # Subtask 5: Sort flagged categories by abs(mom_pct) descending
    flagged_candidates.sort(key=lambda x: x["abs_mom"], reverse=True)

    # Subtasks 6 & 7: Draft top 3 by magnitude and suppress remaining flagged items
    top_3 = flagged_candidates[:3]
    suppressed = flagged_candidates[3:]

    flagged_categories_output = []
    for item in top_3:
        msg = draft_message(item["category"], item["mom_pct"])
        flagged_categories_output.append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "drafted": True,
            "message": msg
        })

    suppressed_categories_output = [item["category"] for item in suppressed]

    # Subtask 8: Emit structured output dictionary matching required JSON schema
    return {
        "run_month": run_month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories_output,
        "suppressed_categories": suppressed_categories_output,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval"
    }


if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_OUTPUT = os.path.join(BASE_DIR, "..", "part1_sql", "output")
    FIXTURES_DIR = os.path.join(BASE_DIR, "..", "part2_engine", "fixtures")

    # Helper paths for running scenarios
    apr_csv = os.path.join(DATA_OUTPUT, "monthly_category_revenue.csv")
    corrupted_csv = os.path.join(FIXTURES_DIR, "corrupted_feed.csv")

    # Test Corrupted Feed Scenario
    print("--- Corrupted Feed Test ---")
    result_corrupted = run("July", apr_csv, corrupted_csv)
    print(json.dumps(result_corrupted, indent=2))