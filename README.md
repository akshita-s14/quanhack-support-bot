# AI-Powered Customer Support Bot 🤖💬

An intelligent, L1 customer support agent that leverages a custom-built RAG (Retrieval-Augmented Generation) C++ engine to handle client queries. The system processes client documents, answers user questions directly via **WhatsApp**, and seamlessly escalates complex or low-confidence queries to a stunning **Human Agent Dashboard**.

## 🌟 Key Features

- **WhatsApp Integration:** Primary user interface powered by Twilio Sandbox, allowing users to interact directly from WhatsApp.
- **Custom C++ RAG Engine:** Fast, efficient retrieval-augmented generation to provide accurate answers based on your specific client documents.
- **Live Agent Dashboard:** A beautiful, glassmorphism web interface that flashes red when a ticket is escalated, allowing human agents to monitor and take over live chats.
- **Automated Human Escalation:** Automatically detects low-confidence responses or uncertain language and escalates to the dashboard.
- **Dynamic Knowledge Base:** Easily drop new `.txt` files into the `knowledge_base` folder and ingest them instantly.

---

## 🏗️ Architecture & Workflow

**Input ➡️ Process ➡️ Output**

1. **Input (WhatsApp):** The customer sends a message via WhatsApp.
2. **Gateway (Twilio & Ngrok):** Twilio receives the message and securely tunnels it to our local Flask server via Ngrok.
3. **Process (Middleware + AI Engine):**
   - The Flask app (`app.py`) receives the query.
   - It forwards the query to the custom C++ RAG Engine (`your-own-ai`).
   - The engine embeds the query, searches the HNSW vector index for relevant document context, and generates an AI response.
4. **Validation (Confidence Check):**
   - The Flask app evaluates the engine's response based on cosine distance.
   - If confidence is high, it replies to the customer.
   - If confidence is low or the AI expresses uncertainty, the system **escalates** the query, intercepting the reply and instantly pushing it to the **Live Agent Dashboard**.
5. **Output:** 
   - Customer receives a WhatsApp message.
   - Human Agent receives a real-time notification on the web UI.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- [Ngrok](https://ngrok.com/) installed
- A [Twilio](https://twilio.com/) Account
- Ollama (with `nomic-embed-text` and `llama3.2` pulled)
- C++ build tools

### 1. Set up the Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run the C++ AI Engine
Navigate to the `your-own-ai` folder and run the compiled engine:
```bash
.\engine.exe
```

### 3. Ingest Your Knowledge Base
Drop your custom `.txt` files into the `knowledge_base/` directory, then train the engine:
```bash
python ingest.py
```

### 4. Start the Application & Dashboard
```bash
python app.py
```
*You can now view the live dashboard at `http://localhost:5000/dashboard`*

### 5. Expose to the Internet & Connect Twilio
In a new terminal, run:
```bash
.\ngrok http 5000
```
Put the generated Ngrok URL (with `/whatsapp` appended) into your Twilio Sandbox Settings as an HTTP POST webhook.

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.
