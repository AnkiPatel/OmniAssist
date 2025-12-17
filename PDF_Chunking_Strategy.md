# PDF Chunking Strategy Analysis for VectorDB

## Overview

This document analyzes 6 PDF files in `CodeBase/backend/data` and recommends optimal chunking strategies for building a high-quality vector database for RAG-based retrieval.

---

## Summary of PDF Files

| File | Pages | Total Chars | Avg Chars/Page | Type |
|------|-------|-------------|----------------|------|
| recoverpoint-vm-install-deploy-6-0-3.pdf | 85 | 189,250 | 2,226 | Installation Guide |
| rp4vm603 Events Reference Guide.pdf | 63 | 80,549 | 1,278 | Reference (Events) |
| rp4vm603 Security Configuration Guide.pdf | 29 | 71,977 | 2,481 | Security Config |
| rp4vm603 admin guide.pdf | 120 | 204,024 | 1,700 | Administration |
| rp4vm603 cli reference.pdf | 148 | 248,515 | 1,679 | CLI Commands |
| rp4vm603 product guide.pdf | 27 | 53,400 | 1,977 | Product Concepts |

**Total Content:** ~847,715 characters across 472 pages

---

## Detailed Analysis Per PDF

### 1. recoverpoint-vm-install-deploy-6-0-3.pdf
**Purpose:** Step-by-step installation and deployment instructions

| Metric | Value |
|--------|-------|
| Chapters | 8 |
| Tables | 23 |
| Figures | 4 |
| CLI/Code References | 245 |
| Numbered Lists (Steps) | 385 |
| Procedures | High |
| Has TOC/Bookmarks | ✅ Yes |

**Content Characteristics:**
- Heavily procedural with numbered steps
- Contains network configuration examples, IP address tables
- CLI commands for installation
- Prerequisites and system requirements
- Step-by-step deployment workflows

**Recommended Chunking Strategy:**
```
Strategy: Semantic + Header-Based Chunking
Chunk Size: 800-1000 tokens
Chunk Overlap: 150-200 tokens
Splitter: MarkdownHeaderTextSplitter or RecursiveCharacterTextSplitter with custom separators
Separators: ["\nChapter ", "\n## ", "\n### ", "\nStep ", "\n\d+\. ", "\n\n"]
```

**Rationale:**
- Preserve entire procedures together (steps 1-N should stay together)
- Keep table data with their headers
- CLI commands should include context of what they accomplish
- Chapter boundaries are natural semantic breaks

---

### 2. rp4vm603 Events Reference Guide.pdf
**Purpose:** Reference documentation for system events/alerts

| Metric | Value |
|--------|-------|
| Chapters | 2 |
| Tables | 44 |
| Figures | 7 |
| CLI/Code References | 0 |
| Numbered Lists | 21 |
| Has TOC/Bookmarks | ✅ Yes |

**Content Characteristics:**
- Heavy table content (event codes, descriptions, actions)
- Structured event definitions
- Alert categories and severity levels
- Troubleshooting guidance per event

**Recommended Chunking Strategy:**
```
Strategy: Table-Aware Chunking with Parent-Child
Chunk Size: 600-800 tokens (smaller due to discrete entries)
Chunk Overlap: 100 tokens
Special Handling: Parse tables as individual documents with metadata
```

**Rationale:**
- Each event entry is self-contained
- Tables should NOT be split mid-row
- Include table headers with each chunk
- Consider creating one chunk per event code with rich metadata

**Implementation Tip:**
```python
# Consider using special table extraction
from langchain.document_loaders import PDFPlumberLoader  # Better for tables
# Or use custom post-processing to identify and preserve table boundaries
```

---

### 3. rp4vm603 Security Configuration Guide.pdf
**Purpose:** Security configuration, ports, and hardening

| Metric | Value |
|--------|-------|
| Chapters | 0 (uses sections) |
| Tables | 20 |
| Figures | 0 |
| CLI/Code References | 57 |
| Numbered Lists | 70 |
| Has TOC/Bookmarks | ✅ Yes |

