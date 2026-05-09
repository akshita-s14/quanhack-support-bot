import os
import csv

KB_DIR = "knowledge_base"

def convert_csv_to_txt():
    if not os.path.exists(KB_DIR):
        print(f"Error: Directory '{KB_DIR}' not found.")
        return

    csv_files = [f for f in os.listdir(KB_DIR) if f.endswith(".csv")]
    
    if not csv_files:
        print(f"No .csv files found in '{KB_DIR}'. Please move your Kaggle dataset there.")
        return

    for filename in csv_files:
        csv_path = os.path.join(KB_DIR, filename)
        txt_filename = filename.replace(".csv", ".txt")
        txt_path = os.path.join(KB_DIR, txt_filename)
        
        print(f"Converting {filename} to {txt_filename}...")
        
        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
                reader = csv.DictReader(csvfile)
                
                with open(txt_path, 'w', encoding='utf-8') as txtfile:
                    for i, row in enumerate(reader, start=1):
                        txtfile.write(f"--- Entry {i} ---\n")
                        for col_name, col_value in row.items():
                            if col_value and str(col_value).strip():
                                txtfile.write(f"{col_name}: {col_value}\n")
                        txtfile.write("\n")
                        
            print(f"✅ Successfully converted! You can now run ingest.py to load {txt_filename} into the AI.")
        except Exception as e:
            print(f"❌ Error converting {filename}: {e}")

if __name__ == "__main__":
    convert_csv_to_txt()
