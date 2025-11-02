### translation : [English](README.md)

# 도서 - 실전 생성형 AI
여기는 제 저서 [**Generative AI in Action**](https://www.manning.com/books/generative-ai-in-action) (Manning 출판)에 수반되는 코드 저장소입니다.

참고: 도서는 [아마존](https://a.co/d/cFDrfcp)에서도 구입할 수 있습니다.

<img src="docs/images/bahree_genai_in_action.jpg" width="35%" height="35%"/>

[![ko-fi](https://img.shields.io/badge/ko--fi-Fuel%20my%20AI-29abe0?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/bahree)

이 저장소에는 다음과 같은 유용한 항목들이 포함되어 있습니다:

- 책 예제 코드
- 다양한 AI 기술과 기법에 관련된 연구 논문 목록
- 많은 개념을 통합해 로컬에서 실행할 수 있는 웹 애플리케이션
- 로컬에서 의존성을 설치하기 위한 상세 설치 안내

| :warning: **경고:** OpenAI API 변경 관련 |
| --- |
책의 코드는 OpenAI가 최근에 업데이트한 새로운 API (v1.0)와 함께 동작합니다. 오래된 패키지 버전(v0.28)을 사용 중이라면 코드를 동작시키기 위해 최신 버전으로 업그레이드해야 합니다. 패키지를 업그레이드하려면 다음 명령을 실행하세요: `pip install --upgrade openai`. conda를 사용 중이라면 `conda update openai`를 실행하세요.

## 주요 의존성 :minidisc:
설치 전에, 책에서 안내한 대로 아래 기본 의존성이 설치되어 있다고 가정합니다. 대부분의 개발자와 데이터 과학자는 이 항목들을 이미 갖추고 있을 것이며, 추가 단계는 필요하지 않을 수 있습니다.

참고: 아래 항목이 누락되어 있고 단계별 지침이 필요하면, 상세한 <a href="docs/detailed-instructions.md" target="_blank">의존성 설치 지침</a>를 참조하세요.

- **IDE:** <a href="https://code.visualstudio.com/" target="_blank">Visual Studio Code</a> (또는 유사 도구) 💻.
- **Python:** 버전 `3.7.1` 이상; 책에서 사용한 버전은 `3.11.3` 입니다.
  - 설치된 Python 버전을 확인하려면: `python --version`
- **패키지 관리자:** 기술적으로는 필수는 아니지만 환경 관리를 위해 권장합니다. 책에서는 `conda`를 사용하지만, 선호하는 것을 사용하시면 됩니다.
- **Git:** GitHub와 함께 사용하므로 로컬에 Git이 설치되어 있어야 합니다.

## 설치 안내 :books:
환경을 준비하는 단계는 <a href="docs/installation.md" target="_blank">설치 안내</a>에 자세히 설명되어 있습니다.

## 코드 위치 :file_folder:
책의 코드는 장별로 구성되어 있으며, `chapters` 폴더에 들어 있습니다. 각 장은 `ch{장번호}` 형식의 폴더로 정리되어 있습니다.

유틸리티 함수와 프로그램은 `utils` 폴더에서 찾을 수 있습니다.

## 웹 애플리케이션 :earth_americas:
장의 코드 외에, 다양한 개념을 한데 모아 로컬에서 실행할 수 있는 완전한 웹 애플리케이션이 제공됩니다. 해당 코드는 `webapp` 폴더에 있습니다. :panda_face:

**참고:** :information_source: 이 웹 애플리케이션은 로컬 참고용으로 제공되며 인터넷에 노출할 목적으로 필요한 모든 프록시 및 보안 제어를 포함하지 않습니다.

## 논문 목록 :page_facing_up:
LLM(대형 언어 모델)과 생성형 AI는 여전히 빠르게 발전 중이며, 관련 연구 문헌도 매우 활발합니다. 많은 관련 자료는 `papers` 폴더(장별로 정리)에서 찾아볼 수 있습니다.

독자가 이 모든 것을 알 필요는 없지만, 관련 개념을 더 깊게 이해하면 큰 도움이 됩니다.

## 연락처
제 <a href="https://github.com/bahree" target="_blank">GitHub 프로필</a>에서 연락 방법을 확인할 수 있습니다. 질문이나 이슈가 있으면 Issue를 제출하세요.

## 후원
[![ko-fi](https://img.shields.io/badge/ko--fi-Fuel%20my%20AI-29abe0?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/bahree)

## 라이선스
이 저장소의 작업물은 <a href="LICENSE" target="_blank">MIT License</a> 하에 공유됩니다.
요약하자면, 저작권 및 라이선스 고지를 보존하는 조건만 있는 짧고 관대한 허가 라이선스입니다. 수정하거나 확장된 작업은 다른 조건으로 배포할 수 있습니다.
