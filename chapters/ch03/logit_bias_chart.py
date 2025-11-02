# 모듈 설명: Logit Bias 효과 시각화
# - logit_bias 파라미터가 토큰 생성 확률에 미치는 영향을 막대 그래프로 표현합니다.
# - 특정 단어의 생성 확률을 높이거나 낮출 때 사용하는 기법
#
# 주요 개념:
# - Logit Bias: 특정 토큰의 생성 확률을 조정하는 파라미터 (-100 ~ 100)
# - -100: 해당 토큰 완전 억제 (절대 생성 안 됨)
# - 100: 해당 토큰 생성 확률 극대화
# - 사용 예: 비속어 차단, 특정 단어 강제, 형식 제어

import matplotlib.pyplot as plt

# 원래 확률 (logit bias 적용 전)
# 모델이 자연스럽게 예측한 각 토큰의 확률
tokens = ['apple', 'banana', 'cherry']
probabilities = [0.3, 0.5, 0.2]  # banana가 가장 높은 확률

# logit bias를 적용한 후의 확률 (예시 값)
# apple에 양수 bias, banana에 음수 bias 적용한 결과
adjusted_probabilities = [0.5, 0.2, 0.3]  # apple이 가장 높아짐

# 막대 차트 설정
barWidth = 0.3
r1 = range(len(probabilities))
r2 = [x + barWidth for x in r1]

plt.bar(r1, probabilities, width=barWidth, color=(10/255, 137/255, 2/255), align='center', label='Original Probabilities')
plt.bar(r2, adjusted_probabilities, width=barWidth, color=(128/255, 194/255, 29/255), align='center', label='Adjusted with Logit Bias')

# 라벨 및 타이틀
plt.xlabel('Tokens', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(probabilities))], tokens)
plt.ylabel('Probability')
plt.title('Effect of Logit Bias on Token Probabilities')
plt.legend()

# 차트 출력
plt.tight_layout()
plt.show()
