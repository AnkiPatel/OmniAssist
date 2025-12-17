try:
    from langchain.chains import create_retrieval_chain
    print("Import success: langchain.chains.create_retrieval_chain")
except ImportError as e:
    print(f"Import failed: {e}")

try:
    from langchain.chains import create_stuff_documents_chain
    print("Import success: langchain.chains.create_stuff_documents_chain")
except ImportError as e:
    print(f"Import failed: {e}")

try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
except:
    print("Could not get langchain version")
