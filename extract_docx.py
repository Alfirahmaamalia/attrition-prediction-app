import zipfile
import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_docx(path):
    with zipfile.ZipFile(path) as docx:
        tree = ET.XML(docx.read('word/document.xml'))
        texts = []
        for paragraph in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            para_text = ""
            for node in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if node.text:
                    para_text += node.text
            if para_text:
                 texts.append(para_text)
        return '\n'.join(texts)

with open('docx_content.txt', 'w', encoding='utf-8') as f:
    f.write(read_docx('KAPSEL DSP ILKOM 2025.docx'))
