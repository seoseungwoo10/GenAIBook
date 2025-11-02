# 모듈 설명: Stability AI를 사용한 이미지 생성 함수 예제
# - 엔진 호출, 응답 검사, base64 디코딩 및 파일 저장을 수행합니다.

# Stability AI를 사용하여 프롬프트에 대한 이미지를 생성하고 파일에 저장하는 Python 함수 작성
def generate_image(prompt):
    if api_key is None:
        raise Exception("Missing Stability API key.")

    # 이미지를 저장할 디렉토리 설정
    image_dir = os.path.join(os.curdir, 'images')

    # 디렉토리가 존재하는지 확인
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # 파일 이름을 정리하는 함수
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