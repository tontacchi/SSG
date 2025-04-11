#---[ Global Imports ]----------------------------------------------------------
import os
from   pathlib import Path
import shutil

from   utils   import extract_title, markdown_to_html_node

#---[ Global Imports ]----------------------------------------------------------


#---[ Main Function ]-----------------------------------------------------------
def main():
    remove_public_dir_files()

    static_dir = get_project_dir("static")
    public_dir = get_project_dir("public")
    copy_files(static_dir, public_dir)

    content_dir  = get_project_dir("content")
    template_dir = get_project_dir(".") / "template.html"

    print("")
    generate_pages_recursively(content_dir, template_dir, public_dir)

    return

#---[ Main Function ]-----------------------------------------------------------

def get_project_dir(subdir: str) -> Path:
    script_dir = Path(__file__).parent.resolve()
    target_dir = script_dir.parent.resolve() / subdir 
    if not target_dir.exists():
        target_dir.mkdir()

    return target_dir

def remove_files(directory: Path) -> None:
    for file in directory.iterdir():
        if file.is_dir():
            remove_files(file)
            os.rmdir(file)
        else:
            os.remove(file)

    return

def copy_files(source_dir: Path, target_dir: Path) -> None:
    print("copying files:")
    print(f"source: {source_dir.parent.name}/{source_dir.name}")
    print(f"dest: {target_dir.parent.name}/{target_dir.name}")
    for file in source_dir.iterdir():
        if file.is_dir():
            new_directory = target_dir / f"{file.name}"
            print(f"creating directory {new_directory.parent.name}/{new_directory.name}")
            os.mkdir(new_directory)
            copy_files(file, new_directory)
        else:
            print(f"copying {file.name}")
            shutil.copy(file, target_dir / f"{file.name}")

    return

def remove_public_dir_files() -> None:
    public_dir = get_project_dir("public")
    remove_files(public_dir)

    return

def generate_page(src_path: Path, template_path: Path, dest_path: Path) -> bool:
    short_src_path      = f"{src_path.parent.parent.name}/{src_path.parent.name}/{src_path.name}"
    short_template_path = f"{template_path.parent.parent.name}/{template_path.parent.name}/{template_path.name}"
    short_dest_path     = f"{dest_path.parent.parent.name}/{dest_path.parent.name}/{dest_path.name}"
    message = f"Generating page from {short_src_path} to {short_dest_path} using {short_template_path}"

    print(message)

    markdown = ""
    with src_path.open("r") as inFile:
        markdown = inFile.read()

        if markdown == "":
            return False

    template = ""
    with template_path.open('r') as inFile:
        template = inFile.read()

        if template == "":
            return False

    root_node = markdown_to_html_node(markdown)

    content = root_node.to_html()
    title = extract_title(markdown)

    html_str = template.replace("{{ Title }}", title)
    html_str = html_str.replace("{{ Content }}", content)

    with dest_path.open('w') as outFile:
        outFile.write(html_str)

    return True

def generate_pages_recursively(content_path: Path, template_path: Path, dest_path: Path) -> None:
    for path in content_path.iterdir():
        if path.is_dir():
            new_dest = dest_path / path.name
            if not new_dest.exists():
                new_dest.mkdir()

            generate_pages_recursively(path, template_path, new_dest)
        elif path.name.endswith(".md"):
            file_dest_path = dest_path / str(path.name).replace(".md", ".html")
            generate_page(path, template_path, file_dest_path)

    return


#---[ Entry ]-------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---[ Entry ]-------------------------------------------------------------------
