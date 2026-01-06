# Phase 1a: Execution Guide (Beginner Friendly)

This guide will help you set up and run the **OmniAssist Backend** on your local machine. You don't need to be an expert!

## 1. Prerequisites
Before you begin, ensure you have the following:
*   **Visual Studio Code (VS Code)** installed.
*   **Terminal** access (built into VS Code).
*   **Groq API Key** (You need this for the AI to work).

## 2. Setup (One-Time Only)

### Step 2.1: Open the Project
1.  Open **Visual Studio Code**.
2.  Go to **File > Open Folder**.
3.  Select the **`OmniAssist`** folder.

### Step 2.2: Create the Environment File
The application needs your API key to function.
1.  Navigate to the **`CodeBase`** folder in the VS Code file explorer.
2.  Right-click on `CodeBase` and select **New File**.
3.  Name the file: **`.env`**
4.  Open the file and paste your key strictly in this format:
    ```text
    GROQ_API_KEY=gsk_your_actual_api_key_here
    ```
5.  Save the file (**Ctrl+S** or **Cmd+S**).

## 3. Starting the Server

### Step 3.1: Open the Integrated Terminal
1.  In VS Code, press **Ctrl+`** (backtick) or go to **Terminal > New Terminal**.
2.  Ensure you are in the `OmniAssist/CodeBase` directory. If not, type:
    ```bash
    cd CodeBase
    ```

### Step 3.2: Run the Server
Copy and paste this command into the terminal and press **Enter**:
```bash
.venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8001
```

**Success Message:**
You should see output like:
> `INFO: Uvicorn running on http://0.0.0.0:8001`

**Note:** Keep this terminal **open** while you use the app. Closing it stops the server.

## 4. Using the Application (Verification)

Since the User Interface (UI) is coming in Phase 1b, we verify functionality using **curl** commands or a browser tool.

### Option A: Quick Test (Command Line)
Open a **new** terminal window (keep the server running in the first one) and run:

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the installation prerequisites?", "role": "learner"}'
```
You should get a detailed text response about installation.

### Option B: Swagger UI (Visual)
1.  Open your web browser (Chrome, Safari, etc.).
2.  Go to: **[http://localhost:8001/docs](http://localhost:8001/docs)**
3.  You will see an interactive menu.
    *   Click on **POST /chat**.
    *   Click **Try it out**.
    *   Edit the "query" text.
    *   Click **Execute**.
    *   Scroll down to see the "Response body".

## 5. Troubleshooting / FAQ

**Q: I see "Collection ... does not exist" error.**
*   **Fix:** The database needs to be re-created. Run this command in the terminal:
    ```bash
    .venv/bin/python backend/ingestion.py
    ```

**Q: I see "ModuleNotFoundError".**
*   **Fix:** Dependencies might be missing. Run:
    ```bash
    .venv/bin/pip install -r backend/requirements.txt
    ```

**Q: How do I stop the server?**
*   Click in the terminal where it's running and press **Ctrl+C**.
