from asyncio.log import logger
from xml.dom.minidom import Document

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from Agent_sample.utils.file_handler import get_file_md5_hex, listdir_with_allowed_type, pdf_loader, text_loader
from Agent_sample.utils.path_tool import get_abs_path
from utils.config_handler import chroma_config
from model.factory import embedding_model 
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os




class VectorStoreService:
    def __init__(self):
        # Initialize the vector store service

        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_config["persist_directory"]
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separator"],
            length_function=len
        )

#返回向量检索器，方便加入链
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["similarity_threshold"]})  

    def load_documents(self):


        def check_md5_hex(md5_for_check):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]), "w").close()
                return False
            with open(get_abs_path(chroma_config["md5_hex_store"]), "r") as f:
                for line in f.readlines():
                    if line.strip() == md5_for_check:
                        return True
                return False
        def save_md5_hex(md5_for_save):
                with open(get_abs_path(chroma_config["md5_hex_store"]), "a") as f:
                    f.write(md5_for_save + "\n")

        def get_file_documents(read_path):
            if read_path.endswith(".txt"):
                return text_loader(read_path)
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            return []

        #NOTE:理解就行，剩下的

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            # 获取文件的MD5
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理完成文件的md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功")

            except Exception as e:
                # exc_info为True会记录详细的报错信息，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue

        
        
