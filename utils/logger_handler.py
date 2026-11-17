import logging
import os
import datetime
from utils.path_tool import get_abs_path
#日志保存的根目录
LOG_ROOT = get_abs_path("logs")

os.makedirs(LOG_ROOT, exist_ok=True)

DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

def get_logger(
        name: str="agent", 
        console_level:int=logging.INFO,
        file_level:int=logging.DEBUG,
        log_file: str = None, 
        ) -> logging.Logger:
    """
    获取一个日志记录器
    :param name: 日志记录器的名称
    :param log_file: 日志文件的路径，如果为None，则不写入文件
    :param console_level: 控制台日志级别
    :param file_level: 文件日志级别 
    :return: 日志记录器对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置日志记录器的最低级别为DEBUG

    if logger.handlers:
        # 如果已经存在处理器，则不再添加新的处理器
        return logger

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger


#快捷获取日志
logger=get_logger()