**Content Characteristics:**
- Port tables (port numbers, protocols, purposes)
- Security settings and configurations
- Authentication/authorization details
- SSL/TLS certificate information
- Compliance requirements

**Recommended Chunking Strategy:**
```
Strategy: Section-Based with Metadata Enrichment
Chunk Size: 800-1000 tokens
Chunk Overlap: 150 tokens
Metadata: Add security_topic, port_range, protocol tags
```

**Rationale:**
- Port tables need to stay together (port + protocol + purpose)
- Security topics are interconnected - slight overlap helps
- CLI commands for security settings need full context

---

### 4. rp4vm603 admin guide.pdf
**Purpose:** Day-to-day administration and operations

| Metric | Value |
|--------|-------|
| Chapters | 6 |
| Tables | 11 |
| Figures | 13 |
| CLI/Code References | 290 |
| Numbered Lists (Steps) | 303 |
| Procedures/How-tos | 49 |
| Errors/Warnings | 134 |
| Has TOC/Bookmarks | ✅ Yes (89+ outline items) |

**Content Characteristics:**
- Heavy procedural content
- UI navigation instructions
- Protection policies configuration
- VM replication workflows
- Troubleshooting sections
- NOTE/CAUTION/WARNING callouts

**Recommended Chunking Strategy:**
```
Strategy: Hierarchical Chunking with Context Preservation
Chunk Size: 1000-1200 tokens
Chunk Overlap: 200 tokens
Context Window: Prepend section header to each chunk
Separators: ["\nChapter", "\n## ", "\nProtect", "\nConfigure", "\nManag", "\n\d+\. "]
```

**Rationale:**
- Largest document - needs good chunk size
- Procedures must stay intact
- NOTE/CAUTION/WARNING should stay with relevant content
- Each procedure should include its parent section title

**Implementation Tip:**
```python
# Add parent context to each chunk
def add_context(chunks, doc_title):
    for chunk in chunks:
        chunk.metadata['parent_section'] = extract_section_header(chunk)
        chunk.metadata['doc_type'] = 'admin_guide'
```

---

### 5. rp4vm603 cli reference.pdf
**Purpose:** Complete CLI command reference

| Metric | Value |
|--------|-------|
| Chapters | 13 |
| Tables | 18 |
| Figures | 0 |
| CLI/Code References | 159 |
| Numbered Lists | 10 |
| Has TOC/Bookmarks | ✅ Yes (156+ outline items) |

**Content Characteristics:**
- One command per section pattern
- Command syntax + parameters + examples
- Keyboard shortcuts tables
- Very structured, repetitive format

**Recommended Chunking Strategy:**
```
Strategy: Command-Based Semantic Chunking (ONE CHUNK PER COMMAND)
Chunk Size: 500-800 tokens (commands are typically smaller)
Chunk Overlap: 50 tokens (minimal - commands are discrete)
Pattern Detection: Split on command name patterns
```

**Rationale:**
- Each CLI command should be ONE complete chunk
- Include: command name, syntax, all parameters, example(s)
- Low overlap needed as commands are independent
- High retrieval precision needed for CLI queries

**Implementation Tip:**
```python
# Custom splitter for CLI reference
command_pattern = r'\n(get_|set_|add_|remove_|create_|delete_|show_|list_)\w+'
# Split at each command boundary, keep command + full description
```

---

### 6. rp4vm603 product guide.pdf
**Purpose:** High-level concepts and architecture

| Metric | Value |
|--------|-------|
| Chapters | 3 |
| Tables | 2 |
| Figures | 8 |
| CLI/Code References | 30 |
| Numbered Lists | 0 |
| Procedures/How-tos | 4 |
| Has TOC/Bookmarks | ✅ Yes (15+ outline items) |

**Content Characteristics:**
- Conceptual explanations
- Architecture diagrams (referenced)
- Key terminology definitions
- System overview content
- Less procedural, more explanatory

**Recommended Chunking Strategy:**
```
Strategy: Semantic/Paragraph-Based Chunking
Chunk Size: 800-1000 tokens
Chunk Overlap: 200-250 tokens (higher overlap for conceptual content)
Separators: ["\n\n", "\n## ", "Figure \d+", "\n"]
```

