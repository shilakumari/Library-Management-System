# import csv
# import os
# from models import Book, Member, Loan

# def load_csv(filepath):
#     if not os.path.exists(filepath):
#         return []
#     with open(filepath, newline='', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         return list(reader)

# def save_csv(filepath, data, fieldnames):
#     with open(filepath, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(data)



import csv
import os
from models import Book, Member, Loan

DATA_DIR = 'data'

def set_data_dir(path):
    global DATA_DIR
    DATA_DIR = path

def _full_path(filename):
    return os.path.join(DATA_DIR, filename)

def load_csv(filename):
    filepath = _full_path(filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_csv(filename, data, fieldnames):
    filepath = _full_path(filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)