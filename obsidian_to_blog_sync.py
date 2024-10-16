import os
import yaml
import re
import shutil
from pathlib import Path
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
    folder_path = Path(folder_path)
    print(folder_path)
    exclude_dirs = {'Planner', 'Areas'}
    
    for md_file in folder_path.glob('**/*.md'):
        # 제외할 디렉토리와 숨김 폴더 처리
        if any(part in exclude_dirs for part in md_file.parts):
            continue
        if any(part.startswith('.') for part in md_file.parts):
            continue
        try:
            with md_file.open('r', encoding='utf-8') as f:
                content = f.read()
                # YAML 프론트 매터 추출
                yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n?', content, re.DOTALL)
                if yaml_match:
                    yaml_content = yaml_match.group(1)
                    try:
                        metadata = yaml.safe_load(yaml_content)
                        # 'blog: true'인 경우 추가
                        if isinstance(metadata, dict) and metadata.get('blog') == True:
                            md_files_with_metadata.append((md_file, metadata, content))
                    except yaml.YAMLError as e:
                        print(f"YAML parsing error ({md_file}): {e}")
        except Exception as e:
            print(f"Error opening file {md_file}: {e}")
    return md_files_with_metadata
    
def generate_destination_path(md_file, metadata, folder_path, destination_base):
    """
    마크다운 파일의 메타데이터와 원래 위치를 기반으로 대상 경로를 생성합니다.

    매개변수:
        md_file (Path): 마크다운 파일의 경로.
        metadata (dict): 마크다운 파일의 YAML 프론트 매터 메타데이터.
        folder_path (Path): 원래 폴더 경로.
        destination_base (Path): 대상 기본 폴더 경로.

    반환값:
        Path 또는 None: 대상 파일 경로를 반환하거나, 오류가 발생하면 None을 반환합니다.
    """
    md_file = Path(md_file)
    folder_path = Path(folder_path)
    destination_base = Path(destination_base)

    # 원본 폴더로부터의 상대 경로 계산
    try:
        relative_path = md_file.relative_to(folder_path)
    except ValueError:
        print(f"File {md_file} is not under folder {folder_path}")
        return None

    # 디렉토리와 파일명 분리
    relative_dir = relative_path.parent
    original_filename = relative_path.name

    # 파일명과 확장자 분리
    filename_without_ext = original_filename.rsplit('.', 1)[0]
    ext = '.' + original_filename.rsplit('.', 1)[1] if '.' in original_filename else ''

    # 파일명과 디렉토리명에서 공백을 하이픈으로 변경
    modified_filename = filename_without_ext.replace(' ', '-')
    modified_relative_dir = Path(*[d.replace(' ', '-') for d in relative_dir.parts])

    # create_date 추출 및 포맷
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

    # 새로운 파일명 생성
    new_filename = f"{date_prefix}-{modified_filename}{ext}"
    # 새로운 상대 경로 생성
    new_relative_path = modified_relative_dir / new_filename
    # 전체 대상 경로 생성
    destination_path = destination_base / new_relative_path
    return destination_path

def synchronize_folders(folder_path, destination_base):
    """
    마크다운 파일을 소스 폴더에서 대상 폴더로 동기화하며, 메타데이터에 'blog: true'가 포함된 파일을 처리하고 링크와 내용을 적절하게 업데이트합니다.

    매개변수:
        folder_path (str 또는 Path): 소스 폴더 경로.
        destination_base (str 또는 Path): 대상 폴더 경로.

    """
    folder_path = Path(folder_path)
    destination_base = Path(destination_base)

    # 'blog: true'인 마크다운 파일 목록 가져오기
    md_files_with_metadata = get_md_files_with_blog_true(folder_path)

    # 대상 폴더에 존재하는 마크다운 파일 목록 가져오기
    existing_files_in_destination = list(destination_base.glob('**/*.md'))

    # 소스 파일에서 대상 경로로의 매핑 생성
    source_to_destination = {}
    # 링크 매핑 생성 (파일 제목: URL)
    title_to_url = {}
    for md_file, metadata, original_content in md_files_with_metadata:
        destination_path = generate_destination_path(md_file, metadata, folder_path, destination_base)
        if destination_path:
            source_to_destination[md_file] = (destination_path, metadata, original_content)
            # URL 생성
            if 'title' in metadata and 'create_date' in metadata:
                title = metadata['title']
                url_title = title.replace(' ', '-')
                # create_date에서 연도 추출
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
                # URL 생성
                url = f"https://chanp5660.github.io/blog/{year}/{url_title}/"
                title_to_url[title] = url

    # 대상 파일 목록
    destination_files = [dest_path for dest_path, _, _ in source_to_destination.values()]

    # 대상 폴더에서 소스에 없는 파일 삭제
    for existing_file in existing_files_in_destination:
        if existing_file not in destination_files:
            existing_file.unlink()
            print(f"Deleted: {existing_file}")

    # 파일 복사 및 업데이트
    for md_file, (destination_path, metadata, original_content) in source_to_destination.items():
        md_file = Path(md_file)
        destination_path = Path(destination_path)
        # 대상 디렉토리 생성
        destination_dir = destination_path.parent
        if not destination_dir.exists():
            destination_dir.mkdir(parents=True)
        # 파일 복사 여부 결정
        if (not destination_path.exists()) or (md_file.stat().st_mtime > destination_path.stat().st_mtime):
            # YAML 프론트 매터 수정
            metadata['mathjax'] = True
            metadata['layout'] = 'post'
            metadata['toc'] = {'sidebar': 'left'}
            # 메타데이터를 YAML 문자열로 변환
            new_yaml_content = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
            # 새로운 프론트 매터 생성
            new_front_matter = f"---\n{new_yaml_content}---\n"
            # 기존 프론트 매터 제거
            content_without_front_matter = re.sub(r'^---\s*\n(.*?)\n---\s*\n?', '', original_content, flags=re.DOTALL)
            # '```table-of-contents' 코드 블록 제거
            content_without_toc = re.sub(r'```table-of-contents[\s\S]*?```', '', content_without_front_matter, flags=re.MULTILINE)
            # 콘텐츠 내 링크 업데이트
            def replace_link(match):
                full_match = match.group(0)
                link_text = match.group(1)
                if link_text.startswith('#'):
                    return full_match
                else:
                    link_text = link_text.strip()
                    if link_text in title_to_url:
                        url = title_to_url[link_text]
                        return f"[{link_text}]({url})"
                    else:
                        return full_match

            content_updated_links = re.sub(r'\[\[([^\[\]]+)\]\]', replace_link, content_without_toc)
            # 새로운 콘텐츠 생성
            new_content = new_front_matter + content_updated_links
            # 수정된 콘텐츠를 대상 파일에 쓰기
            with destination_path.open('w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Copied and modified: {md_file} -> {destination_path}")
        else:
            continue

# 실행 부분
save_path = Path('C:\\Users\\master\\Desktop\\PARA')
# 소스 폴더 경로 설정
if save_path.exists():
    source_path = save_path
else:
    source_path = Path('C:\\Users\\user\\Desktop\\chanp5660\\PARA')

target_path = Path('.\\_posts')  # 대상 폴더 경로 설정

synchronize_folders(source_path, target_path)