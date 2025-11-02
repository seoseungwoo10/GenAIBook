# 모듈 설명: Listing 8.9 - RAG(Retrieval-Augmented Generation) 블로그 GPT 예제
# - Redis 벡터 검색으로 관련 문서를 찾고, 그 내용을 바탕으로 GPT가 답변 생성
# - 토큰 예산을 관리하여 context window 내에서 최대한 많은 문서 포함
# - 검색 결과를 GPT에 컨텍스트로 제공하는 완전한 RAG 파이프라인

import numpy as np
from redis.commands.search.query import Query
import redis
import os
from openai import OpenAI
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import tiktoken as tk

# OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_BOOK_KEY'))

# Redis connection details
redis_host = "localhost"
redis_port = "6379"
redis_password = ""

# Count the number of tokens in a string
def count_tokens(string: str, encoding_name="cl100k_base") -> int:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    encoded_string = encoding.encode(string, disallowed_special=())

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

# Vectorize the query using OpenAI's text-embedding-ada-002 model
def get_embedding(text):
    # vectorize with OpenAI text-emebdding-ada-002
    embedding = client.embeddings.create(input=text,
    model="text-embedding-ada-002")

    vector = embedding.data[0].embedding
    
    return vector

# Perform a hybrid search using Redis search and return the top-k results
def hybrid_search(query_vector, client, top_k=5, hybrid_fields="*"):
    base_query = f"{hybrid_fields}=>[KNN {top_k} @embedding $vector AS vector_score]"
    query = Query(base_query).return_fields("url", 
                                            "title",
                                             "publish_date",
                                             "description",
                                             "content",
                                             "vector_score").sort_by("vector_score").dialect(2)

    try:
        results = client.ft("posts").search(query, query_params={"vector": query_vector})
    except Exception as e:
        print("Error calling Redis search: ", e)
        return None
    
    if results.total == 0:
        print("No results found for the given query vector.")
        return None
    elif results.total < top_k:
        print(f"Only {results.total} results found for the given query vector.")

    return results

# Return a message for GPT, with relevant source texts pulled from a the vector db.
# 벡터 DB에서 관련 문서를 검색하고 GPT 프롬프트 구성
def get_search_results(query: str, max_token = 4096, debug_message=False) -> str:
    # Connect to the Redis server
    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, encoding='utf-8', decode_responses=True)

    if conn.ping():
        if debug_message:
            print("Connected to Redis")

    # Vectorize the query using OpenAI's text-embedding-ada-002 model
    query_vector = get_embedding(query)

    # Convert the vector to a numpy array
    query_vector = np.array(query_vector).astype(np.float32).tobytes()

    # Perform the similarity search
    print("Searching for similar posts...")
    results = hybrid_search(query_vector, conn, top_k=5)
    
    # We reduce the token budget by 2000 to account for the query and the prompt.
    # 토큰 예산 설정: 전체에서 쿼리 및 프롬프트 오버헤드 제외
    token_budget = max_token - count_tokens(query) - 2000
    if debug_message:
        print(f"Token budget: {token_budget}")

    message = 'Use the blog post below to answer the subsequent question. \
            If the answer cannot be found in the articles, write \
            "Sorry, I could not find an answer in the blog posts."'
    
    question = f"\n\nQuestion: {query}"

    # 검색된 문서를 토큰 예산 내에서 최대한 포함
    if results:
        for i, post in enumerate(results.docs):
            next_post = f'\n\nBlog post:\n"""\n{post.content}\n"""'
            new_token_usage = count_tokens(message + question + next_post)
            if new_token_usage < token_budget:
                if debug_message:
                    print(f"Token usage: {new_token_usage}")
                message += next_post
            else:
                break  # 토큰 예산 초과 시 중단
    else:
        print("No results found")

    return message + question

# Ask GPT a question based on the search results
# RAG: 검색된 문서를 컨텍스트로 GPT에 질문
def ask_gpt(query : str, max_token = 4096, debug_message = False) -> str:
    message = get_search_results(
        query,
        max_token,
        debug_message=debug_message)
    
    if debug_message:
        print(message)
    
    # Ask GPT
    messages = [ 
        {"role": "system", 
         "content": "You answer questions in summary from the blog posts."},
        {"role": "user",
            "content": message},]
    
    if debug_message:
        print("Length of messages: ", len(messages))
        if debug_message:
            print("Total tokens: ", count_tokens(messages))
            print(messages)

    # GPT에 검색된 문서를 컨텍스트로 제공하여 답변 생성
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0.5,
        max_tokens=2000,
        top_p=0.95)
    
    response_message = response.choices[0].message.content
    
    return response_message

# Main function
if __name__ == "__main__":
    # Enter a query
    while True:
        query = input("Please enter your query: ")
        print(ask_gpt(query, max_token=15000, debug_message=False))
        print("=="*20)
