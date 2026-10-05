Step 4: Part 4 — Agent Specification
# Agent Specification: Reseller Growth Monitoring Agent

## 4.1 Agent Architecture Components

- **Goal:** Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out[cite: 14].
- **Tools:**
  - `validate_feed(csv_path)` (Part 2)[cite: 10, 14, 15]
  - `mom_growth(previous, current)` (Part 2)[cite: 10, 14, 15]
  - `is_flagged(mom_pct)` (Part 2)[cite: 10, 14, 15]
  - Prompt-pack template-fill draft generator (Part 3)[cite: 12, 14, 15]
- **Memory / State:** Stores monthly revenue per category between pipeline runs to compute sequential MoM metrics[cite: 14, 15].
- **Planner:** Ordered sequence of subtasks 1 through 8 detailed in section 4.2[cite: 14, 15].
- **Feedback Loop:** Human-approval checkpoint where drafts are flagged as `drafted_and_held_for_approval` before any delivery[cite: 14, 15, 16].

### Guardrails:
- **Input Guardrail:** `validate_feed` must evaluate to `True` before any MoM processing occurs[cite: 10, 15].
- **Action Guardrail:** Messages are drafted and held; no message is ever auto-sent[cite: 15].
- **Output Guardrail:** Every number in drafted messages must trace back to Part 1 / Part 2 calculated numbers[cite: 15, 16].

### Failure Handling:
- If `validate_feed` returns `False`, execution halts immediately in a **Hard Stop**, outputting all validation error strings[cite: 15, 16].

---

## 4.2 Ordered Subtasks (Planner Steps)

1. Load current month revenue CSV feed and execute `validate_feed`[cite: 15].
2. If invalid, **Hard Stop** immediately and report error list[cite: 15].
3. If valid, compute `mom_growth` for each category against prior month baseline[cite: 15].
4. Run `is_flagged` on every category MoM percentage[cite: 15].
5. Sort flagged categories descending by absolute magnitude `abs(mom_pct)`[cite: 15].
6. Draft template messages for **at most top 3** flagged categories to prevent notification flooding[cite: 15].
7. Log remaining flagged categories beyond cap into `suppressed_categories` without drafting messages[cite: 15].
8. Log categories with `is_flagged == "escalate_exact_boundary"` into `escalated_categories`[cite: 15].
9. Emit structured JSON output containing status, error details, drafts, suppressed list, and escalated list[cite: 15, 16].

---

## 4.3 Agent Specifications (Given-When-Then Format)

### Spec 1: Normal Operation (May Scenario)
- **GIVEN** valid April and May revenue feeds.
- **WHEN** runner executes May monitoring[cite: 16].
- **THEN** `validation_status` is `"valid"`, `flagged_categories` contains 3 drafted items ordered by `abs(mom_pct)` descending, and 2 items in `suppressed_categories`[cite: 16].

### Spec 2: High Volatility (June Scenario)
- **GIVEN** valid May and June revenue feeds[cite: 16].
- **WHEN** runner executes June monitoring[cite: 16].
- **THEN** exactly 3 categories are drafted (Ethnic Wear, Home & Kitchen, Kids Wear), 1 category suppressed (Western Wear), and 1 unflagged category omitted (Beauty & Personal Care)[cite: 16].

### Spec 3: Input Corruption Scenario
- **GIVEN** `corrupted_feed.csv` as the input feed[cite: 10, 16].
- **WHEN** runner executes validation[cite: 16].
- **THEN** `validation_status` is `"invalid"`, `action_taken` is `"hard_stop"`, and `validation_errors` contains exactly 3 error strings[cite: 10, 16].

### Spec 4: Exact Boundary Condition
- **GIVEN** a feed with exact 8.0% growth[cite: 10, 16].
- **WHEN** runner evaluates flags[cite: 16].
- **THEN** `is_flagged` returns `"escalate_exact_boundary"` and category is appended to `escalated_categories`[cite: 10, 15, 16].
Step 5: Part 4 — Mock Agent Runner (part4_agent/mock_agent_runner.py)
Create part4_agent/mock_agent_runner.py implementing the complete runner and structured JSON schema output[cite: 16]:
import os
import sys
import json
import csv

