#为整个工程提供同意绝对路径

import os

def get_project_root() -> str:
    """获取项目根目录的绝对路径"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_abs_path(relative_path: str) -> str:
    """将相对路径转换为绝对路径"""
    return os.path.join(get_project_root(), relative_path)

