# 모듈 설명: 코드 생성 및 이미지 생성 유틸 예제
# - Stability AI(Txt->Image) 호출 예제와 간단한 OAuth2 샘플 및 타이밍 데코레이터를 포함합니다.
# - 이 파일은 교육 목적의 예시 모음이며, 실제 API 키와 환경 설정이 필요합니다.

import base64
import os
import requests
import datetime
import re


# write a function to calculate the time complexity of a function
# (간단한 실행 시간 측정 데코레이터)
def time_complexity(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        func(*args, **kwargs)
        end = datetime.datetime.now()
        print(f"Function {func.__name__} took {end - start} seconds")

    return wrapper


engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"
api_key = os.getenv("STABILITY_API_KEY")

# write a python function that takes a prompt and uses stability AI 
# to generate a image and save it to a file
def generate_image(prompt):
    # 안정성 API 키 확인
    if api_key is None:
        raise Exception("Missing Stability API key.")

    # Set the directory where we'll store the image
    image_dir = os.path.join(os.curdir, 'images')

    # Make sure the directory exists
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Function to clean up filenames
    def valid_filename(s):
        s = re.sub(r'[^\w_.)( -]', '', s).strip()
        return re.sub(r'[\s]+', '_', s)

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{ "text": f"{prompt}", "weight": 1.0}],
            "cfg_scale": 7, "height": 1024, "width": 1024,
            "samples": 1, "steps": 50,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        filename = f"sd_{valid_filename(prompt)}_{i}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = os.path.join(image_dir, filename)
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))


# write a function to implement oauth2 authentication for a web application running on azure
# - 예시로 Azure Identity와 KeyVault를 사용해 시크릿을 읽는 흐름을 보여줍니다.
def oauth2_authenticate():
    # get the environment variables
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    tenant_id = os.environ["TENANT_ID"]
    redirect_uri = os.environ["REDIRECT_URI"]

    # construct the oauth2 url
    oauth2_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    # construct the oauth2 payload
    oauth2_payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "scope": "https://management.azure.com/.default"
    }

    # make the oauth2 request
    oauth2_response = requests.post(oauth2_url, data=oauth2_payload)

    # return the oauth2 response
    return oauth2_response.json()
