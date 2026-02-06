# AI Operations Assistant (Multi-Agent System)

## Overview
This project implements a local, multi-agent AI Operations Assistant that converts natural language tasks into structured plans, executes real API calls, and verifies results using an LLM.

The system demonstrates agent-based reasoning, tool usage, and real-world API integration.

---

## Architecture
User → Planner Agent → Executor Agent → Verifier Agent → Final Answer

---

## LLM & APIs

### LLM
- Google Gemini 2.5 Flash

### Integrated APIs
- GitHub Search API
- OpenWeatherMap API

---

## Project Structure
ai_ops_assistant/
├── agents/
├── tools/
├── llm/
├── utils/
├── config/
├── main.py
├── requirements.txt
├── .env.example
└── README.md

## Setup 
1. **Prerequisites**
   - Python 3.8+ installed
   - Git installed

2. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd AIOperations_Assistant
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
   **Required Environment Variables:**
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here  # Get from: https://aistudio.google.com/app/apikey
   OPENWEATHER_API_KEY=your_openweather_key_here  # Get from: https://openweathermap.org/api
   GITHUB_TOKEN=your_github_token_here  # Get from: https://github.com/settings/tokens
   ```

5. **Run Locally**
   ```bash
   python main.py
   ```
   
   The system will start and prompt for natural language tasks.

## Example Tasks (For Demo)
Here are 5 example prompts to test the system:

1. **GitHub + Weather Combo:**
   ```
   Find top AI agent GitHub repositories and tell me the current weather in Jaipur
   ```

2. **Deployment Planning:**
   ```
   Search for popular Python automation repositories and give me the weather in London for deployment planning
   ```

3. **DevOps Research:**
   ```
   Get the current weather in Delhi and find trending DevOps GitHub repositories
   ```

4. **CI/CD Planning:**
   ```
   Check weather in Bangalore and list popular CI/CD GitHub repositories to help plan a deployment demo
   ```

5. **ML Research:**
   ```
   Find top machine learning GitHub repositories and check weather conditions in San Francisco
   ```

## Known Limitations & Tradeoffs

### **API Limitations**
- **GitHub API:** Rate limited to 5,000 requests/hour for authenticated requests
- **OpenWeather API:** Free tier limited to 1,000 calls/day
- **Gemini API:** Rate limits vary by model and region

### **System Limitations**
- **Sequential Dependencies:** Current implementation assumes all steps are independent
- **Error Recovery:** Limited retry attempts (3 max) for failed API calls
- **Cache Duration:** Fixed TTL (5-10 minutes) may not suit all use cases
- **Token Estimation:** Cost tracking uses rough token estimation (~4 chars/token)
- **Provider Coverage:** Currently supports 3 major providers (can be extended via config)

### **Tradeoffs**
- **Simplicity vs. Robustness:** Prioritized clean architecture over complex dependency management
- **Performance vs. Cost:** Caching reduces API calls but increases memory usage
- **Parallel vs. Sequential:** Parallel execution improves speed but complicates error handling

### **Troubleshooting**
- **"API_KEY not found":** Check `.env` file is in project root
- **"401 Unauthorized":** Verify API keys are valid and not expired
- **"Model not found":** Ensure Gemini API key has proper permissions
- **"Provider: unknown":** Add model pattern to `config/llm_config.py`
- **"Model not found in pricing config":** Add model to configuration file
- **Network errors:** Check internet connection and API service status

---

## Advanced Features

### **Performance Optimizations**
- **Parallel Execution:** Independent API calls run concurrently
- **Smart Caching:** API responses cached to reduce costs and latency
- **Retry Logic:** Exponential backoff for failed requests

### **Monitoring & Cost Control**
- **Generalized Cost Tracking:** Multi-provider cost monitoring (Gemini, OpenAI, Anthropic)
- **Provider Breakdown:** Cost analysis by LLM provider and model
- **Agent Breakdown:** Cost analysis by agent type (Planner/Verifier)
- **Free Tier Monitoring:** Automatic tracking of free tier limits and usage
- **Configuration-Based:** Easy pricing updates via `config/llm_config.py`
- **Detailed Reports:** JSON reports with comprehensive cost analysis

### **Enhanced Reliability**
- **Schema Validation:** Automatic validation of API response formats
- **Error Recovery:** Automatic retry of failed steps
- **Graceful Degradation:** Partial results returned when possible

---

## Configuration System

### **LLM Configuration**
The system uses a generalized configuration approach for cost tracking:

- **Location:** `config/llm_config.py`
- **Providers Supported:** Google Gemini, OpenAI, Anthropic Claude
- **Auto-Detection:** Automatically detects provider from model name
- **Easy Updates:** Add new models/providers without code changes

### **Cost Tracking Features**
- **Multi-Provider Support:** Track costs across different LLM providers
- **Free Tier Monitoring:** Automatic alerts for free tier usage
- **Provider Breakdown:** Cost analysis by provider and model
- **Configuration-Based:** Pricing updates via config file only

---

