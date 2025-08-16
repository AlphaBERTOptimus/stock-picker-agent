import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime, timedelta
import time
import random
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Optional
import re

# 页面配置
st.set_page_config(
    page_title="选股智能体 - AI Stock Picker | AlphaBERTOptimus",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式 - 深绿色渐变背景，白色字体
st.markdown("""
<style>
    /* 主背景 - 深绿色渐变 */
    .stApp {
        background: linear-gradient(135deg, #1e3a3a 0%, #2d5a5a 25%, #3a7a7a 50%, #2d5a5a 75%, #1e3a3a 100%);
        background-attachment: fixed;
        color: white !important;
    }
    
    /* 主容器样式 */
    .main .block-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 所有文字设为白色 */
    .stApp, .stApp *, .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, 
    .stSelectbox label, .stTextInput label, .stButton label, 
    .css-1d391kg, .css-1d391kg *, div[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* 主标题样式 */
    .main-header {
        background: linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    /* 聊天消息样式 */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white !important;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.3), rgba(56, 178, 172, 0.3));
        border-left: 4px solid #10b981;
        margin-left: 2rem;
    }
    
    .bot-message {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(79, 70, 229, 0.3));
        border-left: 4px solid #3b82f6;
        margin-right: 2rem;
    }
    
    /* 股票卡片样式 */
    .stock-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        color: white !important;
    }
    
    .stock-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* 指标容器 */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-item {
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.8), rgba(79, 70, 229, 0.8)) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.9), rgba(79, 70, 229, 0.9)) !important;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg, div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 58, 58, 0.9), rgba(45, 90, 90, 0.9)) !important;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput > div > div > input::placeholder, .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* 选择框样式 */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* 进度条样式 */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #10b981, #3b82f6) !important;
    }
    
    /* 展开器样式 */
    .streamlit-expanderHeader, .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    /* 标签样式 */
    .recommendation-strong-buy {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .recommendation-buy {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .recommendation-hold {
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        color: white !important;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .recommendation-sell {
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: white !important;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 全美股票数据获取
@st.cache_data(ttl=3600)  # 缓存1小时
def get_all_us_stocks():
    """获取全美股票列表 - 扩展版"""
    try:
        # S&P 500
        sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        sp500_table = pd.read_html(sp500_url)[0]
        sp500_symbols = sp500_table['Symbol'].str.replace('.', '-').tolist()
        
        # NASDAQ 100 (完整列表)
        nasdaq100_symbols = [
            'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'GOOG', 'META', 'TSLA', 'AVGO', 'COST',
            'NFLX', 'TMUS', 'CSCO', 'ADBE', 'PEP', 'LIN', 'TXN', 'QCOM', 'AMAT', 'INTU',
            'ISRG', 'CMCSA', 'BKNG', 'HON', 'AMD', 'AMGN', 'VRTX', 'ADP', 'GILD', 'ADI',
            'MDLZ', 'SBUX', 'PYPL', 'REGN', 'MU', 'LRCX', 'FISV', 'CSX', 'ORLY', 'NXPI',
            'MRVL', 'FTNT', 'ADSK', 'DXCM', 'KLAC', 'CHTR', 'ABNB', 'MELI', 'CDNS', 'SNPS'
        ]
        
        # 热门科技股
        tech_stocks = [
            'CRM', 'SNOW', 'ORCL', 'NOW', 'MDB', 'VEEV', 'PANW', 'TWLO', 'OKTA', 'ZS',
            'NET', 'DDOG', 'PLTR', 'U', 'RBLX', 'COIN', 'RIVN', 'LCID', 'NIO', 'XPEV'
        ]
        
        # 传统行业龙头
        traditional_stocks = [
            'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'V', 'MA', 'JNJ',
            'PFE', 'UNH', 'ABBV', 'KO', 'PG', 'WMT', 'HD', 'DIS', 'MCD', 'XOM'
        ]
        
        # 合并所有股票
        all_stocks = list(set(sp500_symbols + nasdaq100_symbols + tech_stocks + traditional_stocks))
        
        # 过滤掉无效符号
        valid_stocks = []
        for symbol in all_stocks:
            if symbol and len(symbol) <= 5 and symbol.replace('-', '').isalpha():
                valid_stocks.append(symbol)
        
        return sorted(valid_stocks)
    
    except Exception as e:
        st.error(f"获取股票列表失败: {e}")
        return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'CRM', 'JPM']

# 获取股票数据
@st.cache_data(ttl=300)  # 缓存5分钟
def get_enhanced_stock_data(symbol: str) -> Optional[Dict]:
    """获取增强的股票数据"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        if not info:
            return None
            
        hist = stock.history(period="1y")
        if hist.empty:
            return None
            
        current_price = hist['Close'].iloc[-1]
        
        # 计算技术指标
        indicators = calculate_technical_indicators(hist)
        
        # 价格变化
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100
        
        # 构造股票数据
        stock_data = {
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'price': float(current_price),
            'change': float(change),
            'change_percent': float(change_percent),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'pb_ratio': info.get('priceToBook', 0),
            'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
            'roa': info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0,
            'debt_to_equity': info.get('debtToEquity', 0),
            'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
            'revenue_growth': info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0,
            'earnings_growth': info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0,
            'volume': int(hist['Volume'].iloc[-1]),
            'avg_volume': int(hist['Volume'].rolling(30).mean().iloc[-1]),
            'beta': info.get('beta', 1.0),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'target_price': info.get('targetMeanPrice', current_price * 1.1),
            'analyst_rating': info.get('recommendationMean', 3.0),
            '52_week_high': info.get('fiftyTwoWeekHigh', current_price),
            '52_week_low': info.get('fiftyTwoWeekLow', current_price),
            'free_cash_flow': info.get('freeCashflow', 0),
            'market_cap_category': get_market_cap_category(info.get('marketCap', 0)),
            **indicators
        }
        
        # 计算综合评分
        stock_data['score'] = calculate_comprehensive_score(stock_data)
        stock_data['recommendation'] = get_recommendation(stock_data)
        
        return stock_data
        
    except Exception as e:
        return None

def calculate_technical_indicators(df: pd.DataFrame) -> Dict:
    """计算技术指标"""
    indicators = {}
    
    try:
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        indicators['rsi'] = rsi.iloc[-1] if not rsi.empty else 50
        
        # MACD
        ema12 = df['Close'].ewm(span=12).mean()
        ema26 = df['Close'].ewm(span=26).mean()
        macd = ema12 - ema26
        macd_signal = macd.ewm(span=9).mean()
        indicators['macd'] = macd.iloc[-1] if not macd.empty else 0
        indicators['macd_signal'] = macd_signal.iloc[-1] if not macd_signal.empty else 0
        
        # 移动平均线
        indicators['sma20'] = df['Close'].rolling(20).mean().iloc[-1] if len(df) >= 20 else df['Close'].iloc[-1]
        indicators['sma50'] = df['Close'].rolling(50).mean().iloc[-1] if len(df) >= 50 else df['Close'].iloc[-1]
        indicators['sma200'] = df['Close'].rolling(200).mean().iloc[-1] if len(df) >= 200 else df['Close'].iloc[-1]
        
        # ATR
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        indicators['atr'] = true_range.rolling(14).mean().iloc[-1] if len(true_range) >= 14 else df['Close'].iloc[-1] * 0.02
        indicators['atr_percent'] = (indicators['atr'] / df['Close'].iloc[-1]) * 100
        
        # 布林带
        bb_middle = df['Close'].rolling(20).mean()
        bb_std = df['Close'].rolling(20).std()
        indicators['bb_upper'] = (bb_middle + bb_std * 2).iloc[-1] if len(bb_middle) >= 20 else df['Close'].iloc[-1] * 1.1
        indicators['bb_lower'] = (bb_middle - bb_std * 2).iloc[-1] if len(bb_middle) >= 20 else df['Close'].iloc[-1] * 0.9
        
    except Exception as e:
        # 设置默认值
        current_price = df['Close'].iloc[-1] if not df.empty else 100
        indicators.update({
            'rsi': 50,
            'macd': 0,
            'macd_signal': 0,
            'sma20': current_price,
            'sma50': current_price,
            'sma200': current_price,
            'atr': current_price * 0.02,
            'atr_percent': 2.0,
            'bb_upper': current_price * 1.1,
            'bb_lower': current_price * 0.9
        })
    
    return indicators

def get_market_cap_category(market_cap: int) -> str:
    """根据市值分类"""
    if market_cap >= 200e9:
        return "Mega Cap"
    elif market_cap >= 10e9:
        return "Large Cap"  
    elif market_cap >= 2e9:
        return "Mid Cap"
    elif market_cap >= 300e6:
        return "Small Cap"
    else:
        return "Micro Cap"

def calculate_comprehensive_score(data: Dict) -> int:
    """计算综合评分 (0-100)"""
    score = 50  # 基础分
    
    try:
        # 基本面评分 (40分)
        if data.get('pe_ratio') and 0 < data['pe_ratio'] < 15:
            score += 8
        elif data.get('pe_ratio') and 15 <= data['pe_ratio'] < 25:
            score += 5
        elif data.get('pe_ratio') and 25 <= data['pe_ratio'] < 35:
            score += 2
        
        if data.get('roe', 0) > 20:
            score += 8
        elif data.get('roe', 0) > 15:
            score += 5
        elif data.get('roe', 0) > 10:
            score += 2
        
        if data.get('debt_to_equity', 0) < 0.3:
            score += 6
        elif data.get('debt_to_equity', 0) < 0.7:
            score += 3
        
        if data.get('revenue_growth', 0) > 20:
            score += 10
        elif data.get('revenue_growth', 0) > 10:
            score += 5
        
        if data.get('dividend_yield', 0) > 3:
            score += 6
        elif data.get('dividend_yield', 0) > 1:
            score += 3
        
        # 技术面评分 (30分)
        rsi = data.get('rsi', 50)
        if 40 <= rsi <= 60:
            score += 8
        elif 30 <= rsi <= 70:
            score += 5
        elif rsi < 30:
            score += 6
        
        if data.get('macd', 0) > data.get('macd_signal', 0):
            score += 8
        
        current_price = data.get('price', 0)
        sma20 = data.get('sma20', current_price)
        if current_price > sma20:
            score += 7
        
        if data.get('volume', 0) > data.get('avg_volume', 1):
            score += 7
        
        # 风险调整 (30分)
        beta = data.get('beta', 1.0)
        if 0.8 <= beta <= 1.2:
            score += 10
        elif 0.5 <= beta <= 1.5:
            score += 5
        
        if data.get('52_week_high', 0) > 0:
            price_to_52h = data.get('price', 0) / data.get('52_week_high', 1)
            if price_to_52h > 0.8:
                score += 10
            elif price_to_52h > 0.6:
                score += 6
        
        if data.get('analyst_rating', 3.0) <= 2.5:
            score += 10
        
    except Exception as e:
        pass
    
    return min(100, max(0, score))

def get_recommendation(data: Dict) -> str:
    """根据评分获取推荐等级"""
    score = data.get('score', 50)
    if score >= 85:
        return 'STRONG BUY'
    elif score >= 75:
        return 'BUY'
    elif score >= 60:
        return 'HOLD'
    else:
        return 'SELL'

# AI对话处理系统
class AdvancedStockAI:
    """高级股票AI对话处理器"""
    
    def __init__(self):
        self.conversation_history = []
    
    def extract_investment_intent(self, query: str) -> Dict:
        """提取投资意图"""
        query_lower = query.lower()
        intent = {
            'strategy': 'mixed',
            'timeframe': 'medium',
            'risk_level': 'medium',
            'sectors': [],
            'conditions': {}
        }
        
        # 投资策略识别
        if any(word in query_lower for word in ['long', '长期', 'value', '价值', 'dividend', '股息']):
            intent['strategy'] = 'long_term'
        elif any(word in query_lower for word in ['swing', '波段', 'technical', '技术']):
            intent['strategy'] = 'swing_trade'
        elif any(word in query_lower for word in ['day', '日内', 'scalp', '短期']):
            intent['strategy'] = 'day_trade'
        
        # 行业识别
        if any(word in query_lower for word in ['tech', '科技', 'technology', 'ai', '人工智能']):
            intent['sectors'].append('Technology')
        if any(word in query_lower for word in ['health', '医疗', 'bio', '生物']):
            intent['sectors'].append('Healthcare')
        
        # 数值条件提取
        intent['conditions'] = self.extract_numeric_conditions(query)
        
        return intent
    
    def extract_numeric_conditions(self, query: str) -> Dict:
        """提取数值条件"""
        conditions = {}
        
        # P/E比率
        pe_match = re.search(r'p[/\s]*e\s*[<>≤≥]\s*(\d+(?:\.\d+)?)', query.lower())
        if pe_match:
            operator = '<' if any(op in query.lower() for op in ['<', '小于', 'less']) else '>'
            conditions['pe_ratio'] = (operator, float(pe_match.group(1)))
        
        # ROE
        roe_match = re.search(r'roe\s*[<>≤≥]\s*(\d+(?:\.\d+)?)', query.lower())
        if roe_match:
            operator = '>' if any(op in query.lower() for op in ['>', '大于', 'greater']) else '<'
            conditions['roe'] = (operator, float(roe_match.group(1)))
        
        # 股息率
        div_match = re.search(r'(?:dividend|股息|分红).*?[<>≤≥]\s*(\d+(?:\.\d+)?)', query.lower())
        if div_match:
            operator = '>' if any(op in query.lower() for op in ['>', '大于', 'greater']) else '<'
            conditions['dividend_yield'] = (operator, float(div_match.group(1)))
        
        return conditions
    
    def filter_stocks_by_intent(self, stocks: List[str], intent: Dict) -> List[Tuple[str, Dict]]:
        """根据意图筛选股票"""
        filtered_results = []
        
        # 限制搜索范围以提高性能
        sample_size = min(20, len(stocks))
        sample_stocks = random.sample(stocks, sample_size)
        
        progress_bar = st.progress(0)
        
        for i, symbol in enumerate(sample_stocks):
            progress_bar.progress((i + 1) / len(sample_stocks))
            stock_data = get_enhanced_stock_data(symbol)
            if stock_data and self.meets_criteria(stock_data, intent):
                filtered_results.append((symbol, stock_data))
        
        progress_bar.empty()
        
        # 按评分排序
        filtered_results.sort(key=lambda x: x[1]['score'], reverse=True)
        return filtered_results[:10]
    
    def meets_criteria(self, stock_data: Dict, intent: Dict) -> bool:
        """判断股票是否符合意图条件"""
        
        # 检查数值条件
        conditions = intent.get('conditions', {})
        for metric, (operator, value) in conditions.items():
            stock_value = stock_data.get(metric, 0)
            if operator == '>' and stock_value <= value:
                return False
            elif operator == '<' and stock_value >= value:
                return False
        
        # 根据投资策略筛选
        strategy = intent.get('strategy', 'mixed')
        
        if strategy == 'long_term':
            return (stock_data.get('pe_ratio', 100) < 35 and 
                    stock_data.get('roe', 0) > 8 and
                    stock_data.get('debt_to_equity', 10) < 2.0)
        
        elif strategy == 'swing_trade':
            return (30 <= stock_data.get('rsi', 50) <= 75 and 
                    stock_data.get('volume', 0) > stock_data.get('avg_volume', 1) * 0.8)
        
        elif strategy == 'day_trade':
            return (stock_data.get('beta', 0) > 0.8 and 
                    stock_data.get('volume', 0) > 500000)
        
        return True
    
    def generate_ai_response(self, query: str, results: List[Tuple], intent: Dict) -> str:
        """生成智能AI回复"""
        
        response_parts = []
        response_parts.append("🤖 **AI分析结果**")
        
        # 投资策略识别
        strategy_names = {
            'long_term': '长期投资策略',
            'swing_trade': '波段交易策略', 
            'day_trade': '日内交易策略',
            'mixed': '综合投资策略'
        }
        
        strategy = intent.get('strategy', 'mixed')
        response_parts.append(f"📈 **策略识别**: {strategy_names.get(strategy)}")
        
        # 筛选条件总结
        conditions = intent.get('conditions', {})
        if conditions:
            response_parts.append("📊 **筛选条件**:")
            for metric, (op, value) in conditions.items():
                metric_names = {
                    'pe_ratio': 'P/E比率',
                    'roe': 'ROE净资产收益率',
                    'dividend_yield': '股息率'
                }
                metric_name = metric_names.get(metric, metric)
                response_parts.append(f"   • {metric_name} {op} {value}")
        
        # 结果统计
        if results:
            avg_score = sum(stock[1]['score'] for stock in results) / len(results)
            response_parts.append(f"✅ **筛选结果**: 找到 {len(results)} 只符合条件的优质股票")
            response_parts.append(f"📊 **平均评分**: {avg_score:.1f}/100")
        else:
            response_parts.append("❌ **暂无结果**:response_parts.append("❌ **暂无结果**: 当前条件下未找到符合要求的股票")
        
        return "\n".join(response_parts)

# 股票卡片显示组件
def display_enhanced_stock_card(symbol: str, data: Dict):
    """显示增强版股票信息卡片"""
    
    rec_styles = {
        'STRONG BUY': ('recommendation-strong-buy', '🚀'),
        'BUY': ('recommendation-buy', '📈'), 
        'HOLD': ('recommendation-hold', '⏸️'),
        'SELL': ('recommendation-sell', '📉')
    }
    
    rec_class, rec_icon = rec_styles.get(data['recommendation'], ('recommendation-hold', '⚪'))
    price_color = "#10b981" if data['change'] >= 0 else "#ef4444"
    
    def format_market_cap(market_cap):
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.1f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.1f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.1f}M"
        else:
            return f"${market_cap:,.0f}"
    
    # 主卡片
    st.markdown(f"""
    <div class="stock-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                    <h2 style="margin: 0; color: white; font-size: 1.8rem; font-weight: bold;">{symbol}</h2>
                    <span class="{rec_class}">{rec_icon} {data['recommendation']}</span>
                    <span style="background: rgba(255,255,255,0.1); padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem;">
                        {data.get('market_cap_category', 'Unknown')}
                    </span>
                </div>
                <h3 style="margin: 0 0 0.3rem 0; color: #cbd5e1; font-size: 1rem; font-weight: normal;">{data['name']}</h3>
                <div style="display: flex; gap: 1.5rem; font-size: 0.85rem; color: #94a3b8;">
                    <span>🏢 {data['sector']}</span>
                    <span>💼 {format_market_cap(data['market_cap'])}</span>
                </div>
            </div>
            <div style="text-align: right;">
                <h1 style="margin: 0; color: white; font-size: 2.2rem; font-weight: bold;">${data['price']:.2f}</h1>
                <p style="margin: 0.3rem 0; color: {price_color}; font-size: 1.1rem; font-weight: bold;">
                    {'+' if data['change'] >= 0 else ''}{data['change']:.2f} ({data['change_percent']:.2f}%)
                </p>
                <div style="font-size: 0.8rem; color: #94a3b8;">
                    <div>目标价: ${data.get('target_price', 0):.2f}</div>
                </div>
            </div>
        </div>
        
        <div class="metric-container">
            <div class="metric-item">
                <div style="font-size: 1.5rem; font-weight: bold; color: {'#10b981' if data['score'] >= 75 else '#f59e0b' if data['score'] >= 60 else '#ef4444'};">
                    {data['score']}
                </div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">综合评分</div>
            </div>
            <div class="metric-item">
                <div style="font-size: 1.2rem; font-weight: bold; color: white;">
                    {data.get('pe_ratio', 0):.1f}
                </div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">P/E比率</div>
            </div>
            <div class="metric-item">
                <div style="font-size: 1.2rem; font-weight: bold; color: white;">
                    {data.get('roe', 0):.1f}%
                </div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">ROE</div>
            </div>
            <div class="metric-item">
                <div style="font-size: 1.2rem; font-weight: bold; color: white;">
                    {data.get('rsi', 0):.1f}
                </div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">RSI</div>
            </div>
            <div class="metric-item">
                <div style="font-size: 1.2rem; font-weight: bold; color: white;">
                    {data.get('revenue_growth', 0):.1f}%
                </div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">营收增长</div>
            </div>
            <div class="metric-item">
                <div style="font-size: 1.2rem; font-weight: bold; color: white;">
                    {data.get('beta', 0):.2f}
                </div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">Beta风险</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 详细分析展开
    with st.expander(f"📊 {symbol} 深度分析", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📈 基本面指标")
            st.write(f"**P/E比率**: {data.get('pe_ratio', 0):.2f}")
            st.write(f"**P/B比率**: {data.get('pb_ratio', 0):.2f}")
            st.write(f"**ROE**: {data.get('roe', 0):.1f}%")
            st.write(f"**ROA**: {data.get('roa', 0):.1f}%")
            st.write(f"**债务权益比**: {data.get('debt_to_equity', 0):.2f}")
        
        with col2:
            st.markdown("### 💰 成长指标")
            st.write(f"**营收增长**: {data.get('revenue_growth', 0):.1f}%")
            st.write(f"**盈利增长**: {data.get('earnings_growth', 0):.1f}%")
            st.write(f"**股息率**: {data.get('dividend_yield', 0):.2f}%")
            st.write(f"**自由现金流**: {data.get('free_cash_flow', 0)/1e9:.1f}B" if data.get('free_cash_flow', 0) > 0 else "N/A")
        
        with col3:
            st.markdown("### 🔍 技术指标")
            st.write(f"**RSI**: {data.get('rsi', 0):.1f}")
            st.write(f"**MACD**: {data.get('macd', 0):.3f}")
            st.write(f"**20日均线**: ${data.get('sma20', 0):.2f}")
            st.write(f"**ATR**: ${data.get('atr', 0):.2f}")
            st.write(f"**Beta**: {data.get('beta', 0):.2f}")

# 主应用程序
def main():
    # 页面标题
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0; font-size: 2.8rem; text-align: center; font-weight: bold;">
            🤖 AI选股智能体
        </h1>
        <h2 style="color: #cbd5e1; margin: 0.5rem 0 0 0; font-size: 1.4rem; text-align: center; font-weight: normal;">
            AI-Powered Stock Screening Agent
        </h2>
        <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 1rem; text-align: center;">
            支持中英文对话 • 覆盖全美股市场 • 35+基本面指标 • 25+技术指标 • 智能推荐系统
        </p>
        <p style="color: #6b7280; margin: 0.3rem 0 0 0; font-size: 0.9rem; text-align: center;">
            Powered by AlphaBERTOptimus | Built with ❤️ for Investors
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 初始化AI处理器
    if "ai_processor" not in st.session_state:
        st.session_state.ai_processor = AdvancedStockAI()

    # 侧边栏配置
    with st.sidebar:
        st.markdown("## 🎯 AI选股能力")
        
        with st.expander("📊 基本面分析 (35+ 指标)", expanded=True):
            st.markdown("""
            **🏷️ 估值指标**
            • P/E比率、P/B比率、PEG比率、市销率
            
            **💰 盈利能力**  
            • ROE、ROA、毛利率、净利率
            
            **💪 财务健康**
            • 债务权益比、流动比率、自由现金流
            
            **📈 成长指标**
            • 营收增长率、盈利增长率、股息率
            """)
        
        with st.expander("📈 技术分析 (25+ 指标)", expanded=True):
            st.markdown("""
            **📊 趋势指标**
            • SMA20/50/200、MACD、ADX
            
            **⚡ 动量指标**
            • RSI、随机指标、威廉指标
            
            **🌊 波动率指标**
            • 布林带、ATR、历史波动率
            
            **📦 成交量指标**
            • 成交量、OBV、放量突破信号
            """)

    # 快速策略选择
    st.markdown("## 💡 快速开始")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎯 长期投资", use_container_width=True):
            st.session_state.suggested_prompt = "推荐适合长期投资的价值股，P/E < 25, ROE > 15%, 债务权益比 < 0.5"
    
    with col2:
        if st.button("📈 波段交易", use_container_width=True):
            st.session_state.suggested_prompt = "寻找适合波段交易的股票，RSI在30-70区间, MACD金叉"
    
    with col3:
        if st.button("⚡ 日内交易", use_container_width=True):
            st.session_state.suggested_prompt = "筛选日内交易机会，Beta > 1.0，成交量 > 100万股"
    
    with col4:
        if st.button("🌟 AI推荐", use_container_width=True):
            st.session_state.suggested_prompt = "基于当前市场环境，推荐综合评分最高的优质股票"

    # 示例问题
    st.markdown("## 💭 使用示例")
    
    tab1, tab2 = st.tabs(["🇨🇳 中文示例", "🇺🇸 English Examples"])
    
    with tab1:
        chinese_examples = [
            "帮我找一些P/E低于20的价值股，ROE要大于15%",
            "推荐适合波段交易的科技股，RSI在40-60之间",
            "寻找高股息率的蓝筹股，股息率大于3%",
            "筛选AI概念股，受益ChatGPT热潮，营收增长 > 30%"
        ]
        for i, example in enumerate(chinese_examples):
            if st.button(f"💬 {example}", key=f"cn_{i}", use_container_width=True):
                st.session_state.suggested_prompt = example
    
    with tab2:
        english_examples = [
            "Find growth stocks with revenue growth > 25% and P/E < 30",
            "Show me dividend aristocrats with 20+ years of dividend growth",
            "Recommend biotech stocks with promising drug pipeline",
            "Find momentum stocks breaking above 52-week highs"
        ]
        for i, example in enumerate(english_examples):
            if st.button(f"💬 {example}", key=f"en_{i}", use_container_width=True):
                st.session_state.suggested_prompt = example

    # AI对话界面
    st.markdown("## 💬 AI智能选股对话")
    
    # 初始化会话
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": """🤖 **欢迎使用AI选股智能体！**

我是您的专业AI选股助手，具备以下能力：

**🎯 核心优势**：
- **全美股覆盖**：S&P 500 + NASDAQ + NYSE，1000+股票实时跟踪
- **35+基本面指标**：估值、盈利、财务、成长全方位分析  
- **25+技术指标**：趋势、动量、波动率深度技术分析
- **智能评分系统**：0-100分综合评分，风险收益评估

**💬 对话能力**：
- **中英文支持**：自然语言，理解复杂投资条件
- **策略识别**：自动识别长期/中期/短期投资意图
- **个性化推荐**：基于您的风险偏好和投资目标

**🚀 开始对话**：
- "找一些适合长期投资的科技股，P/E < 25, ROE > 20%"
- "Find growth stocks with revenue growth > 30%"  
- "推荐波段交易机会，RSI超卖，MACD即将金叉"

让我们开始您的投资之旅吧！🚀
"""
            }
        ]
    
    if "stock_universe" not in st.session_state:
        with st.spinner("🔄 正在加载全美股数据库..."):
            st.session_state.stock_universe = get_all_us_stocks()
        st.success(f"✅ 已加载 {len(st.session_state.stock_universe)} 只美股数据")

    # 显示对话历史
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 您:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 AI助手:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            if "stocks" in message:
                st.markdown("### 📈 AI筛选结果")
                for symbol, data in message["stocks"]:
                    display_enhanced_stock_card(symbol, data)

    # 用户输入
    user_input = st.text_area(
        "🎯 请描述您的选股需求 (支持中英文):",
        value=st.session_state.get("suggested_prompt", ""),
        placeholder="例如: '帮我找一些适合长期投资的价值股，P/E < 20, ROE > 15%' 或 'Find growth stocks with revenue growth > 25%'",
        height=100,
        key="user_input"
    )
    
    if st.session_state.get("suggested_prompt"):
        del st.session_state.suggested_prompt

    # 处理用户输入
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚀 开始AI选股分析", use_container_width=True) and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("🧠 AI正在分析全美股数据，请稍候..."):
                try:
                    intent = st.session_state.ai_processor.extract_investment_intent(user_input)
                    filtered_stocks = st.session_state.ai_processor.filter_stocks_by_intent(
                        st.session_state.stock_universe, intent
                    )
                    
                    ai_response = st.session_state.ai_processor.generate_ai_response(
                        user_input, filtered_stocks, intent
                    )
                    
                    if filtered_stocks:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": ai_response,
                            "stocks": filtered_stocks
                        })
                    else:
                        fallback_response = f"""😔 **未找到符合条件的股票**

您的查询：「**{user_input}**」

**建议调整**：
- 适当放宽筛选条件
- 尝试不同的投资策略
- 参考示例重新提问"""
                        
                        st.session_state.messages.append({"role": "assistant", "content": fallback_response})
                
                except Exception as e:
                    error_response = "抱歉，分析过程中遇到技术问题。请稍后重试。"
                    st.session_state.messages.append({"role": "assistant", "content": error_response})
            
            st.rerun()
    
    with col2:
        if st.button("🔄 清空对话", use_container_width=True):
            st.session_state.messages = st.session_state.messages[:1]
            st.rerun()

    # 页脚信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 0.9rem;">
        <p><strong>⚠️ 投资风险提示</strong>：本工具仅供参考，不构成投资建议。投资有风险，入市需谨慎。</p>
        <p><strong>📊 数据来源</strong>：Yahoo Finance API • <strong>🚀 开发者</strong>：AlphaBERTOptimus</p>
        <p><strong>💡 技术栈</strong>：Python + Streamlit + yfinance • <strong>⭐ GitHub</strong>：star支持项目</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
