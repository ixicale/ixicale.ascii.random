import os

from run import ASCII_ART


def generate_md_file():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "ascii preview", "README.md")
    with open(file_path, "+w") as f:
        f.write(f"# Available ASCII ART\n\n")
        for key, value in ASCII_ART.items():
            f.write(f"## {key}\n")
            f.write(f"```coffe\n{value}\n```\n\n")

if __name__ == "__main__":
    generate_md_file()