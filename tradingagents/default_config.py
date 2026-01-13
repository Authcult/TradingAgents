import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": os.getenv("TRADINGAGENTS_DATA_DIR", os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        "data"
    )),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "modelscope",
    "deep_think_llm": "Qwen/Qwen2.5-72B-Instruct",
    "quick_think_llm": "Qwen/Qwen3-235B-A22B-Instruct-2507",
    "backend_url": "https://api-inference.modelscope.cn/v1/",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Data vendor configuration
    # Category-level configuration (default for all tools in category)
    "data_vendors": {
        "core_stock_apis": "yfinance",       # Options: yfinance, alpha_vantage, local
        "technical_indicators": "yfinance",  # Options: yfinance, alpha_vantage, local
        "fundamental_data": "alpha_vantage", # Options: alpha_vantage, local (不使用 openai)
        "news_data": "alpha_vantage,local",  # 指定fallback: alpha_vantage → local (跳过 openai)
    },
    # Tool-level configuration (takes precedence over category-level)
    "tool_vendors": {
        # Example: "get_stock_data": "alpha_vantage",  # Override category default
        # Example: "get_news": "google",               # Override category default (不使用 openai)
    },
}
