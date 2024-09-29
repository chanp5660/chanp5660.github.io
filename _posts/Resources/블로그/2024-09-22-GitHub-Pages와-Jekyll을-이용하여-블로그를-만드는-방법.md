---
title: GitHub Pages와 Jekyll을 이용하여 블로그를 만드는 방법
create_date: 2024-09-22 21:54
status_complete: false
tags:
- github
- 블로그
- Jekyll
aliases: null
blog: true
mathjax: true
layout: post
---
연결 문서


# GitHub Pages와 Jekyll을 이용하여 블로그를 만드는 방법

## 1. GitHub 계정 생성하기

- 아직 GitHub 계정이 없다면 [GitHub](https://github.com/)에서 무료로 계정을 생성하세요.

## 2. Ruby와 Jekyll 설치하기

- **Ruby 설치하기**
  - **Windows**: [RubyInstaller](https://rubyinstaller.org/)를 사용하여 Ruby를 설치합니다.
  - **macOS**: 터미널에서 `brew install ruby` 명령어로 설치하거나, macOS에는 기본적으로 Ruby가 설치되어 있습니다.
  - **Linux**: 패키지 관리자를 사용하여 Ruby를 설치합니다 (`sudo apt-get install ruby` 등).

- **Jekyll 및 Bundler 설치하기**
  - 터미널이나 명령 프롬프트에서 다음 명령어를 실행합니다:
    ```
    gem install jekyll bundler
    ```

## 3. 새로운 Jekyll 사이트 생성하기

- 터미널에서 블로그를 만들고 싶은 디렉토리로 이동한 후, 다음 명령어를 실행합니다:
  ```
  jekyll new my-blog
  ```
- `my-blog`는 원하는 디렉토리 이름으로 변경 가능합니다.

## 4. 로컬에서 사이트 실행 및 테스트하기

- 생성된 디렉토리로 이동합니다:
  ```
  cd my-blog
  ```
- **디렉토리에 Gemfile에  추가** : `gem 'webrick'`
- 필요 라이브러리를 설치합니다:
  ```
  bundle install
  ```
- 로컬 서버를 실행합니다:
  ```
  bundle exec jekyll serve
  ```
- 브라우저에서 `http://localhost:4000`에 접속하여 사이트가 제대로 작동하는지 확인합니다.

## 5. GitHub 저장소 생성하기

- GitHub에서 **새로운 저장소**를 생성합니다.
- 저장소 이름은 `yourusername.github.io` 형식으로 지정해야 합니다. 여기서 `yourusername`은 당신의 GitHub 사용자명입니다.

## 6. 로컬 저장소와 GitHub 연동하기

- Git 초기화 및 원격 저장소 추가:
  ```
  git init
  git remote add origin https://github.com/yourusername/yourusername.github.io.git
  ```
- 모든 파일 추가 및 커밋:
  ```
  git add .
  git commit -m "Initial commit"
  ```
- 파일을 GitHub에 푸시:
  ```
  git push -u origin master
  ```

[[git 토큰으로 clone]]

[[사용된 github 공유 토큰]]
## 7. GitHub Pages 설정 확인하기

- GitHub 저장소의 **Settings** 탭으로 이동합니다.
- 좌측 메뉴에서 **Pages**를 선택하고, 소스 브랜치가 `master` 또는 `main`으로 설정되어 있는지 확인합니다.
- 몇 분 후에 `https://yourusername.github.io`에서 블로그를 확인할 수 있습니다.

## 8. Markdown 파일로 게시물 작성하기

- `_posts` 폴더에서 새로운 Markdown 파일을 생성합니다.
- 파일명은 `YYYY-MM-DD-제목.md` 형식이어야 합니다 (예: `2023-10-01-hello-world.md`).
- 파일의 맨 위에 다음과 같은 Front Matter를 추가합니다:
  ```
  ---
  layout: post
  title:  "게시물 제목"
  date:   2023-10-01 12:00:00 +0900
  categories: 카테고리명
  ---
  ```
- 그 아래에 Markdown 형식으로 내용을 작성합니다.

## 9. 테마 및 스타일 적용하기

- **테마 선택** : [Jekyll 테마 다운로드](https://chanp5660.github.io/blog/2024/Jekyll-테마-다운로드/)
  - [Jekyll 테마](https://jekyllthemes.io/) 사이트에서 마음에 드는 테마를 선택합니다.
  - Gem 기반 테마의 경우, `Gemfile`과 `_config.yml` 파일을 수정하여 테마를 적용합니다.
- **CSS 커스터마이징**
  - `_sass` 폴더나 `assets/css` 폴더에서 스타일을 수정하여 원하는 디자인을 적용할 수 있습니다.

## 10. 변경사항을 GitHub에 반영하기

- 새로운 게시물이나 변경사항이 있을 때마다 다음 명령어로 업데이트합니다:
  ```
  git add .
  git commit -m "Add new post"
  git push
  ```
- GitHub Pages는 자동으로 사이트를 다시 빌드하고 업데이트합니다.

[md 파일 변경 후 업데이트](https://chanp5660.github.io/blog/2024/md-파일-변경-후-업데이트/)
## 추가 참고 사항

- **플러그인 제한**: GitHub Pages에서는 보안상의 이유로 일부 Jekyll 플러그인을 지원하지 않습니다. 필요한 경우 [GitHub Actions](https://docs.github.com/en/actions)로 사이트를 빌드하여 배포할 수 있습니다.
- **커스텀 도메인 사용**: 개인 도메인을 연결하려면 저장소 루트에 `CNAME` 파일을 생성하고, 도메인 DNS 설정에서 `A` 레코드나 `CNAME` 레코드를 설정해야 합니다.
- **공식 문서 참고**:
  - [Jekyll 공식 문서](https://jekyllrb.com/docs/)
  - [GitHub Pages 가이드](https://docs.github.com/en/pages)

이러한 단계들을 따라하면 GitHub Pages와 Jekyll을 이용하여 Markdown 파일로 블로그를 손쉽게 만들 수 있습니다. 추가적인 도움이 필요하시면 공식 문서를 참고하시거나 관련 커뮤니티에 질문해보세요.