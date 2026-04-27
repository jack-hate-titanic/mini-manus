import logging
from fastapi import APIRouter
from app.interfaces.schemas import Response



logger = logging.getLogger(__name__)
router = APIRouter(prefix="/status", tags=["状态模块"])

@router.get(
    path="",
    summary="健康检查",
    description="检查系统的健康状态，返回系统是否正常运行。",
    response_model=Response[bool]
)
async def get_status():
    """
    健康检查接口，返回系统是否正常运行。
    """
    logger.info("执行健康检查")
    return Response.success(data=True, msg="系统正常运行")