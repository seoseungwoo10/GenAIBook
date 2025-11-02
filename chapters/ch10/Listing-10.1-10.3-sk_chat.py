# 모듈 설명: Listing 10.1-10.3 - Semantic Kernel과 ChromaDB를 사용한 RAG 예제
# - PDF 파일을 로드하고 각 페이지를 ChromaDB에 임베딩하여 저장합니다.
# - 사용자 질문에 대해 벡터 검색으로 관련 문서를 찾고 LLM에 컨텍스트로 제공합니다.
# - Azure OpenAI의 Chat Completion과 Text Embedding을 사용

# needs these packages installed
# conda install chromadb=0.4.15
# pip install chromadb==0.4.15
# pip install semantic-kernel==1.2.0
# pip install PyPDF2==3.0.1

import os
import warnings
import asyncio
from PyPDF2 import PdfReader
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (AzureChatCompletion,AzureTextEmbedding)
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
from tqdm import tqdm
import tqdm.asyncio as tqdm_asyncio

warnings.filterwarnings("ignore")

# Load environment variables
AOAI_KEY = os.getenv("AOAI_KEY")
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_MODEL = "gpt-35-turbo"
AOAI_EMBEDDINGS = "text-embedding-ada-002"
API_VERSION = '2023-09-15-preview'

PERSIST_DIR = os.getenv("PERSIST_DIR")
VECTOR_DB = os.getenv("VECTOR_DB")

DOG_BOOKS = "./data/dog_books"
DEBUG = True
VECTOR_DB = "dog_books"
PERSIST_DIR = "./storage"
ALWAYS_CREATE_VECTOR_DB = False

# Load PDFs and extract text
# PDF 파일들을 로드하고 각 페이지의 텍스트를 추출
def load_pdfs():
    docs = []
    total_docs = 0
    total_pages = 0
    filenames = [filename for filename in os.listdir(DOG_BOOKS) if filename.endswith(".pdf")]
    with tqdm(total=len(filenames), desc="Processing PDFs") as pbar_outer:
        for filename in filenames:
            pdf_path = os.path.join(DOG_BOOKS, filename)
            with open(pdf_path, "rb") as file:
                pdf = PdfReader(file, strict=False)
                j = 0
                total_docs += 1
                with tqdm(total=len(pdf.pages), desc="Loading Pages") as pbar_inner:
                    for page in pdf.pages:
                        total_pages += 1
                        j += 1
                        docs.append(page.extract_text())
                        pbar_inner.update()
                pbar_outer.update()
    print(f"Processed {total_docs} PDFs with {total_pages} pages.")
    return docs

# Populate the DB with the PDFs
# 추출한 텍스트를 벡터 DB에 저장 (임베딩 생성 및 저장)
async def populate_db(memory: SemanticTextMemory, docs) -> None:
    for i, doc in enumerate(tqdm_asyncio.tqdm(docs, desc="Populating DB")):
        if doc:  # Check if doc is not empty
            try:
                await memory.save_information(VECTOR_DB, id=str(i), text=doc)
            except Exception as e:
                print(f"Failed to save information for doc {i}: {e}")
                continue  # Skip to the next iteration

# Check if user wants to quit
def check_prompt(user_input):
    if user_input.casefold() == "quit":
        exit()
    return user_input

# Load the vector DB
# 벡터 DB 로드 또는 생성 (이미 있으면 재사용, 없으면 PDF에서 생성)
async def load_vector_db(memory: SemanticTextMemory, vector_db_name: str) -> None:
    if not ALWAYS_CREATE_VECTOR_DB:
        collections = await memory.get_collections()
        if vector_db_name in collections:
            if DEBUG:
                print(f" Vector DB {vector_db_name} exists in the collections. We will reuse this.")
            return

    print(f" Vector DB {vector_db_name} does not exist in the collections.")
    print("Reading the pdfs...")

    pdf_docs = load_pdfs()
    print("Total PDFs loaded: ", len(pdf_docs))
    print("Creating embeddings and vector db of the PDFs...")

    # NOTE: this may take some time as we call OpenAI embedding API for each row
    await populate_db(memory, pdf_docs)

# Main function
async def main():
    if DEBUG:
        print("Starting...")
        print("AOAI_KEY: ", AOAI_KEY)
        print("AOAI_ENDPOINT: ", AOAI_ENDPOINT)
        print("AOAI_MODEL: ", AOAI_MODEL)
        print("AOAI_EMBEDDINGS: ", AOAI_EMBEDDINGS)
        print("API_VERSION: ", API_VERSION)
        print("PERSIST_DIR: ", PERSIST_DIR)
        print("VECTOR_DB: ", VECTOR_DB)
        print("DOG_BOOKS: ", DOG_BOOKS)
        
    # Setup Semantic Kernel
    # Semantic Kernel 초기화 (Chat Completion 및 Text Embedding 서비스 추가)
    kernel = sk.Kernel()
    kernel.add_service(
        AzureChatCompletion(
            service_id="chat_completion",
            deployment_name=AOAI_MODEL,
            endpoint=AOAI_ENDPOINT,
            api_key=AOAI_KEY,
            api_version=API_VERSION
        )
    )
    kernel.add_service(
        AzureTextEmbedding(
            service_id="text_embedding",
            deployment_name=AOAI_EMBEDDINGS,
            endpoint=AOAI_ENDPOINT,
            api_key=AOAI_KEY,
        )
    )

    if DEBUG:
        print("SK kernel loaded...")

    # Specify the type of memory to attach to SK. Here we will use Chroma as it is easy to run it locally
    # ChromaDB를 벡터 저장소로 사용 (로컬에서 실행 가능)
    store = ChromaMemoryStore(persist_directory=PERSIST_DIR)
    memory = SemanticTextMemory(
        storage=store, embeddings_generator=kernel.get_service("text_embedding")
    )
    kernel.add_plugin(TextMemoryPlugin(memory), "TextMemoryPluginACDB")

    await load_vector_db(memory, VECTOR_DB)
    if DEBUG:
        print("Vector DB loaded...")

    while True:
        prompt = check_prompt(
            input('Ask a question against the PDF (type "quit" to exit):')
        )
        if not prompt:
            continue  # 사용자 입력이 비어있으면 다시 입력 받음

        # Now query the memory for most relevant match using search_async specifying 
        # relevance score and "limit" of number of closest documents
        result = await memory.search(
            collection=VECTOR_DB, limit=3, min_relevance_score=0.7, query=prompt
        )
        if result:
            print(result[0].text)
        else:
            print("No matches found.")

        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(main())
