from utils.config_handler import prompts_config
from utils.path_tool import get_abs_path

def load_system_prompt() -> str:
    """
    加载系统提示词
    :return: 系统提示词字符串
    """
    prompt_path = get_abs_path(prompts_config.get("main_prompt_path", "prompts/main_prompt.txt"))
    with open(prompt_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    return system_prompt

def load_rag_summarize_prompt() -> str:
    """
    加载RAG总结提示词
    :return: RAG总结提示词字符串
    """
    prompt_path = get_abs_path(prompts_config.get("rag_summarize_prompt_path", "prompts/rag_summarize_prompt.txt"))
    with open(prompt_path, 'r', encoding='utf-8') as file:
        rag_summarize_prompt = file.read()
    return rag_summarize_prompt

def load_report_prompt() -> str:
    """
    加载报告提示词
    :return: 报告提示词字符串
    """
    prompt_path = get_abs_path(prompts_config.get("report_prompt_path", "prompts/report_prompt.txt"))
    with open(prompt_path, 'r', encoding='utf-8') as file:
        report_prompt = file.read()
    return report_prompt