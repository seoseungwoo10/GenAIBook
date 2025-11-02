# 모듈 설명: Stability AI 마스킹(inpainting) 예제
# - 원본 이미지와 마스크 이미지를 업로드하고, 마스크된 영역만 변형하여 이미지를 생성합니다.
# - 응답의 base64 이미지를 디코딩하여 저장합니다.

import base64
import os
import requests
import datetime
import re

engine_id = "stable-inpainting-512-v2-0"
api_host = "https://api.stability.ai"
api_key = os.getenv("STABILITY_API_KEY")

orginal_image = "images/serene_vacation_lake_house.jpg"
mask_image = "images/mask_serene_vacation_lake_house.jpg"
prompt = "A serene vacation lake house"

# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')

# Make sure the directory exists
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Function to clean up filenames
def valid_filename(s):
    s = re.sub(r'[^\w_.)( -]', '', s).strip()
    return re.sub(r'[\s]+', '_', s)

if api_key is None:
    raise Exception("Missing Stability API key.")

# 마스킹을 포함한 이미지-투-이미지 API 호출
response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/image-to-image/masking",
    headers={
        "Accept": 'application/json',
        "Authorization": f"Bearer {api_key}"
    },
    files={
        'init_image': open(orginal_image, 'rb'),
        'mask_image': open(mask_image, 'rb'),
    },
    data={
        "mask_source": "MASK_IMAGE_BLACK",
        "text_prompts[0][text]": prompt,
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "samples": 4,
        "steps": 50,
    }
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()

for i, image in enumerate(data["artifacts"]):
    filename = f"{valid_filename(os.path.basename(orginal_image))}_masking_{i}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image["base64"]))
