# 모듈 설명: Logit bias 효과를 보여주는 수평 막대 차트 예제
# - 수평 막대(hbar)를 사용해 원래 확률과 조정된 확률을 비교합니다.

import matplotlib.pyplot as plt

# 원래 확률
tokens = ['apple', 'banana', 'cherry']
probabilities = [0.3, 0.5, 0.2]

# logit bias 적용 후 확률
adjusted_probabilities = [0.5, 0.2, 0.3]

# 수평 막대 차트 설정
barHeight = 0.3
r1 = range(len(probabilities))
r2 = [x + barHeight for x in r1]

plt.barh(r1, probabilities, height=barHeight, color=(10/255, 137/255, 2/255), align='center', label='Original Probabilities')
plt.barh(r2, adjusted_probabilities, height=barHeight, color=(128/255, 194/255, 29/255), align='center', label='Adjusted with Logit Bias')

# 라벨
plt.ylabel('Tokens', fontweight='bold')
plt.yticks([r + barHeight for r in range(len(probabilities))], tokens)
plt.xlabel('Probability')
plt.title('Effect of Logit Bias on Token Probabilities')
plt.legend()

# 출력
plt.tight_layout()
plt.show()
