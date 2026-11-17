

from abc import ABC, abstractmethod
from typing import Optional

from chromadb import Embeddings
from langchain_openai import ChatOpenAI
from utils.config_handler import rag_config

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)->Optional[Embeddings | ChatOpenAI]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> ChatOpenAI:
        return ChatOpenAI(
            model_name=rag_config["model_name"],
            temperature=0,
            api_key=rag_config["api_key"]
        )

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Embeddings:
        return Embeddings(
            model=rag_config["embedding_model"],
            api_key=rag_config["embedding_api_key"],
            base_url="https://openrouter.ai/api/v1",
            check_embedding_ctx_length=False,
            chunk_size=1
        )
chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()