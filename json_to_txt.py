import os
import json

KB_DIR = "knowledge_base"

def convert_json_to_txt():
    if not os.path.exists(KB_DIR):
        print(f"Error: Directory '{KB_DIR}' not found.")
        return

    json_files = [f for f in os.listdir(KB_DIR) if f.endswith(".json")]
    
    if not json_files:
        print(f"No .json files found in '{KB_DIR}'. Please move your Kaggle JSON file there.")
        return

    for filename in json_files:
        json_path = os.path.join(KB_DIR, filename)
        txt_filename = filename.replace(".json", ".txt")
        txt_path = os.path.join(KB_DIR, txt_filename)
        
        print(f"Converting {filename} to {txt_filename}...")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                
            with open(txt_path, 'w', encoding='utf-8') as txtfile:
                # Handle standard Kaggle "intents.json" format
                if "intents" in data:
                    for intent in data["intents"]:
                        tag = intent.get("tag", "Unknown Topic")
                        patterns = intent.get("patterns", [])
                        responses = intent.get("responses", [])
                        
                        txtfile.write(f"--- Topic: {tag} ---\n")
                        txtfile.write(f"Common Questions: {', '.join(patterns)}\n")
                        txtfile.write(f"Official Response: {', '.join(responses)}\n\n")
                
                # Handle generic JSON array format
                elif isinstance(data, list):
                    for i, item in enumerate(data, start=1):
                        txtfile.write(f"--- Entry {i} ---\n")
                        if isinstance(item, dict):
                            for k, v in item.items():
                                txtfile.write(f"{k}: {v}\n")
                        else:
                            txtfile.write(f"{item}\n")
                        txtfile.write("\n")
                        
                else:
                    # Handle generic dictionary
                    for k, v in data.items():
                        txtfile.write(f"{k}: {v}\n")
                        
            print(f"✅ Successfully converted! You can now run ingest.py to load {txt_filename} into the AI.")
        except Exception as e:
            print(f"❌ Error converting {filename}: {e}")

if __name__ == "__main__":
    convert_json_to_txt()
