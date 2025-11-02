# 모듈 설명: Listing 8.3 - Redis를 사용한 벡터 검색 인덱스 생성/관리 예제
# - Redis Stack의 FT(Full-Text Search) 모듈을 사용해 벡터 검색 인덱스를 생성, 조회, 삭제합니다.
# - HNSW 알고리즘 기반의 벡터 필드와 텍스트/태그 필드를 포함한 스키마 정의
# - 메뉴 기반 대화식 인터페이스 제공

import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import TagField

# Redis connection details
redis_host = "localhost"
redis_port = "6379"
redis_password = ""
 
# Connect to the Redis server
conn = redis.Redis(host=redis_host, 
                   port=redis_port,
                   password=redis_password, 
                   encoding='utf-8', 
                   decode_responses=True)

# Define the schema for the index
# 벡터 검색을 위한 스키마: 태그, 텍스트, 벡터 필드 정의
SCHEMA = [
    TagField("url"),
    TextField("title"), 
    TextField("description"),
    TextField("publish_date"),
    TextField("content"),
    VectorField("embedding", "HNSW", {
        "TYPE": "FLOAT32",
        "DIM": 1536,  # text-embedding-ada-002의 차원
        "DISTANCE_METRIC": "COSINE"}
        ),
]

# Create an index
# 인덱스 생성 (이미 존재하면 예외 처리)
def create_index(conn, schema, index_name="posts"):
    try:
        conn.ft(index_name).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=["post:"], index_type=IndexType.HASH))
    except Exception as e:
        print("Index already exists")

# Delete an index
# 인덱스 삭제
def delete_index(conn, index_name="posts"):
    try:
        conn.execute_command('FT.DROPINDEX', index_name)
    except Exception as e:
        print("Failed to delete index: ", e)

# Delete all keys from an index
# 인덱스의 모든 문서 키 삭제
def delete_all_keys_from_index(conn, index_name="posts"):
    try:
        # 1. Retrieve all document IDs from the index.
        result = conn.execute_command('FT.SEARCH', index_name, '*', 'NOCONTENT')

        # 2. Parse the result to get document IDs. Skip the first element which is the total count.
        doc_ids = result[1::2]  # Taking every second element starting from the first.

        # 3. Delete each document key.
        for doc_id in doc_ids:
            conn.delete(doc_id)
            
    except Exception as e:
        print("Failed to delete keys: ", e)

# View index details
# 인덱스 상세 정보 조회
def view_index(conn, index_name="posts"):
    try:
        info = conn.execute_command('FT.INFO', index_name)
        for i in range(0, len(info), 2):
            print(f"{info[i]}: {info[i+1]}")
    except Exception as e:
        print("Failed to retrieve index details: ", e)

# Main function
# 메뉴 기반 대화식 인터페이스
def main():
    while True:
        print("1. View index details 🤘")
        print("2. Create index 😁")
        print("3. Delete index 😭")
        print("4. Exit 🚪")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_index(conn)
        elif choice == '2':
            create_index(conn, SCHEMA)
        elif choice == '3':
            delete_all_keys_from_index(conn)
            delete_index(conn)
        elif choice == '4':
            break
        else:
            print("Invalid choice. 🙃 Please enter a valid option.")

if __name__ == "__main__":
    main()