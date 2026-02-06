import time
import random
import concurrent.futures
from tools.github_tool import search_repositories
from tools.weather_tool import get_weather

def retry_with_backoff(func, *args, max_retries=3, base_delay=1, **kwargs):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            time.sleep(delay)
    
def execute_single_step(step):
    """Execute a single step with retry logic"""
    tool = step.get("tool")
    input_data = step.get("input")
    
    try:
        if tool == "github_search":
            output = retry_with_backoff(search_repositories, input_data)
        elif tool == "weather_api":
            output = retry_with_backoff(get_weather, input_data)
        else:
            output = {"info": f"No tool needed for: {step['action']}"}
        
        return {
            "step_id": step["step_id"],
            "action": step["action"],
            "output": output,
            "status": "success"
        }
    except Exception as e:
        return {
            "step_id": step["step_id"],
            "action": step["action"],
            "error": str(e),
            "status": "failed"
        }

def can_execute_parallel(plan):
    """Check if steps can be executed in parallel (no dependencies)"""
    return len(plan) > 1

def execute_plan(plan):
    results = []
    
    if can_execute_parallel(plan):
        print(f"Executing {len(plan)} steps in parallel...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(plan), 4)) as executor:
            # Submit all steps for parallel execution
            future_to_step = {executor.submit(execute_single_step, step): step for step in plan}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_step):
                result = future.result()
                results.append(result)
    else:
        # Sequential execution for single steps or dependent steps
        print("Executing steps sequentially...")
        for step in plan:
            result = execute_single_step(step)
            results.append(result)
    
    # Sort results by step_id to maintain order
    results.sort(key=lambda x: x["step_id"])
    return results
