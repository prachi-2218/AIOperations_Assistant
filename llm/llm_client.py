import os
import google.generativeai as genai
from utils.cost_tracker import cost_tracker

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")
MODEL_NAME = "gemini-2.5-flash"

def call_llm(system_prompt, user_prompt, agent_type="unknown"):
    """
    Unified LLM call for Gemini.
    We manually combine system + user prompt since Gemini
    does not support system role like OpenAI.
    """

    full_prompt = f"""
SYSTEM INSTRUCTIONS:
{system_prompt}

USER REQUEST:
{user_prompt}
"""

    response = model.generate_content(full_prompt)
    response_text = response.text
    
    # Track cost
    cost_tracker.track_call(MODEL_NAME, full_prompt, response_text, agent_type)
    
    return response_text
