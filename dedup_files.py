from os import listdir, remove, path
from os.path import isfile, isdir, join, getctime
from hashlib import sha256
from sys import argv


class File_Record:
    def __init__(self, filename, extension, full_path, creation_time):
        self.filename = filename
        self.extension = extension
        self.full_path = full_path
        self.creation_time = creation_time

target_directory = ""
target_extensions = [
    ".mp4",
    ".jpg",
    ".png",
    ".jpeg",
    ".gif",
    ".bmp"
]

file_table = list()
file_hash_dict = dict()
duplicate_files = list()

remove_files = False

def parse_args():
    if len(argv) == 1:
        print("No file path provided.")
        exit(1)

    if isdir(argv[1]):
        global target_directory 
        target_directory = argv[1]
    else:
        print(f"Invalid path provided: {argv[1]}")
        exit(2)

    if len(argv) >= 3:
        if argv[2] == "-r":
            remove_files = True

def build_file_table():
    for f in listdir(target_directory):
        file_extension = path.splitext(f)[1]
        file_path = join(target_directory, f)
        if isfile(file_path) and file_extension in target_extensions:
            record = File_Record(f, file_extension, file_path, getctime(file_path))
            file_table.append(record)
    
    file_table.sort(key=lambda f: f.creation_time)

def find_duplicate_files():
    for f in file_table:
        file_object = open(f.full_path, "rb")
        file_data = file_object.read()
        file_object.close()
        file_hash = sha256(file_data).hexdigest()

        if file_hash_dict.get(file_hash) == None:
            file_hash_dict[file_hash] = list()
            
        file_hash_dict[file_hash].append(f)


def delete_duplicate_files():
    print(f"Deleting {str(len(duplicate_files))} duplicate(s)...")
    for f in duplicate_files:
        remove(f.full_path)
        print(f"Deleted {f.filename}")

def show_results():
    for file_hash, file_records in file_hash_dict.items():
        if len(file_records) > 1:
            for f in file_records[1:]:
                print(f"{file_hash[0:16]}: {f.filename}")
                duplicate_files.append(f)

def main():
    parse_args()
    build_file_table()
    find_duplicate_files()

    if len(file_hash_dict) > 0:
        show_results()
        if remove_files:
            delete_duplicate_files()
    else:
        print(f"No duplicate files found in target directory: {target_directory}.")

main()