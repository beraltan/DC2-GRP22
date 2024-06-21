import os

def generate_tree(dir_path, prefix=""):
    contents = sorted(os.listdir(dir_path))
    pointers = [ "├── "] * (len(contents) - 1) + ["└── "]

    for pointer, content in zip(pointers, contents):
        path = os.path.join(dir_path, content)
        if os.path.isdir(path):
            print(f"{prefix}{pointer}{content}/")
            generate_tree(path, prefix + "│   ")
        else:
            print(f"{prefix}{pointer}{content}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    print(directory)
    generate_tree(directory)
