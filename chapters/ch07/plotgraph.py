# 모듈 설명: 3D 벡터 공간 시각화 예제
# - matplotlib를 사용하여 3D 산점도를 그립니다.
# - 단어 임베딩 벡터를 시각화하는 예제로 활용 가능합니다.
# - 쿼리 단어와 유사도가 높은 단어들의 위치 관계를 표현

import matplotlib.pyplot as plt
import numpy as np

# Sample data points
# 임베딩 벡터를 시뮬레이션한 랜덤 데이터
x = np.random.rand(50) * 10
y = np.random.rand(50) * 10
z = np.random.rand(50) * 10

# Create a new figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plotting the data points
ax.scatter(x, y, z, c='g', marker='o', s=50)  # Using green color with 'o' marker

# Adding labels
# 특정 위치에 단어 레이블 추가
ax.text(2, 2, 2, 'Wolf')
ax.text(4, 4, 4, 'Dog')
ax.text(6, 6, 6, 'Cat')
ax.text(8, 8, 8, 'Banana')
ax.text(9, 9, 9, 'Apple')
ax.text(3, 4, 4, 'Query: Puppy', color='blue')  # Highlighting the 'Query: Puppy' label

# Setting the axis labels
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# Display the plot
plt.show()
