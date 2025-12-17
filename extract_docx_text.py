import zipfile
import xml.etree.ElementTree as ET
import os
import sys

# Set encoding globally at start
sys.stdout.reconfigure(encoding='utf-8')

def extract_text(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            # Namespaces likely used in docx
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            text_parts = []
            # Iterate over paragraphs
            for p in tree.iter(f"{{{ns['w']}}}p"):
                # Iterate over runs and text in paragraph
                paragraph_text = []
                for node in p.iter():
                    if node.tag == f"{{{ns['w']}}}t":
                        if node.text:
                            paragraph_text.append(node.text)
                    elif node.tag == f"{{{ns['w']}}}br":
                         paragraph_text.append('\n')
                    elif node.tag == f"{{{ns['w']}}}tab":
                         paragraph_text.append('\t')
                
                text_parts.append("".join(paragraph_text))
                text_parts.append("\n") # Newline after paragraph
            
            return "".join(text_parts)
    except Exception as e:
        return f"Error reading {docx_path}: {e}"

files = [
    r"ProjectDocuments\PRD_Document.docx",
    r"ProjectDocuments\RequirmentRefinement.docx"
]

print(f"Current working directory: {os.getcwd()}")
for f in files:
    print(f"--- CONTENT OF {f} ---")
    full_path = os.path.abspath(f)
    if os.path.exists(full_path):
        content = extract_text(full_path)
        print(content)
    else:
        print(f"File not found: {full_path}")
    print("\n----------------------\n")
