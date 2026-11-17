import hashlib
import os
from utils.logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_core.documents import Document


def get_file_md5_hex(file_path: str) -> str:
    """
    计算文件的MD5值，并返回16进制字符串表示
    :param file_path: 文件路径
    :return: 文件的MD5值的16进制字符串表示
    """
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return 
    if not os.path.isfile(file_path):
        logger.error(f"路径不是文件: {file_path}")
        return
    
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # 分块读取文件内容，避免一次性读取大文件导致内存占用过高
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def listdir_with_allowed_type(path:str, allowed_types: tuple[str]): #负担会文件夹内的文件列表
    files = []
    if not os.path.isdir(path):
        logger.error(f"路径不是文件夹: {path}")
        return allowed_types

    for file in os.listdir(path):
        if file.endswith(allowed_types):
            files.append(os.path.join(path, file))
    return tuple(files)

def pdf_loader(filepath:str,passwd=None):
    loader = PyPDFLoader(filepath, password=passwd)
    return loader.load()

def text_loader(filepath:str):
    loader = TextLoader(filepath)
    return loader.load()