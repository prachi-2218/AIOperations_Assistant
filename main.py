import os
from dotenv import load_dotenv

load_dotenv()
from agents.planner import create_plan
from agents.executor import execute_plan
from agents.verifier import verify_and_format
from utils.cost_tracker import cost_tracker



def main():
    print("=== AI Operations Assistant ===")
    user_task = input("Enter your task: ")

    print("\n[1] Planning...")
    plan = create_plan(user_task)
    print("Plan:", plan)

    print("\n[2] Executing...")
    execution_results = execute_plan(plan)
    print("Execution Results:", execution_results)

    print("\n[3] Verifying & Formatting...")
    final_answer = verify_and_format(user_task, execution_results)

    print("\n=== FINAL ANSWER ===")
    print(final_answer)
    
    # Display cost summary
    cost_summary = cost_tracker.get_summary()
    print(f"\n=== COST SUMMARY ===")
    print(f"Total LLM calls: {cost_summary['total_calls']}")
    print(f"Total tokens used: {cost_summary['total_tokens']:,}")
    print(f"Total cost: ${cost_summary['total_cost_usd']:.6f}")
    print(f"Cost by agent: {cost_summary['cost_by_agent']}")
    print(f"Cost by provider: {cost_summary['cost_by_provider']}")
    
    # Show free tier status if applicable
    if "free_tier_status" in cost_summary:
        free_status = cost_summary["free_tier_status"]
        print(f"\n=== FREE TIER STATUS ===")
        print(f"Provider: {free_status['provider']}")
        print(f"Model: {free_status['model']}")
        print(f"Tokens used: {free_status['tokens_used']:,}")
        print(f"Monthly limit: {free_status['monthly_limit']:,}")
        print(f"Usage: {free_status['monthly_usage_percent']:.2f}%")
        print(f"Status: {'WITHIN FREE TIER' if free_status['within_free_tier'] else 'EXCEEDS FREE TIER'}")
    
    # Save cost report
    cost_tracker.save_to_file()

if __name__ == "__main__":
    main()
