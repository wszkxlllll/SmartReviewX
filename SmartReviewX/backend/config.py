from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # 应用基本设置
    APP_NAME: str = "Review Generator API"
    DEBUG: bool = True
    HOST: str = "47.108.197.221"
    PORT: int = 8000
    # 文件存储设置
    REVIEWS_SAVE_PATH: str = "data/reviews"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Data Generator"
    
   # OpenAI配置
    OPENAI_API_KEY1: str = ""# 请替换为你的 华东师范大学 API密钥
    #OPENAI_API_KEY2: str = ""# 请替换为你的 Openai API密钥
    OPENAI_API_KEY2: str = ""#请替换为你的 moonshot API密钥
    OPENAI_API_KEY3: str = ""# 请替换为你的 Deepseek API密钥
    OPENAI_API_BASE1: str = "https://chat.ecnu.edu.cn/open/api/v1"
    #OPENAI_API_BASE2: str = "https://api.openai.com/v1"
    OPENAI_API_BASE2: str = "https://api.moonshot.cn/v1"
    OPENAI_API_BASE3: str = "https://api.deepseek.com"
    OPENAI_API_MODEL1: str = "ecnu-plus"  # 使用华东师范大学的模型
    OPENAI_API_MODEL2: str = "moonshot-v1-auto"  # 使用 moonshot的模型
    OPENAI_API_MODEL3: str = "deepseek-chat"  # 使用Deepseek的模型
    # 大模型配置
    LLM_TEMPERATURE: float = 0.7
    LLM_TOP_P: float = 0.9
    LLM_MAX_TOKENS: int = 2000
    LLM_FREQUENCY_PENALTY: float = 0.0
    LLM_PRESENCE_PENALTY: float = 0.0
    
    # 评价生成配置
    MAX_REVIEW_LENGTH: int = 1000
    MIN_REVIEW_LENGTH: int = 200
    MAX_RETRIES: int = 3
    QUALITY_THRESHOLD: float = 0.8
    SENTIMENT_THRESHOLD: float = 0.8
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data.db"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # 数据生成配置
    MAX_GENERATION_LENGTH: int = 1000
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    
    # 异步任务配置
    TASK_TIMEOUT: int = 300  # 5分钟
    TASK_CLEANUP_INTERVAL: int = 3600  # 1小时
    
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 
