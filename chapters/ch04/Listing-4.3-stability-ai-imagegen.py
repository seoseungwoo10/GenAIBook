# 모듈 설명: Stability AI text-to-image 예제
# - Stability API에 텍스트 프롬프트를 전송해 이미지를 생성하고 base64로 반환되는
#   결과를 디코드하여 로컬에 이미지 파일로 저장합니다.

import base64
import os
import requests
import datetime
import re

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"
api_key = os.getenv("STABILITY_API_KEY")

prompt = "A panda surfing on a wave"

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

# 요청 전송
response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/text-to-image",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "text_prompts": [
            {
                "text": f"{prompt}",
            }
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 50,
    },
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()

# 반환된 base64 이미지들을 디코딩하여 파일로 저장
for i, image in enumerate(data["artifacts"]):
    filename = f"sd_{valid_filename(prompt)}_{i}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image["base64"]))
