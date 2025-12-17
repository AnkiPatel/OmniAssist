import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pypdf import PdfReader
import os
import re

data_path = r'c:\Users\ankit\CodingWorkspace\PraviSolutions\AntigravityWorkspace\OmniAssist\CodeBase\backend\data'

all_pdfs = [f for f in sorted(os.listdir(data_path)) if f.endswith('.pdf')]

for pdf_file in all_pdfs:
    file_path = os.path.join(data_path, pdf_file)
    if not os.path.exists(file_path):
        continue
    print("\n\n" + "="*80)
    print(f"FILE: {pdf_file}")
    print("="*80)
    print(f"File size: {os.path.getsize(file_path):,} bytes")
    
    reader = PdfReader(file_path)
    print(f"Total pages: {len(reader.pages)}")
    
    if reader.outline:
        print("Has Table of Contents/Bookmarks: Yes")
        # Try to extract outline structure
        def extract_outline(outline, level=0):
            result = []
            for item in outline:
                if isinstance(item, list):
                    result.extend(extract_outline(item, level+1))
                else:
                    result.append(("  "*level + str(item.title))[:60])
            return result
        outline_items = extract_outline(reader.outline)
        print(f"Outline structure (first 15 items):")
        for item in outline_items[:15]:
            print(f"  {item}")
        if len(outline_items) > 15:
            print(f"  ... and {len(outline_items)-15} more items")
    else:
        print("Has Table of Contents/Bookmarks: No")
    
    total_chars = 0
    all_text = ""
    for page in reader.pages:
        text = page.extract_text() or ""
        total_chars += len(text)
        all_text += text + "\n"
    
    print(f"Total characters: {total_chars:,}")
    print(f"Avg chars per page: {total_chars // len(reader.pages) if reader.pages else 0:,}")
    
    # Content structure analysis
    chapters = len(re.findall(r"CHAPTER\s+\d+", all_text, re.IGNORECASE))
    tables = len(re.findall(r"Table\s+\d+", all_text))
    figures = len(re.findall(r"Figure\s+\d+", all_text))
    code_blocks = len(re.findall(r"rpm|yum|vmware|esxi|ssh|vcenter|rpcli|rpa_|powerpath|datastore|get-|set-", all_text, re.IGNORECASE))
    numbered_lists = len(re.findall(r"^\d+\.\s", all_text, re.MULTILINE))
    headers = len(re.findall(r"^[A-Z][a-zA-Z\s]+\n", all_text, re.MULTILINE))
    procedures = len(re.findall(r"procedure|steps to|how to|to configure", all_text, re.IGNORECASE))
    errors = len(re.findall(r"error|warning|caution|note:", all_text, re.IGNORECASE))
    
    print(f"\nContent Structure Analysis:")
    print(f"  Chapters detected: {chapters}")
    print(f"  Headers/Sections: {headers}")
    print(f"  Tables: {tables}")
    print(f"  Figures: {figures}")
    print(f"  CLI/Code references: {code_blocks}")
    print(f"  Numbered lists: {numbered_lists}")
    print(f"  Procedures/How-tos: {procedures}")
    print(f"  Errors/Warnings/Notes: {errors}")
    
    # Sample content from different pages
    print(f"\n--- Sample from middle of document (page 15 or last page) ---")
    sample_page = min(14, len(reader.pages)-1)
    text = reader.pages[sample_page].extract_text() or ""
    text = text.encode("utf-8", errors="replace").decode("utf-8")
    print(f"[Page {sample_page+1}]:")
    sample = text[:1500] if len(text) > 1500 else text
    print(sample)
    if len(text) > 1500:
        print("...")
