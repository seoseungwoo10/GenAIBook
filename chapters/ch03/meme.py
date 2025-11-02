# 모듈 설명: AI 밈 이미지 생성 예제
# - matplotlib을 사용하여 3패널 코믹 스트립 형태의 밈을 생성합니다.
# - AI의 능력과 한계를 유머러스하게 표현하는 이미지
#
# 주요 개념:
# - Matplotlib: Python의 시각화 라이브러리
# - Subplot: 여러 개의 그래프를 한 화면에 배치
# - PIL (Pillow): 이미지 처리 라이브러리 (여기서는 import만 함)

import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import rcParams


# Create the meme (3개의 패널을 병렬로 생성)
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
font_size = 12

# Panel 1: 검은 배경, 제목 텍스트
ax[0].set_facecolor('black')
ax[0].set_xticks([])
ax[0].set_yticks([])
# color 변수가 없으므로 기본값 문자열 사용
ax[0].set_title("Human: Solve this complex problem for me",
                color='white', fontsize=font_size)

# Panel 2
ax[1].set_facecolor('black')
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_title("AI: Done!", color='white', fontsize=font_size)

# Panel 3
ax[2].set_facecolor('black')
ax[2].set_xticks([])
ax[2].set_yticks([])
ax[2].set_title('Human: Now, can you understand sarcasm?', 
                color='white', fontsize=font_size)
ax[2].text(0.5, 0.5, "AI: Working on it...", color='white', fontsize=font_size,
           ha='center', va='center')

# 그림 레이아웃 정리 및 저장
plt.tight_layout()
# 저장 경로는 환경에 맞게 조정 필요 (현재는 /mnt/data 사용)
plt.savefig("/mnt/data/AI_meme_v2.png")
plt.show()
