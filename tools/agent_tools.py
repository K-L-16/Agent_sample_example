from langchain_core.tools import tool
from Agent_sample.utils.path_tool import get_abs_path
from rag.rag_service import RagSummarizeService
import random
rag = RagSummarizeService()
from utils.config_handler import agent_config
from utils.logger_handler import logger
import os

external_data = {}

@tool(description="从知识库中检索相关信息并进行总结，输入为用户的查询问题，输出为总结结果。")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气信息，输入为城市名称，输出为天气信息。")
def get_weather(city: str) -> str:
    # 这里可以调用天气API获取天气信息
    return f"当前{city}的天气是晴天，温度25摄氏度。"

@tool(description="获取用户城市的名称")
def get_user_location() -> str:
    return random.choice(["北京", "上海", "广州", "深圳", "杭州"])

@tool(description="获取用户的id")
def get_user_id() -> str:
    return f"user_{random.randint(1000, 9999)}"

@tool(description="获取当前的月份")
def get_current_month() -> str:
    return f"当前月份是{random.randint(1, 12)}月"

def generate_external_data():
      if not external_data:
        external_data_path = get_abs_path(agent_config["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回，如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""





@tool(description="从外部系统中获取用户的使用记录，以字符串形式返回")
def get_user_usage_records() -> str:
    return f"用户使用记录：{random.randint(1, 100)}次"