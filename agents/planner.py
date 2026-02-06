import json
import re
from llm.llm_client import call_llm

SYSTEM_PROMPT = """
You are a Planner Agent.
Convert the user task into a JSON plan.
Each step must include:
- step_id
- action
- tool (if any)
- input

Return ONLY raw JSON array. No markdown. No explanation.
"""

def extract_json(text):
    # Remove markdown if Gemini adds it
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()

def create_plan(user_task):
    user_prompt = f"""
User Task: {user_task}

Return JSON only in this format:
[
  {{
    "step_id": 1,
    "action": "Search GitHub repositories",
    "tool": "github_search",
    "input": "ai agents"
  }}
]
"""
    response = call_llm(SYSTEM_PROMPT, user_prompt, agent_type="planner")
    clean = extract_json(response)
    return json.loads(clean)