import os
import shutil
import hashlib
import re

def extract_publish_file(file_path):
    """
    Extracts the publish_file field value from the .md file.
    """
    publish_file = None
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read the first line
        first_line = f.readline().strip()
        if first_line == '---':
            # Read until the second '---'
            content = f.read()
            match = re.search(r'publish_file:\s*(.*?)\s', content, re.DOTALL)
            if match:
                publish_file = match.group(1)
    return publish_file

def try_publish_file(file_path,dest_file):
    """
    Copies .md files from source directory to destination directory.
    """
    # Check if the destination file exists and has the same content
    if os.path.exists(dest_file):
        if file_md5(file_path) == file_md5(dest_file):
            # print(f"Skipping {dest_file} as it already exists and has the same content.")
            return
    shutil.copyfile(file_path, dest_file)
    print(f"Copied {dest_file} to _posts directory.")

def file_md5(file_path):
    """
    Calculates the MD5 hash of a file.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buffer = f.read(65536)  # Read file in chunks to conserve memory
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = f.read(65536)
    return hasher.hexdigest()

def process_notes_directory(directory,dest_dir):
    """
    Processes all .md files in a directory and its subdirectories.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                publish_file = extract_publish_file(file_path)
                if publish_file:
                    dest_file = os.path.join(dest_dir,publish_file)
                    try_publish_file(file_path,dest_file)
                    

if __name__ == "__main__":
    notes_directory = "_notes"
    posts_directory = "_posts"
    process_notes_directory(notes_directory,posts_directory)
