import os


os.makedirs("test_folder/subfolder", exist_ok=True)

print("Directories created")

files = os.listdir(".")
print("Files and folders:")
print(files)