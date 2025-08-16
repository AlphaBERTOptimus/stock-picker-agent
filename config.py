"""
配置文件 - AlphaBERTOptimus 选股智能体
"""
import os

# 项目信息
PROJECT_NAME = "AI Stock Picker Agent"
VERSION = "2.0.0"
AUTHOR = "AlphaBERTOptimus"
GITHUB_REPO = "https://github.com/AlphaBERTOptimus/stock-picker-agent"

# API配置
YAHOO_FINANCE_ENABLED = True
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')

# 缓存配置
CACHE_TTL_STOCK_DATA = 300  # 5分钟
CACHE_TTL_STOCK_LIST = 3600  # 1小时

# 筛选配置
MAX_STOCKS_PER_QUERY = 10
MAX_SEARCH_UNIVERSE = 20
MIN_MARKET_CAP = 100e6  # 1亿美元最小市值

# UI配置
DEFAULT_THEME = "dark_green"
ENABLE_REAL_TIME_DATA = True

# 评分权重配置
SCORING_WEIGHTS = {
    'fundamental': 0.4,  # 基本面权重40%
    'technical': 0.3,    # 技术面权重30%
    'growth': 0.2,       # 成长性权重20%
    'risk': 0.1          # 风险调整权重10%
}