**Rationale:**
- Concepts often span multiple paragraphs
- Higher overlap helps maintain context
- Definitions should include examples
- Good for "what is X?" type queries

---

## Global Recommendations

### 1. Current Implementation Issues

Your current `ingestion.py` uses:
```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
```

> [!WARNING]
> **Problems with current approach:**
> - One-size-fits-all doesn't work for these diverse document types
> - Tables are being split mid-row losing critical information
> - CLI commands may be cut off from their parameters
> - Procedures might be split across chunks

### 2. Recommended Multi-Strategy Approach

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

def get_splitter_for_document(filename):
    """Return appropriate splitter based on document type."""
    
    if 'cli reference' in filename.lower():
        # CLI Reference - smaller chunks, minimal overlap
        return RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=50,
            separators=["\n\n\n", "\n\n", "\nget_", "\nset_", "\nadd_", "\n"]
        )
    
    elif 'events reference' in filename.lower():
        # Events Guide - table-focused, small chunks
        return RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n\n", "\nTable ", "\n\n", "\n"]
        )
    
    elif 'security' in filename.lower():
        # Security Guide - medium chunks with context
        return RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n\n", "\nTable ", "\n## ", "\n\n"]
        )
    
    elif 'install' in filename.lower() or 'deploy' in filename.lower():
        # Installation Guide - preserve procedures
        return RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\nChapter ", "\n## ", "\nStep ", "\n\n", "\n"]
        )
    
    elif 'admin' in filename.lower():
        # Admin Guide - larger chunks for procedures
        return RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            separators=["\nChapter ", "\n## ", "\nNOTE:", "\n\n"]
        )
    
    elif 'product guide' in filename.lower():
        # Product Guide - conceptual, higher overlap
        return RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=250,
            separators=["\n\n\n", "\n## ", "\n\n"]
        )
    
    else:
        # Default fallback
        return RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
```

### 3. Metadata Enrichment

Add rich metadata to improve retrieval:

```python
def enrich_metadata(doc, filename):
    """Add metadata to improve retrieval."""
    doc.metadata['source_file'] = filename
    doc.metadata['doc_type'] = classify_doc_type(filename)
    
    # Add content hints
    if 'port' in doc.page_content.lower():
        doc.metadata['topic'] = 'networking'
    if any(cmd in doc.page_content for cmd in ['get_', 'set_', 'add_']):
        doc.metadata['topic'] = 'cli_command'
    if 'step' in doc.page_content.lower() or re.search(r'^\d+\.', doc.page_content):
        doc.metadata['topic'] = 'procedure'
    
    return doc
```

### 4. Consider Using Better PDF Extractors

For table-heavy documents, consider:

```python
# Option 1: PDFPlumber (better table extraction)
from langchain_community.document_loaders import PDFPlumberLoader

# Option 2: Unstructured (best for complex layouts)
from langchain_community.document_loaders import UnstructuredPDFLoader
```

---

## Expected Chunk Counts

| Document | Current (1000/200) | Recommended | Change |
|----------|-------------------|-------------|--------|
| Install Guide | ~190 chunks | ~220 chunks | +16% |
| Events Guide | ~80 chunks | ~130 chunks | +62% |
| Security Guide | ~72 chunks | ~95 chunks | +32% |
| Admin Guide | ~204 chunks | ~185 chunks | -9% |
| CLI Reference | ~249 chunks | ~350 chunks | +40% |
| Product Guide | ~53 chunks | ~60 chunks | +13% |

---

## Summary

| PDF Type | Chunk Size | Overlap | Key Separators | Priority |
|----------|------------|---------|----------------|----------|
| CLI Reference | 500-600 | 50 | Command patterns | Command integrity |
| Events Reference | 500-600 | 100 | Table rows | Event completeness |
| Security Guide | 800 | 150 | Sections, Tables | Context preservation |
| Install Guide | 1000 | 200 | Chapters, Steps | Procedure integrity |
| Admin Guide | 1200 | 200 | Chapters, Notes | Workflow completeness |
| Product Guide | 900 | 250 | Paragraphs | Concept understanding |
