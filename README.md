Here is the high-level roadmap and operational synopsis for completing the entire project from end to end:
Project Overview & Core Architecture
The goal of this project is to build an end-to-end, guarded data and monitoring pipeline for Meesho category performance. It connects raw transactional SQL queries, automated Python validation, reliable narrative drafting, and an agentic monitoring runner without external LLM API dependencies.
[Part 1: SQL Database & Queries] 
              │
              ▼
[Part 2: Growth Engine & Rules Validation] 
              │
              ▼
[Part 3: Prompt Pack, Narrative & Masking] 
              │
              ▼
[Part 4: Agentic Workflow & Mock Runner]
Phase 1: Database Setup & SQL Analytics (Part 1)
Execute Dataset Generator: Run generate_dataset.py to create the SQLite database (meesho_reseller.db) and CSV feeds (resellers.csv, orders.csv).
Execute Queries & Export CSVs: Run part1_sql/generate_and_query.py to query delivered orders and export 5 key output files:

monthly_category_revenue.csv (Monthly breakdown).
region_wise_revenue.csv (North, West, South, East totals).
top_resellers_by_spend.csv (Resellers spending > INR 50,000).
zero_order_resellers.csv (Identifies RS024 using COUNT(order_id)).
june_aov.csv (Average order value).
3. Document Technical Findings: Write part1_sql/README.md explaining why COUNT(order_id) must be used over COUNT(*) during LEFT JOIN operations to avoid false positive counts on unmatched resellers.
Phase 2: Python Growth Engine & Validation (Part 2)
Implement Feed Validation (validate_feed): Check CSV headers, non-empty values, non-negative numeric types, and verify that all expected categories exist.
Implement Growth Metrics (mom_growth & is_flagged):
Calculate signed percentage growth rounded to 2 decimal places.
Flag metrics where absolute growth $\vert{}MoM\vert{} > 8.0\%$. 
Mark exact boundary conditions ($\vert{}MoM\vert{} == 8.0\%$) as "escalate_exact_boundary"
Automate Unit Tests: Build test_growth_engine.py using pytest to validate both clean data and corrupted edge cases.
Phase 3: Stakeholder Narratives & Privacy Policy (Part 3)Design Prompt Pack (prompt_pack.md): Write a four-part prompt template (Trigger, Input List, Prompt, Checklist) that enforces Context $\rightarrow$ Insight $\rightarrow$ Implication formatting. 
Draft Narrative Reports (narrative_report.md):

Write structured narratives for May (+77.1%) and June (-58.74%) Ethnic Wear results using exact numbers.
Self-score each narrative against Specificity, Audience Fit, Completeness, and Actionability.
Document chart-choice justifications (vertical bar, donut, horizontal bar) without rendering actual images.
Enforce Data Privacy (masking.py): Implement alias_for() to convert raw reseller IDs into aliases (e.g., RS019 $\rightarrow$ ALIAS-19) and build assert_no_raw_names_leak() to ensure raw merchant names never leak into external reports.  
Phase 4: Agentic Workflow & Mock Runner (Part 4)
Document Agent Architecture (agent_spec.md): Define the agent's Goal, Tools, Memory, Planner (8 subtasks), Feedback Loop, Guardrails, and Given-When-Then specs.
Build Mock Runner (mock_agent_runner.py): Step 1: Validate the current month CSV feed (trigger a Hard Stop if invalid).   
Step 2: Compute MoM growth against the prior month baseline.   Step 3: Sort flagged categories by absolute growth magnitude.   Step 4: Draft narrative updates for at most the top 3 categories, log excess categories into suppressed_categories, and route exact 8.0% boundary items into escalated_categories.   Step 5: Emit structured telemetry JSON setting action_taken = "drafted_and_held_for_approval".   Summary Checklist for SubmissionStepRequirementTarget File / ArtifactPart 1SQLite DB & SQL Exportsdata/meesho_reseller.db, part1_sql/generate_and_query.py, part1_sql/output/*.csvPart 2Python Validation Enginepart2_engine/growth_engine.py, part2_engine/test_growth_engine.pyPart 3Prompt Pack & Privacy Maskingpart3_narrative/prompt_pack.md, part3_narrative/narrative_report.md, part3_narrative/masking.pyPart 4Agent Specification & Runnerpart4_agent/agent_spec.md, part4_agent/mock_agent_runner.pyRootMaster InstructionsREADME.md (Explains execution order and zero API key requirement)
Summary Checklist for Submission
Step	Requirement	Target File / Artifact
Part 1	SQLite DB & SQL Exports	data/meesho_reseller.db, part1_sql/generate_and_query.py, part1_sql/output/*.csv
Part 2	Python Validation Engine	part2_engine/growth_engine.py, part2_engine/test_growth_engine.py
Part 3	Prompt Pack & Privacy Masking	part3_narrative/prompt_pack.md, part3_narrative/narrative_report.md, part3_narrative/masking.py
Part 4	Agent Specification & Runner	part4_agent/agent_spec.md, part4_agent/mock_agent_runner.py

