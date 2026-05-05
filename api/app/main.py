'''
Author: 悦者生存 1002783067@qq.com
Date: 2026-05-01 22:02:48
LastEditors: 悦者生存 1002783067@qq.com
LastEditTime: 2026-05-03 19:53:35
FilePath: /mini-manus/api/app/main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import logging

from fastapi import FastAPI
from app.infrastructure.storage.redis import get_redis_client
from core.config import get_settings
from app.infrastructure.endpoints.routes import router as api_router
from app.infrastructure.logging import setup_logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.errors.exception_handlers import register_exception_handlers
from app.infrastructure.storage.cos import get_cos_client
from app.infrastructure.storage.postgres import get_postgres_client




# 1. 加载配置
settings = get_settings()

# 2. 初始化日志
setup_logging()
logger = logging.getLogger()

# 3. 定义fastapi路由tags标签
openai_tags = [
    {
        "name": '状态模块',
        "description": '包含 **状态监测** 等API接口， 用于监测系统的运行状态和健康状况。'
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('应用正在启动...')

    # 4. 初始化Redis连接
    redis_client = get_redis_client()
    await redis_client.init()

    # 5. 初始化PostgreSQL连接
    postgres_client = get_postgres_client()
    await postgres_client.init()

    # 6. cos客户端初始化
    cos_client = get_cos_client()
    await cos_client.init()


    try:
        # lifespan节点/分界
        yield
    finally:    
        await redis_client.close()  
        await postgres_client.close()
        await cos_client.close()
        logger.info('应用正在关闭...')

app = FastAPI(
    title="Manus API",
    description="Manus API 是一个基于 FastAPI 构建的接口服务，提供了与 OpenAI API 交互的功能，支持多种模型和功能模块。",
    version="1.0.0",
    openapi_tags=openai_tags,
    lifespan=lifespan
)


# 5.配置CORS中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_credentials=True,  # 允许携带凭证（如Cookies）
    allow_headers=["*"],  # 允许所有请求头
)

# 6.注册全局异常处理器·
register_exception_handlers(app)


app.include_router(api_router, prefix="/api")
