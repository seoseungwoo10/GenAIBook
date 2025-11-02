"""
Listing 2.5 - 문자열 역순 변환 알고리즘
제자리(in-place) 방식으로 문자열을 역순으로 뒤집는 함수입니다.
투 포인터(two pointer) 알고리즘을 사용합니다.
"""

# 모듈 설명: Listing 2.5 - 문자열 역순 변환 (in-place 방식 시뮬레이션)
# - 파이썬에서는 문자열이 불변(immutable)이므로 실제 in-place 변경은 불가능하며,
#   리스트로 변환한 다음 두 포인터(two-pointer) 방법으로 교환하여 역순을 만듭니다.

def inplace_reverse(str):
    """
    주어진 문자열을 역순으로 반환합니다 (리스트 변환 후 투 포인터로 교환).

    Args:
        str: 역순으로 만들 문자열

    Returns:
        역순 문자열

    시간 복잡도: O(n)
    공간 복잡도: O(n) - 파이썬 문자열 불변성으로 인해 리스트로 변환함
    """
    if str:
        # 문자열을 리스트로 변환하여 변경 가능하게 함
        lst = list(str)

        # 시작과 끝 인덱스 초기화
        start = 0
        end = len(lst) - 1

        # 투 포인터로 요소 교환
        while start < end:
            lst[start], lst[end] = lst[end], lst[start]
            start += 1
            end -= 1

        # 리스트를 다시 문자열로 합쳐서 반환
        return ''.join(lst)
    # 빈 문자열 또는 None인 경우 그대로 반환
    return str
