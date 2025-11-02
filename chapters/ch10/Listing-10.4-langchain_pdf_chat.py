# 모듈 설명: Listing 10.4 - LangChain을 사용한 PDF 문서 기반 Q&A 시스템
# - LangChain 프레임워크를 사용하여 PDF 문서에 대한 질문-답변 시스템 구축
# - FAISS 벡터 스토어로 문서 임베딩 저장 및 검색
# - OpenAI LLM과 연계하여 자연스러운 답변 생성
#
# 주요 개념:
# - LangChain: LLM 애플리케이션 개발을 위한 프레임워크
# - FAISS: Facebook AI의 벡터 유사도 검색 라이브러리 (빠른 검색 성능)
# - QA Chain: 질문-답변을 위한 LangChain의 체인 패턴
# - Document: LangChain의 문서 객체 (content + metadata)

# Needs the following installed:
# langchain                                  0.1.6
# langchain-community                        0.0.19
# langchain-core                             0.1.23
# langchain-openai                           0.0.6
# opentelemetry-instrumentation-langchain    0.14.3

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI, OpenAIEmbeddings
from tqdm import tqdm
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv('.env')
OPENAI_KEY = os.getenv('OPENAI_API_BOOK_KEY')
DOG_BOOKS = "./data/dog_books"
DEBUG = False

# Create the index
# FAISS 벡터 인덱스 생성
def create_index():
    try:
        # load the documents and create the index
        docs = load_pdfs()
        if not docs:
            print('No PDFs found.')
            return None
        
        # CharacterTextSplitter: 문자 수 기반 텍스트 분할
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=2048,  # 각 청크의 최대 문자 수
            chunk_overlap=200,  # 청크 간 중복 문자 수 (맥락 유지)
            length_function=len
        )
        
        # Convert the chunks of text into embeddings
        # 텍스트 청크를 임베딩으로 변환하여 FAISS 인덱스 생성
        print("Chunking and creating embeddings...")
        chunks = text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)

        # FAISS.from_documents: 문서들을 임베딩하여 벡터 DB 생성
        vectordb = FAISS.from_documents(chunks, embeddings)
    except Exception as e:
        print("Error while creating index:", e)
        exit()
    return vectordb

# Load the PDFs
# PDF 파일들을 로드하여 Document 객체 리스트로 변환
def load_pdfs() -> list[Document]:
    docs = []
    total_docs = 0
    total_pages = 0
    filenames = [filename for filename in os.listdir(DOG_BOOKS)
                 if filename.endswith('.pdf')]
    with tqdm(total=len(filenames), desc="Processing PDFs") as pbar_outer:
        for filename in filenames:
            pdf_path = os.path.join(DOG_BOOKS, filename)
            with open(pdf_path, 'rb') as file:
                pdf = PdfReader(file, strict=False)
                j = 0
                total_docs += 1
                with tqdm(total=len(pdf.pages),
                            desc="Loading Pages") as pbar_inner:
                    for page in pdf.pages:
                        total_pages += 1
                        j += 1
                        # Document 객체 생성: 페이지 내용 + 메타데이터
                        docs.append(Document(
                            page_content=page.extract_text(),
                            metadata={'page':j, 'source':file.name}
                        ))
                        pbar_inner.update()
                pbar_outer.update()
    print(f"Processed {total_docs} PDFs with {total_pages} pages.")
    return docs

# Check if user wants to quit
def check_prompt(user_input):
    if user_input.casefold() == 'quit':
        exit()
    return user_input

# Main function
def main():
    # 벡터 인덱스 생성 (모든 PDF 임베딩)
    vectordb = create_index()
    
    if vectordb is None:
        print("No index to query.")
        exit()

    # OpenAI LLM 초기화
    llm = OpenAI(openai_api_key=OPENAI_KEY)

    # QA Chain 생성: 'stuff' 방식은 모든 관련 문서를 프롬프트에 포함
    # 다른 방식: 'map_reduce', 'refine', 'map_rerank'
    chain = load_qa_chain(llm, chain_type='stuff')

    while True:
        prompt = check_prompt(input(
            'Ask a question against the PDF (type "quit" to exit):'))
        if not prompt:
            print("Please enter a valid question.")
            continue

        # similarity_search: 질문과 유사한 문서 검색
        # k=3: 상위 3개 문서만 반환
        # fetch_k=10: 먼저 10개를 가져온 후 재순위화
        docs = vectordb.similarity_search(prompt, k=3, fetch_k=10)

        # QA Chain 실행: 검색된 문서를 컨텍스트로 답변 생성
        response = chain.invoke({'input_documents': docs,
                                 'question': prompt},
                                return_only_outputs=True)
        print(f"Answer:\n {response['output_text']}")
        print("-"*80)

if __name__ == "__main__":
    main()