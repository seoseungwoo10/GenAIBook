# 모듈 설명: Listing 7.9 - Azure Document Intelligence(Form Recognizer) 사용 예제
# - Azure AI Form Recognizer(현재 Document Intelligence로 명칭 변경)를 사용하여
#   PDF 문서의 레이아웃, 텍스트, 표, 선택 마크 등을 인식합니다.
# - prebuilt-layout 모델을 사용하여 문서 구조를 자동으로 분석

# Form recognizer (now called Document Intelligence) isn't available on conda yet, so we'll use pip
# pip install azure-ai-formrecognizer 
# conda install -c conda-forge azure-core 

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

#endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
#key = "YOUR_FORM_RECOGNIZER_KEY"
endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
key = os.getenv("DOC_INTELLIGENCE_KEY")

# sample document
pdf_file = "./data/test.pdf"

# Document Intelligence 클라이언트 초기화
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Open the file in binary mode
# prebuilt-layout 모델을 사용하여 문서 분석 시작
with open(pdf_file, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", f.read())
result = poller.result()

# 대안: URL에서 직접 문서 분석
# poller = document_analysis_client.begin_analyze_document_from_url(
#     "prebuilt-layout", pdf_file)
# result = poller.result()

# 스타일 정보 출력 (손글씨 여부 등)
for style in enumerate(result.styles):
    print(
        "Document contains {} content".format(
         "handwritten" if style.is_handwritten else "no handwritten"
        )
    )

# 각 페이지의 라인 단위 텍스트 출력
for page in result.pages:
    for line_idx, line in enumerate(page.lines):
        print(
         "...Line # {} has text content '{}'".format(
        line_idx,
        line.content.encode("utf-8")
        )
    )

    # 선택 마크(체크박스 등) 정보 출력
    for selection_mark in page.selection_marks:
        print(
         "...Selection mark is '{}' and has a confidence of {}".format(
         selection_mark.state,
         selection_mark.confidence
         )
    )

# 표 정보 출력
for table_idx, table in enumerate(result.tables):
    print(
        "Table # {} has {} rows and {} columns".format(
        table_idx, table.row_count, table.column_count
        )
    )
        
    # 각 셀의 내용 출력
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
            cell.row_index,
            cell.column_index,
            cell.content.encode("utf-8"),
            )
        )

print("----------------------------------------")
