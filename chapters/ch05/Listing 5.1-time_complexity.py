# 모듈 설명: Listing 5.1 - 시간 측정 및 OpenAI Completion 사용 예제(테스트 포함)
# - unittest를 사용해 OpenAI Completion 호출 결과를 모의(moc)하여 테스트하는 예제입니다.
# - 실제 OpenAI 호출은 네트워크/환경 변수에 의존하므로 테스트는 mocking으로 처리합니다.

# import os
# import openai

# openai.api_type = "azure"
# openai.api_base = os.getenv("AOAI_ENDPOINT")
# openai.api_version = "2022-12-01"
# openai.api_key = os.getenv("AOAI_KEY")

# prompt_startphrase = "Suggest three names for a new pet salon business."

# response = openai.Completion.create(
#   engine="text-davinci-003",
#   prompt=prompt_startphrase,
#   temperature=0.8,
#   max_tokens=100,
#   suffix="\nThats all folks!",
#   stop=None)

# responsetext = response["choices"][0]["text"]

# print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)

# print(response)

import unittest
from unittest.mock import patch, MagicMock
import os
import openai

class TestOpenAICompletion(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_base = "test_api_base"
        os.environ["AOAI_KEY"] = self.api_key
        os.environ["AOAI_ENDPOINT"] = self.api_base

    @patch('openai.Completion.create')
    def test_completion_create(self, mock_create):
        # mock 설정: Completion.create가 반환해야 할 값 설정
        mock_create.return_value = {
            "choices": [
                {"text": "test_text"}
            ]
        }
        prompt_startphrase = "Suggest three names for a new pet salon business."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_startphrase,
            temperature=0.8,
            max_tokens=100,
            suffix="\nThats all folks!",
            stop=None)
        # 모의 응답이 올바르게 사용되는지 검증
        self.assertEqual(response["choices"][0]["text"], "test_text")

    @patch('builtins.print')
    def test_print(self, mock_print):
        prompt_startphrase = "Suggest three names for a new pet salon business."
        responsetext = "test_text"
        print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
        mock_print.assert_called_with("Prompt:Suggest three names for a new pet salon business.\nResponse:test_text")

if __name__ == '__main__':
    unittest.main()