meesho-growth-pipeline/
│
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
│
└── part4_agent/
    ├── agent_spec.md
    └── mock_agent_runner.py

    # Reusable Prompt Pack for Stakeholder Updates

## 1. Trigger
The specific condition that starts this prompt is when `growth_engine.is_flagged(mom_pct)` returns `"flagged"` (i.e., absolute MoM growth exceeds the 8.0% threshold)[cite: 9, 12].

## 2. Input List
- `{category}`: Category name (e.g., Ethnic Wear)[cite: 12]
- `{previous_revenue}`: Revenue for the prior month in INR[cite: 12]
- `{current_revenue}`: Revenue for the current month in INR[cite: 12]
- `{mom_pct}`: Computed MoM percentage change[cite: 12]
- `{month}`: Current reporting month (e.g., May or June)[cite: 12]
- `{prev_month}`: Prior baseline month (e.g., April or May)[cite: 12]

## 3. Prompt Template
You are an operational analytics assistant for Meesho Regional Managers[cite: 12, 13].
Transform the following verified growth metrics into a concise stakeholder narrative using strict **Context -> Insight -> Implication** structure[cite: 12]:

- **Category:** {category}[cite: 12]
- **Period:** {month} vs {prev_month}[cite: 12]
- **Prior Month Revenue:** INR {previous_revenue}[cite: 12]
- **Current Month Revenue:** INR {current_revenue}[cite: 12]
- **MoM Change:** {mom_pct}%[cite: 12]

### Instructions:
1. **Context:** State what is being measured and over what period[cite: 12].
2. **Insight:** Present the exact verified MoM growth figure, explicitly labeling it as a fact[cite: 12]. Do not state any number not provided in the input[cite: 12].
3. **Implication:** Provide a concrete, actionable next step[cite: 12]. If proposing a root cause, explicitly label it as a hypothesis[cite: 12].
4. **Resellers:** Refer to resellers strictly by coded aliases (e.g., `ALIAS-19`), never by raw seller names[cite: 12, 13].

## 4. Checklist (Verification Rules)
- [ ] Does every number in the draft match a supplied placeholder value exactly?[cite: 12]
- [ ] Is every claim labeled explicitly as either fact or hypothesis?[cite: 12]
- [ ] Is the recommendation specific and actionable (not a vague suggestion like "look into ethnic wear")?[cite: 12]
- [ ] Is any reseller referenced only by coded alias (never by raw name)?[cite: 12]

# Worked Narrative Report & Chart Justifications

## 3.2 Worked Narrative Block 1: May Ethnic Wear (+77.1% MoM)
- **Context:** Revenue performance for the Ethnic Wear category measured for May compared against April[cite: 12].
- **Insight:** Ethnic Wear revenue reached INR 185107.61 in May, moving from INR 104520.77 in April—representing a verified MoM growth of +77.1% (Fact)[cite: 10, 12].
- **Implication:** Regional Ops should expand top reseller seller-onboarding allocations in North region hubs by 15% for June (Actionable Step). Hypothesis: Demand grew due to festival catalog promotions run during early May[cite: 12].

### Self-Score against Refinement Criteria:
- **Specificity:** PASS — Uses exact category name ("Ethnic Wear"), exact months ("May vs April"), and verified figure (+77.1%)[cite: 10, 13].
- **Audience Fit:** PASS — Written concisely for a Regional Manager rather than a data engineer[cite: 13].
- **Completeness:** PASS — Context, Insight (Fact), and Implication (Actionable step + Hypothesis) are all explicitly present[cite: 12, 13].
- **Actionability:** PASS — Recommends a concrete 15% expansion of North hub onboarding allocations rather than a vague suggestion[cite: 12, 13].

---

## 3.2 Worked Narrative Block 2: June Ethnic Wear (-58.74% MoM)
- **Context:** Revenue performance for the Ethnic Wear category measured for June compared against May[cite: 12].
- **Insight:** Ethnic Wear revenue contracted to INR 76371.53 in June from INR 185107.61 in May, recording a MoM decline of -58.74% (Fact)[cite: 8, 11, 12].
- **Implication:** Category managers should audit return reasons for top-selling SKUs and adjust merchant price points before July sales events (Actionable Step). Hypothesis: Demand normalized following the conclusion of May promotional campaigns[cite: 12].

### Self-Score against Refinement Criteria:
- **Specificity:** PASS — References exact category ("Ethnic Wear"), exact months ("June vs May"), and verified figure (-58.74%)[cite: 11, 13].
- **Audience Fit:** PASS — Tailored for executive operational review[cite: 13].
- **Completeness:** PASS — Context, Insight, and Implication sections are fully articulated[cite: 12, 13].
- **Actionability:** PASS — Specifies immediate auditing of return reasons and price points for key SKUs[cite: 12, 13].

---

## 3.3 Chart-Choice Justification

1. **"Which month had the highest total revenue?"**
   - **Chart Type:** Vertical Bar Chart (Univariate / Discrete Time)[cite: 13].
   - **Justification:** A simple vertical bar chart with 3 discrete bars (April, May, June) and a baseline starting at zero allows stakeholders to visually compare total monthly revenue within 2 seconds without visual distraction[cite: 13].

2. **"What percentage share does Ethnic Wear represent of April's total revenue?"**
   - **Chart Type:** 100% Stacked Bar Chart or Donut Chart (Proportion Analysis)[cite: 13].
   - **Justification:** A donut chart clearly represents part-to-whole relationships for categorical proportions in a single period, highlighting Ethnic Wear's 24.92% share at a glance[cite: 13].

3. **"How do the four regions compare on total revenue?"**
   - **Chart Type:** Horizontal Bar Chart (Bivariate Category Comparison)[cite: 13].
   - **Justification:** A horizontal bar chart sorted in descending order cleanly compares total revenue across discrete categories (North, West, South, East) with non-overlapping region labels[cite: 8, 13].

---

## 3.4 Top Resellers Spend Narrative (Masked)

Top high-performing resellers by spend (> INR 50,000)[cite: 8]:
- `ALIAS-19` generated total spend of INR 75295.09[cite: 8].
- `ALIAS-22` generated total spend of INR 73882.33[cite: 8].
- `ALIAS-12` generated total spend of INR 69936.46[cite: 8].
- `ALIAS-06` generated total spend of INR 64238.97[cite: 8].
- `ALIAS-05` generated total spend of INR 61825.02[cite: 8].
def alias_for(reseller_id: str) -> str:
    """Transforms a reseller ID into an anonymized alias (e.g. RS019 -> ALIAS-19)."""
    return f"ALIAS-{reseller_id[3:]}"

def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """Verifies that no raw reseller names appear verbatim in the narrative text."""
    for name in reseller_names:
        if name in text:
            return False
    return True

if __name__ == "__main__":
    # Test cases per acceptance criteria
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"
    
    known_names = ["Mumbai Reseller 1", "Mumbai Reseller 4", "Hyderabad Reseller 6", "Lucknow Reseller 6", "Jaipur Reseller 5"]
    
    clean_narrative = "Top performers include ALIAS-19 with INR 75295.09 and ALIAS-22 with INR 73882.33."
    leaky_narrative = "Top performer Mumbai Reseller 1 achieved total spend of INR 75295.09."
    
    assert assert_no_raw_names_leak(clean_narrative, known_names) is True
    assert assert_no_raw_names_leak(leaky_narrative, known_names) is False
    
    print("All masking assertions passed successfully!")