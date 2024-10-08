import os
import yaml
import re
import shutil
from datetime import datetime

def get_md_files_with_blog_true(folder_path):
    """
    지정된 폴더 내에서 YAML 프론트 매터에 'blog: true'가 포함된 마크다운 파일을 재귀적으로 검색합니다.

    매개변수:
        folder_path (str): 검색할 폴더의 경로.

    반환값:
        list: 파일 경로, 메타데이터 딕셔너리, 파일 내용을 포함하는 튜플 목록.
    """
    md_files_with_metadata = []
    # 모든 하위 파일 목록
    for root, dirs, files in os.walk(folder_path):
        # 특정 디렉토리 이름을 제외하고 싶을 때
        exclude_dirs = {'Planner', 'Areas'}

        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract YAML front matter using regular expressions
                    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n?', content, re.DOTALL)
                    if yaml_match:
                        yaml_content = yaml_match.group(1)
                        try:
                            metadata = yaml.safe_load(yaml_content)
                            # Check if metadata is a dictionary and 'blog' is True
                            if isinstance(metadata, dict) and 'blog' in metadata and metadata['blog'] == True:
                                md_files_with_metadata.append((full_path, metadata, content))
                        except yaml.YAMLError as e:
                            print(f"YAML parsing error ({full_path}): {e}")
    return md_files_with_metadata
    
