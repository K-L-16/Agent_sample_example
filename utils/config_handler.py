import yaml
from utils.path_tool import get_abs_path

def load_rag_config(config_path: str = get_abs_path("config/rag.yaml"),encoding: str = 'utf-8') -> dict:
    """
    加载RAG配置文件
    :param config_path: 配置文件的路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file,Loader=yaml.FullLoader)
    return config

def load_chroma_config(config_path: str = get_abs_path("config/chroma.yaml"),encoding: str = 'utf-8') -> dict:
    """
    加载Chroma配置文件
    :param config_path: 配置文件的路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file,Loader=yaml.FullLoader)
    return config

def load_prompts_config(config_path: str = get_abs_path("config/prompts.yaml"),encoding: str = 'utf-8') -> dict:
    """
    加载Prompts配置文件
    :param config_path: 配置文件的路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file,Loader=yaml.FullLoader)
    return config

def load_agent_config(config_path: str = get_abs_path("config/agent.yaml"),encoding: str = 'utf-8') -> dict:
    """
    加载Agent配置文件
    :param config_path: 配置文件的路径
    :return: 配置字典
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file,Loader=yaml.FullLoader)
    return config

rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
agent_config = load_agent_config()