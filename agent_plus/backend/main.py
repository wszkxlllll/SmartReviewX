import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from backend.service.routes import app
from backend.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # 使用stdout而不是默认的stderr
        logging.FileHandler('app.log', encoding='utf-8')  # 指定文件编码为utf-8
    ]
)

# 设置控制台输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    logger.info("Application starting...")  # 使用英文消息避免编码问题
    # 这里可以添加数据库连接等初始化操作

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理操作"""
    logger.info("Application shutting down...")  # 使用英文消息避免编码问题
    # 这里可以添加数据库断开连接等清理操作

if __name__ == "__main__":
    # 启动应用
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # 开发模式下启用热重载
        log_level="info"
    ) 