def generate_destination_path(md_file, metadata, folder_path, destination_base):
    """
    마크다운 파일의 메타데이터와 원래 위치를 기반으로 대상 경로를 생성합니다.

    매개변수:
        md_file (str): 마크다운 파일의 경로.
        metadata (dict): 마크다운 파일의 YAML 프론트 매터 메타데이터.
        folder_path (str): 원래 폴더 경로.
        destination_base (str): 대상 기본 폴더 경로.

    반환값:
        str 또는 None: 대상 파일 경로를 반환하거나, 오류가 발생하면 None을 반환합니다.
    """
    # Calculate the relative path from the original folder
    relative_path = os.path.relpath(md_file, folder_path)
    # Split into directory and filename
    relative_dir, original_filename = os.path.split(relative_path)
    # Split filename and extension
    filename_without_ext, ext = os.path.splitext(original_filename)
    # Replace spaces in filename with hyphens
    modified_filename = filename_without_ext.replace(' ', '-')
    # Replace spaces in directory names with hyphens
    dir_components = relative_dir.split(os.sep)
    modified_dir_components = [d.replace(' ', '-') for d in dir_components]
    # Reconstruct the modified relative_dir
    modified_relative_dir = os.path.join(*modified_dir_components)
    # Extract create_date and use only the date part
    if 'create_date' in metadata:
        create_date_str = str(metadata['create_date'])
        try:
            create_date = datetime.strptime(create_date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                create_date = datetime.strptime(create_date_str, '%Y-%m-%d')
            except ValueError:
                print(f"Date format error ({md_file}): {create_date_str}")
                return None
        date_prefix = create_date.strftime('%Y-%m-%d')
    else:
        print(f"No create_date found ({md_file})")
        return None
    # Create new filename
    new_filename = f"{date_prefix}-{modified_filename}{ext}"
    # Create new relative path
    new_relative_path = os.path.join(modified_relative_dir, new_filename)
    # Generate the full destination path
    destination_path = os.path.join(destination_base, new_relative_path)
    return destination_path

def synchronize_folders(folder_path, destination_base):
    """
    마크다운 파일을 소스 폴더에서 대상 폴더로 동기화하며, 메타데이터에 'blog: true'가 포함된 파일을 처리하고 링크와 내용을 적절하게 업데이트합니다.

    매개변수:
        folder_path (str): 소스 폴더 경로.
        destination_base (str): 대상 폴더 경로.

    """
    # Get the list of Markdown files with 'blog: true'
    md_files_with_metadata = get_md_files_with_blog_true(folder_path)

    # Get the list of existing Markdown files in the destination
    existing_files_in_destination = []
    for root, dirs, files in os.walk(destination_base):
        for file in files:
            if file.endswith('.md'):
                existing_files_in_destination.append(os.path.join(root, file))

    # Create a mapping from source files to destination paths
    source_to_destination = {}
    # Create link mapping (file title: URL)
    title_to_url = {}
    for md_file, metadata, original_content in md_files_with_metadata:
        destination_path = generate_destination_path(md_file, metadata, folder_path, destination_base)
        if destination_path:
            source_to_destination[md_file] = (destination_path, metadata, original_content)
            # Generate URL based on permalink structure in config.yml
            if 'title' in metadata and 'create_date' in metadata:
                title = metadata['title']
                url_title = title.replace(' ', '-')
                # Extract year from create_date
                create_date_str = str(metadata['create_date'])
                try:
                    create_date = datetime.strptime(create_date_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    try:
                        create_date = datetime.strptime(create_date_str, '%Y-%m-%d')
                    except ValueError:
                        print(f"Date format error ({md_file}): {create_date_str}")
                        continue
                year = create_date.strftime('%Y')
                # Generate URL based on the permalink structure '/blog/:year/:title/'
                url = f"https://chanp5660.github.io/blog/{year}/{url_title}/"
                title_to_url[title] = url

    # List of destination files
    destination_files = [dest_path for dest_path, _, _ in source_to_destination.values()]

    # Remove files from destination that are not in source
    for existing_file in existing_files_in_destination:
        if existing_file not in destination_files:
            os.remove(existing_file)
            print(f"Deleted: {existing_file}")

    # Copy and update files
    for md_file, (destination_path, metadata, original_content) in source_to_destination.items():
        # Create destination directory if it doesn't exist
        destination_dir = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # Copy the file if it doesn't exist or if the source is newer
        if (not os.path.exists(destination_path)) or (os.path.getmtime(md_file) > os.path.getmtime(destination_path)):
            # Modify YAML front matter
            metadata['mathjax'] = True
            metadata['layout'] = 'post'
            # 프론트매터에 'toc: sidebar: left' 추가
            metadata['toc'] = {'sidebar': 'left'}
            # Convert metadata back to YAML string
            new_yaml_content = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
            # Reconstruct YAML front matter
            new_front_matter = f"---\n{new_yaml_content}---\n"
            # Replace existing YAML front matter in content
            content_without_front_matter = re.sub(r'^---\s*\n(.*?)\n---\s*\n?', '', original_content, flags=re.DOTALL)
            # '```table-of-contents' 코드 블록 제거
            content_without_toc = re.sub(r'```table-of-contents[\s\S]*?```', '', content_without_front_matter, flags=re.MULTILINE)
            # Update links in content
            # Pattern: [[File Title]] (excluding [[#File Title]])
            def replace_link(match):
                full_match = match.group(0)
                link_text = match.group(1)
                if link_text.startswith('#'):
                    # Do not change [[#File Title]] patterns
                    return full_match
                else:
                    # Strip leading and trailing whitespace from link text
                    link_text = link_text.strip()
                    if link_text in title_to_url:
                        url = title_to_url[link_text]
                        return f"[{link_text}]({url})"
                    else:
                        return full_match  # Do not change if no mapping exists

            content_updated_links = re.sub(r'\[\[([^\[\]]+)\]\]', replace_link, content_without_toc)
            # Combine new front matter with updated content
            new_content = new_front_matter + content_updated_links
            # Write the modified content to the destination file
            with open(destination_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Copied and modified: {md_file} -> {destination_path}")
        else:
            #print(f"Up to date: {destination_path}")
            continue

# Execution part
# 특정 경로가 있는지에 따라 어떤 컴퓨터에서 실행되는지 확인
# 'C:\\Users\\master\\Desktop\\PARA' 폴더가 있고 없는 경우에 따라 sorce_path를 다르게 설정

save_path = 'C:\\Users\\master\\Desktop\\PARA'
# Change to your source folder path.
if os.path.exists(save_path):
    source_path = 'C:\\Users\\master\\Desktop\\PARA'
else:
    source_path = 'C:\\Users\\user\\Desktop\\PARA'

target_path = '.\\_posts'  # Change to your destination folder path.

synchronize_folders(source_path, target_path)
