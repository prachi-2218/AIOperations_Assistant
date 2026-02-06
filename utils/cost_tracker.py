import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from config.llm_config import LLM_CONFIG, get_model_info, is_free_tier, get_monthly_limit

@dataclass
class LLMCall:
    timestamp: float
    model: str
    provider: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    agent_type: str  # planner, verifier, etc.

class CostTracker:
    def __init__(self):
        self.calls: List[LLMCall] = []
        # Use external configuration
        self.config = LLM_CONFIG
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (approximately 4 characters per token)"""
        return len(text) // 4
    
    def detect_provider(self, model: str) -> str:
        """Auto-detect provider from model name using config"""
        model_info = get_model_info(model)
        if model_info:
            return model_info["provider"]
        return "unknown"  # Default if can't detect
    
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost based on model pricing from config"""
        model_info = get_model_info(model)
        if model_info:
            pricing = model_info["model_info"]
            input_cost = (prompt_tokens * pricing["input_price"]) / 1000000
            output_cost = (completion_tokens * pricing["output_price"]) / 1000000
            return input_cost + output_cost
        else:
            # Default pricing if model not found
            return (prompt_tokens * 0.001 + completion_tokens * 0.002) / 1000000
    
    def track_call(self, model: str, prompt: str, response: str, agent_type: str):
        """Track an LLM call and calculate costs"""
        provider = self.detect_provider(model)
        prompt_tokens = self.estimate_tokens(prompt)
        completion_tokens = self.estimate_tokens(response)
        total_tokens = prompt_tokens + completion_tokens
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        
        call = LLMCall(
            timestamp=time.time(),
            model=model,
            provider=provider,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost,
            agent_type=agent_type
        )
        
        self.calls.append(call)
        return call
    
    def get_total_cost(self) -> float:
        """Get total cost for all calls"""
        return sum(call.cost_usd for call in self.calls)
    
    def get_total_tokens(self) -> int:
        """Get total tokens used"""
        return sum(call.total_tokens for call in self.calls)
    
    def get_cost_by_agent(self) -> Dict[str, float]:
        """Get cost breakdown by agent type"""
        costs = {}
        for call in self.calls:
            if call.agent_type not in costs:
                costs[call.agent_type] = 0
            costs[call.agent_type] += call.cost_usd
        return costs
    
    def get_summary(self) -> Dict:
        """Get cost and usage summary with provider-specific details"""
        total_tokens = self.get_total_tokens()
        summary = {
            "total_calls": len(self.calls),
            "total_cost_usd": self.get_total_cost(),
            "total_tokens": total_tokens,
            "cost_by_agent": self.get_cost_by_agent(),
            "cost_by_provider": self.get_cost_by_provider(),
            "average_cost_per_call": self.get_total_cost() / len(self.calls) if self.calls else 0
        }
        
        # Add free tier status for applicable models using config
        for call in self.calls:
            if is_free_tier(call.model):
                monthly_limit = get_monthly_limit(call.model)
                if monthly_limit > 0:  # Only show if there's a limit
                    summary["free_tier_status"] = {
                        "provider": call.provider,
                        "model": call.model,
                        "tokens_used": total_tokens,
                        "monthly_limit": monthly_limit,
                        "monthly_usage_percent": (total_tokens / monthly_limit) * 100,
                        "within_free_tier": total_tokens < monthly_limit
                    }
                    break  # Show status for first applicable model
        
        return summary
    
    def get_cost_by_provider(self) -> Dict[str, float]:
        """Get cost breakdown by provider"""
        costs = {}
        for call in self.calls:
            if call.provider not in costs:
                costs[call.provider] = 0
            costs[call.provider] += call.cost_usd
        return costs
    
    def save_to_file(self, filename: str = "cost_report.json"):
        """Save cost report to file"""
        summary = self.get_summary()
        summary["detailed_calls"] = [asdict(call) for call in self.calls]
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Cost report saved to {filename}")
    
    def reset(self):
        """Reset all tracking data"""
        self.calls.clear()
        print("Cost tracking reset")

# Global cost tracker instance
cost_tracker = CostTracker()
