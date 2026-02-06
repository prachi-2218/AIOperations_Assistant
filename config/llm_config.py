"""
LLM Configuration for Cost Tracking
This file makes it easy to update pricing and add new models/providers
"""

# LLM Provider Configuration
LLM_CONFIG = {
    "providers": {
        "google": {
            "name": "Google Gemini",
            "models": {
                "gemini-2.5-flash": {
                    "input_price": 0.0,      # $0.0 per 1M input tokens (free tier)
                    "output_price": 0.0,     # $0.0 per 1M output tokens (free tier)
                    "free_tier": True,
                    "monthly_limit": 15_000_000,  # 15M tokens/month
                    "description": "Latest Gemini model, free tier available"
                },
                "gemini-pro": {
                    "input_price": 0.25,     # $0.25 per 1M input tokens
                    "output_price": 0.50,    # $0.50 per 1M output tokens
                    "free_tier": False,
                    "description": "Standard Gemini model"
                },
                "gemini-1.5-flash": {
                    "input_price": 0.075,    # $0.075 per 1M input tokens
                    "output_price": 0.15,     # $0.15 per 1M output tokens
                    "free_tier": False,
                    "description": "Fast Gemini model"
                }
            }
        },
        
        "openai": {
            "name": "OpenAI",
            "models": {
                "gpt-4": {
                    "input_price": 0.03,      # $0.03 per 1M input tokens
                    "output_price": 0.06,     # $0.06 per 1M output tokens
                    "free_tier": False,
                    "description": "Most capable GPT-4 model"
                },
                "gpt-4-turbo": {
                    "input_price": 0.01,      # $0.01 per 1M input tokens
                    "output_price": 0.03,     # $0.03 per 1M output tokens
                    "free_tier": False,
                    "description": "Faster GPT-4 model"
                },
                "gpt-3.5-turbo": {
                    "input_price": 0.0015,    # $0.0015 per 1M input tokens
                    "output_price": 0.002,    # $0.002 per 1M output tokens
                    "free_tier": False,
                    "description": "Fast and affordable model"
                }
            }
        },
        
        "anthropic": {
            "name": "Anthropic Claude",
            "models": {
                "claude-3-opus": {
                    "input_price": 0.015,     # $0.015 per 1M input tokens
                    "output_price": 0.075,     # $0.075 per 1M output tokens
                    "free_tier": False,
                    "description": "Most capable Claude model"
                },
                "claude-3-sonnet": {
                    "input_price": 0.003,     # $0.003 per 1M input tokens
                    "output_price": 0.015,     # $0.015 per 1M output tokens
                    "free_tier": False,
                    "description": "Balanced Claude model"
                },
                "claude-3-haiku": {
                    "input_price": 0.00025,   # $0.00025 per 1M input tokens
                    "output_price": 0.00125,   # $0.00125 per 1M output tokens
                    "free_tier": False,
                    "description": "Fast and affordable Claude model"
                }
            }
        }
    },
    
    # Model name patterns for auto-detection
    "model_patterns": {
        "google": ["gemini"],
        "openai": ["gpt"],
        "anthropic": ["claude"]
    }
}

# Default configuration for this project
DEFAULT_PROVIDER = "google"
DEFAULT_MODEL = "gemini-2.5-flash"

def get_model_info(model_name: str) -> dict:
    """Get model information by name"""
    for provider_key, provider_config in LLM_CONFIG["providers"].items():
        for model_key, model_info in provider_config["models"].items():
            if model_key in model_name.lower():
                return {
                    "provider": provider_key,
                    "provider_name": provider_config["name"],
                    "model": model_key,
                    "model_info": model_info
                }
    return None

def is_free_tier(model_name: str) -> bool:
    """Check if model has free tier available"""
    model_info = get_model_info(model_name)
    if model_info:
        return model_info["model_info"].get("free_tier", False)
    return False

def get_monthly_limit(model_name: str) -> int:
    """Get monthly token limit for free tier models"""
    model_info = get_model_info(model_name)
    if model_info and model_info["model_info"].get("free_tier", False):
        return model_info["model_info"].get("monthly_limit", 0)
    return 0
