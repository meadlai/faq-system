from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from dotenv import load_dotenv

import os

load_dotenv()

# init Azure OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME = os.getenv("OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME")
OPENAI_ADA_EMBEDDING_MODEL_NAME = os.getenv("OPENAI_ADA_EMBEDDING_MODEL_NAME")

FAQ_BASE_INDEX_PATH = os.getenv("FAQ_BASE_INDEX_PATH")


class FAQAPI:
    count = 0

    def __init__(self, indexPath=FAQ_BASE_INDEX_PATH):
        ##
        self._baseIndexPaTH = indexPath
        ##
        embeddings = OpenAIEmbeddings(deployment=OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME,
                                      model=OPENAI_ADA_EMBEDDING_MODEL_NAME,
                                      openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT,
                                      openai_api_type="azure",
                                      chunk_size=1)

        llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
                              model_name=OPENAI_MODEL_NAME,
                              openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT,
                              openai_api_version=OPENAI_DEPLOYMENT_VERSION,
                              openai_api_key=OPENAI_API_KEY,
                              openai_api_type="azure")

        vector_store = FAISS.load_local(self._baseIndexPaTH, embeddings)
        retriever_from_llm = MultiQueryRetriever.from_llm(retriever = vector_store.as_retriever(), llm=llm)
        self._qa_chain = RetrievalQA.from_chain_type(llm, retriever = retriever_from_llm)

    def ask_question(self, question):
        result = self._qa_chain({"query": question})
        ##print("Question:", question)
        ##print("Answer:", result["result"])
        return result["result"]
