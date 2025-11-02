# 모듈 설명: Listing 11.6 - Azure Managed Identity를 사용한 인증
# - API 키 대신 Azure AD 토큰 기반 인증을 사용합니다.
# - Managed Identity를 통해 보안 강화 및 키 관리 부담 감소
# - 프로덕션 환경에서 권장되는 보안 모범 사례
#
# 주요 개념:
# - Managed Identity: Azure 리소스에 자동으로 관리되는 ID 제공
# - Azure AD Token: API 키 대신 토큰으로 인증 (더 안전함)
# - DefaultAzureCredential: 여러 인증 방법을 자동으로 시도 (Managed Identity, CLI, 환경변수 등)
# - Bearer Token: OAuth 2.0 표준 인증 토큰

import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Set your OpenAI API key
AOAI_API_KEY = os.getenv("AOAI_KEY")  # 참고용 (실제로는 사용 안 함)
AZURE_ENDPOINT = os.getenv("AOAI_ENDPOINT")
API_VERSION = "2024-02-15-preview"

# Bearer 토큰 프로바이더 생성
# DefaultAzureCredential: 다양한 인증 소스를 자동으로 시도
#   1. 환경 변수
#   2. Managed Identity (VM, App Service 등)
#   3. Azure CLI
#   4. Visual Studio Code
#   5. Azure PowerShell
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"  # Cognitive Services 스코프
)

# Azure OpenAI 클라이언트 생성
# azure_ad_token_provider 사용: API 키 대신 토큰 기반 인증
# 장점:
#   - 키 로테이션 자동화
#   - 키 유출 위험 감소
#   - Azure RBAC와 통합
#   - 감사 로그 개선
client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    azure_ad_token_provider=token_provider,  # 토큰 기반 인증
)

# 이후 일반적인 방식으로 API 사용 가능
# response = client.chat.completions.create(...)
