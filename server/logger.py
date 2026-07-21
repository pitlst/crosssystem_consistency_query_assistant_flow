import sys
from loguru import logger

# 配置 loguru 终端输出：彩色格式，详细的错误追踪信息打印到 stderr
logger.remove()
logger.add(
    sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    level="DEBUG",
    colorize=True,
    backtrace=True,
    diagnose=True,
)
