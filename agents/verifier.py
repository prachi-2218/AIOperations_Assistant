import json
from llm.llm_client import call_llm
from agents.executor import execute_plan
from utils.cost_tracker import cost_tracker

SYSTEM_PROMPT = """
You are a Verifier Agent.
Validate results and check completeness.

If data is missing or incomplete:
1. Identify what's missing
2. Suggest specific retry steps
3. Format a clean final user answer

Schema compliance:
- GitHub results should have: name, stars, description
- Weather results should have: city, temp_c, condition
- All steps should have status: success or failed
"""

def validate_schema(results):
    """Validate that results conform to expected schemas"""
    issues = []
    
    for result in results:
        if result.get("status") == "success":
            output = result.get("output", {})
            action = result.get("action", "")
            
            if "GitHub" in action:
                if isinstance(output, list):
                    for i, item in enumerate(output):
                        if not all(key in item for key in ["name", "stars", "description"]):
                            issues.append(f"GitHub result {i+1} missing required fields")
                            
            elif "weather" in action.lower():
                if not all(key in output for key in ["city", "temp_c", "condition"]):
                    issues.append("Weather result missing required fields")
    
    return issues

def retry_failed_steps(user_task, execution_results):
    """Retry failed steps and update results"""
    retry_steps = []
    
    for result in execution_results:
        if result.get("status") == "failed" or "error" in result:
            # Create a retry step for failed executions
            original_step_id = result.get("step_id")
            action = result.get("action", "")
            
            if "GitHub" in action:
                retry_steps.append({
                    "step_id": f"retry_{original_step_id}",
                    "action": action,
                    "tool": "github_search",
                    "input": "ai agents"  # Default fallback
                })
            elif "weather" in action.lower():
                retry_steps.append({
                    "step_id": f"retry_{original_step_id}",
                    "action": action,
                    "tool": "weather_api",
                    "input": "London"  # Default fallback
                })
    
    if retry_steps:
        print(f"Retrying {len(retry_steps)} failed steps...")
        retry_results = execute_plan(retry_steps)
        
        # Update original results with retry data
        for retry_result in retry_results:
            original_step_id = retry_result["step_id"].replace("retry_", "")
            for original_result in execution_results:
                if original_result["step_id"] == int(original_step_id):
                    if retry_result.get("status") == "success":
                        original_result.update(retry_result)
                    break
    
    return execution_results

def verify_and_format(user_task, execution_results):
    # First, validate schema compliance
    schema_issues = validate_schema(execution_results)
    
    # Retry failed steps if any
    updated_results = retry_failed_steps(user_task, execution_results)
    
    # Re-validate after retries
    final_issues = validate_schema(updated_results)
    
    user_prompt = f"""
User Task: {user_task}

Execution Results:
{json.dumps(updated_results, indent=2)}

Schema Issues Found: {final_issues if final_issues else "None"}

Return a helpful final structured answer for the user.
If there are still missing or incomplete data, mention it clearly.
"""

    return call_llm(SYSTEM_PROMPT, user_prompt, agent_type="verifier")
