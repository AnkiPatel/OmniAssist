import sys
import os
sys.path.append(os.getcwd())

try:
    print("Attempting to import core.rag...")
    from backend.core import rag
    print("Successfully imported core.rag")
except Exception as e:
    print(f"Failed to import core.rag: {e}")
    import traceback
    traceback.print_exc()