# Import Part 2 engine functions directly
PART2_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "part2_engine"))
sys.path.append(PART2_DIR)

from growth_engine import validate_feed, mom_growth, is_flagged


def load_category_revenue(csv_path: str) -> dict[str, float]:
    """Helper to parse a valid monthly category revenue CSV file."""
    revenue_map = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["category"].strip()
            rev = float(row["revenue"].strip())
            revenue_map[cat] = rev
    return revenue_map


def draft_narrative(
    category: str, mom_pct: float, prev_rev: float, curr_rev: float, run_month: str
) -> str:
    """Generates draft narrative using Part 3 template logic without external LLM calls."""
    sign = "+" if mom_pct > 0 else ""
    return (
        f"Category '{category}' recorded a MoM revenue shift of {sign}{mom_pct}% in {run_month} "
        f"(from INR {prev_rev:.2f} to INR {curr_rev:.2f}). "
        f"Recommendation: Review regional allocation and catalog promotions."
    )


def run(
    run_month: str, previous_month_csv: str, current_month_csv: str
) -> dict:
    """Executes the subtasks 1-8 and returns structured JSON output."""
    # Subtask 1 & 2: Validate input feed
    is_valid, errors = validate_feed(current_month_csv)
    if not is_valid:
        return {
            "run_month": run_month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    prev_data = load_category_revenue(previous_month_csv)
    curr_data = load_category_revenue(current_month_csv)

    evaluated = []
    escalated_categories = []

    # Subtasks 3, 4 & 8: Evaluate MoM and flags
    for cat, curr_rev in curr_data.items():
        if cat in prev_data:
            prev_rev = prev_data[cat]
            pct = mom_growth(prev_rev, curr_rev)
            flag_status = is_flagged(pct)

            if flag_status == "escalate_exact_boundary":
                escalated_categories.append(cat)
            elif flag_status == "flagged":
                evaluated.append(
                    {
                        "category": cat,
                        "mom_pct": pct,
                        "previous_revenue": prev_rev,
                        "current_revenue": curr_rev,
                        "abs_mom": abs(pct),
                    }
                )

    # Subtask 5: Sort flagged categories descending by magnitude
    evaluated.sort(key=lambda x: x["abs_mom"], reverse=True)

    # Subtasks 6 & 7: Top 3 cap and suppression logging
    top_3_flagged = evaluated[:3]
    suppressed_items = evaluated[3:]

    flagged_categories_output = []
    for item in top_3_flagged:
        msg = draft_narrative(
            item["category"],
            item["mom_pct"],
            item["previous_revenue"],
            item["current_revenue"],
            run_month,
        )
        flagged_categories_output.append(
            {
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": msg,
            }
        )

    suppressed_categories_output = [item["category"] for item in suppressed_items]

    # Subtask 9: Output JSON Schema
    return {
        "run_month": run_month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories_output,
        "suppressed_categories": suppressed_categories_output,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_OUTPUT_DIR = os.path.join(BASE_DIR, "..", "part1_sql", "output")
    FIXTURES_DIR = os.path.join(BASE_DIR, "..", "part2_engine", "fixtures")

    # Filtered Monthly CSV paths for testing scenarios
    apr_csv = os.path.join(DATA_OUTPUT_DIR, "monthly_category_revenue.csv")
    corrupted_csv = os.path.join(FIXTURES_DIR, "corrupted_feed.csv")

    print("--- Test Run: Corrupted Feed Scenario ---")
    result_corrupted = run("July", apr_csv, corrupted_csv)
    print(json.dumps(result_corrupted, indent=2))
    Step 6: End-to-End Execution Verification
Run these commands in order from your terminal to verify all parts pass locally before pushing to GitHub: