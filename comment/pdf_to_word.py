import PyPDF2
from docx import Document

path="F:\\陈文林.pdf"
# 打开PDF文件
pdf_file = open(path, 'rb')


doc=Document()
# 创建一个PDF读取器对象
pdf_reader = PyPDF2.PdfReader(pdf_file)

# 创建一个Word文档对象

text_all=[]
# 读取PDF文件中的每一页，并将其转换为Word文档中的段落
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text = page.extract_text()
    text_all.append(text)

doc.add_paragraph(" ".join(text_all))
# 保存Word文档
doc.save('F:\\陈文林.docx')

# 关闭PDF文件和Word文档对象
pdf_file.close()

