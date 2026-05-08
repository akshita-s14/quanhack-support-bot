import os
import requests

ENGINE_URL = "http://localhost:9090"
KB_DIR = "knowledge_base"

def ingest_documents():
    if not os.path.exists(KB_DIR):
        print(f"Error: Directory '{KB_DIR}' not found.")
        return

    print("Checking engine status...")
    try:
        res = requests.get(f"{ENGINE_URL}/status")
        if res.status_code != 200:
            print("Engine is not ready.")
            return
    except Exception as e:
        print("Failed to connect to engine. Make sure engine.exe is running!")
        return

    print(f"Reading files from '{KB_DIR}'...")
    for filename in os.listdir(KB_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(KB_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            title = filename.replace(".txt", "").replace("_", " ").title()
            print(f"Ingesting: {title}...")
            
            payload = {
                "title": title,
                "text": content
            }
            try:
                r = requests.post(f"{ENGINE_URL}/doc/insert", json=payload)
                if r.status_code == 200:
                    print(f"  -> Successfully inserted {title}")
                else:
                    print(f"  -> Failed: {r.text}")
            except Exception as e:
                print(f"  -> Error communicating with engine: {e}")

if __name__ == "__main__":
    ingest_documents()
