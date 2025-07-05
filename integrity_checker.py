import hashlib
import os
import json
import time

HASH_DB_FILE = 'hash_database.json'

def calculate_hash(filepath, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def load_hash_database():
    if os.path.exists(HASH_DB_FILE):
        with open(HASH_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hash_database(db):
    with open(HASH_DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

def monitor_directory(directory):
    hash_db = load_hash_database()
    updated_db = {}

    print(f"\n[INFO] Scanning directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)

            updated_db[filepath] = file_hash

            if filepath not in hash_db:
                print(f"[NEW FILE] {filepath}")
            elif hash_db[filepath] != file_hash:
                print(f"[MODIFIED] {filepath}")
            else:
                print(f"[UNCHANGED] {filepath}")

    removed_files = set(hash_db.keys()) - set(updated_db.keys())
    for filepath in removed_files:
        print(f"[REMOVED] {filepath}")

    save_hash_database(updated_db)
    print("\n[INFO] Scan complete.\n")

# Example usage
if __name__ == "__main__":
    target_directory = input("Enter directory path to monitor: ").strip()
    while not os.path.isdir(target_directory):
        print("Invalid directory. Please try again.")
        target_directory = input("Enter directory path to monitor: ").strip()
    
    monitor_directory(target_directory)
