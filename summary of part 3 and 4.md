Here is the concise summary for Part 3 and Part 4:

Part 3: Reliable AI Narrative & Prompt-Pack Report 
Objective: Standardize executive communication, generate hallucination-free narratives using verified numbers, and enforce strict reseller data privacy rules.   


Key Components & Files:

prompt_pack.md: A four-part template (Trigger, Input List, Prompt, Checklist) that enforces the Context → Insight → Implication narrative framework.   


narrative_report.md: Worked narrative updates for May (+77.1% MoM) and June (-58.74% MoM) Ethnic Wear results—self-scored against 4 refinement criteria (Specificity, Audience Fit, Completeness, Actionability)—along with written chart-choice justifications.   


masking.py: Privacy logic providing alias_for() (converting IDs like RS019 to ALIAS-19) and assert_no_raw_names_leak() to ensure raw vendor names never leak into external updates.   


Part 4: Agentic Workflow Spec & Mock Agent Runner 
Objective: Integrate Parts 1–3 into an automated, guarded monitoring pipeline that processes revenue feeds and drafts stakeholder alerts.   


Key Components & Files:

agent_spec.md: Architectural document detailing the 5 core agent components (Goal, Tools, Memory/State, Planner, Feedback Loop), input/action/output guardrails, failure modes, and Given-When-Then specs.   

mock_agent_runner.py: Execution script that runs 8 ordered subtasks—validates CSV data (triggers a Hard Stop on corruption), computes MoM growth, flags anomalies, caps drafts at top 3 by growth magnitude, logs suppressed/escalated categories, and emits a structured JSON telemetry output.   
