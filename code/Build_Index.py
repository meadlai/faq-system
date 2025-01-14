
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import OutlookMessageLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv

import os

# load environment variables
load_dotenv()

# init Azure OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")

OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME = os.getenv("OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME")
OPENAI_ADA_EMBEDDING_MODEL_NAME = os.getenv("OPENAI_ADA_EMBEDDING_MODEL_NAME")

FAQ_BASE_DOCS_PATH = os.getenv("FAQ_BASE_DOCS_PATH")
FAQ_BASE_INDEX_PATH = os.getenv("FAQ_BASE_INDEX_PATH")
FAQ_BASE_EMAIL_PATH = os.getenv("FAQ_BASE_EMAIL_PATH")


if __name__ == "__main__":

    print('Embeddings...')
    # init vector engine
    embeddings = AzureOpenAIEmbeddings(deployment=OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME,
                                  model=OPENAI_ADA_EMBEDDING_MODEL_NAME,
                                  azure_endpoint=OPENAI_DEPLOYMENT_ENDPOINT,
                                  openai_api_type="azure",
                                  chunk_size=1)
    print('Loading documents...')
    # Load Documents
    documents = []
    for root, dirs, files in os.walk(FAQ_BASE_DOCS_PATH):
        for file in files:
            # conjunct the full file path
            file_path = os.path.join(root, file)
            print('      Loading file_path: ', file_path)
            if file.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith('.txt') or file.endswith('.md'):
                loader = TextLoader(file_path)
                documents.extend(loader.load())

    # Load Emails
    print('Loading Emails...')
    # emailLoader = DirectoryLoader(path=FAQ_BASE_EMAIL_PATH, glob='**/*.msg',
    #     show_progress=True, loader_cls=OutlookMessageLoader)
    # documents.extend(emailLoader.load())
    print('Documents Load Completed ')

    # Split doc to chunks
    print('Splitting...')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
    chunked_documents = text_splitter.split_documents(documents)
    print(f'Splitting completed. Number of chunks: {len(chunked_documents)}')

    if not chunked_documents:
        print('No documents were split into chunks. Please check the document loading process.')
    else:
        print('Indexing')
        # Use Langchain to create the embeddings using text-embedding-ada-002
        db = FAISS.from_documents(documents=chunked_documents, embedding=embeddings)
        print('Embedding pages')

        # save the embeddings into FAISS vector store
        db.save_local(FAQ_BASE_INDEX_PATH)
        print('Saved Index data')
