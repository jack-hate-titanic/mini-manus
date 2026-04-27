import logging

from fastapi import FastAPI
from core.config import get_settings
from app.infrastructure.endpoints.routes import router as api_router
from app.infrastructure.logging import setup_logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.errors.exception_handlers import register_exception_handlers




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

    try:
        # lifespan节点/分界
        yield
    finally:
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