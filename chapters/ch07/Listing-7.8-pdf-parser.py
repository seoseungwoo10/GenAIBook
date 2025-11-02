# 모듈 설명: Listing 7.8 - PDF 파서를 사용한 고급 추출 예제
# - pdfminer, tabula, PIL 등 여러 라이브러리를 사용하여
#   PDF에서 텍스트, 이미지, 표를 추출합니다.
# - 이미지는 PNG로 변환하여 저장하고, 표는 CSV로 저장합니다.

# pip install pdfminer-six
# pip install camelot-py[cv]
# pip install tabula-py # this also needs Java to be installed

# conda install -c conda-forge pdfminer.six
# conda install -c conda-forge camelot-py
# conda install -c conda-forge tabula-py
# conda install -c conda-forge pypdf2
# conda install -c conda-forge pillow

import os
# Import the required modules from pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTFigure, LTImage
from pdfminer.image import ImageWriter
from PIL import Image
import tabula
import warnings

warnings.filterwarnings("ignore")

PDF_FILE = "./data/test.pdf"
OUTPUT_FOLDER = "./data/temp/"

# Create an empty string to store the text
text = ''

# function that processes the elements of the PDF file
# PDF 요소(텍스트, 이미지, 도형)를 처리하는 함수
def process_element(element, iw):
    global text
    
    if isinstance(element, LTTextBox):
        # 텍스트 박스인 경우 텍스트 추출
        text += element.get_text()
    elif isinstance(element, LTImage):
        # 이미지인 경우 BMP로 추출 후 PNG로 변환
        # Export the image as a BMP file
        bmp_file = iw.export_image(element)
        
        # Prepend the output directory to the filename
        bmp_file = os.path.join(iw.outdir, bmp_file)
        
        # Open the BMP file with PIL
        img = Image.open(bmp_file)
        
        # Convert the image to PNG and save it
        png_file = bmp_file.rsplit('.', 1)[0] + '.png'
        img.save(png_file)
        
    if isinstance(element, LTFigure):
        # 도형인 경우 하위 요소를 재귀적으로 처리
        for child in element:
            process_element(child, iw)

# check if the output folder exists, if not create it
def check_output_folder():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

 # main function
def main():
    check_output_folder()
    
    print("Extracting text and images from the PDF file...")
    # Create an ImageWriter object to save the images
    iw = ImageWriter(OUTPUT_FOLDER)

    # Get the first page from the PDF file
    page = next(extract_pages(PDF_FILE))

    for element in page:
        process_element(element, iw)

    # Save the text in a file
    with open(OUTPUT_FOLDER + 'text.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    # Read the tables from all the pages of the PDF file using Tabula
    # Tabula를 사용하여 PDF의 모든 표 추출
    tables = tabula.read_pdf(PDF_FILE, pages='all', encoding='ISO-8859-1')

    # Save each table into a separate CSV file
    for i, table in enumerate(tables):
        table.to_csv(f'{OUTPUT_FOLDER}table_{i}.csv', index=False)

    print("Text and images extracted successfully!")
    print(f"The extracted images are saved in {OUTPUT_FOLDER}")
    print(f"The extracted text is saved in {OUTPUT_FOLDER} text.txt")
    print("Total number of tables extracted:", len(tables))

if __name__ == "__main__":
    main()