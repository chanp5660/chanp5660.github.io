---
title: al-folio toc 표시
create_date: 2024-10-06 01:14
status_complete: false
tags:
- al-folio
- 블로그
aliases: null
blog: true
mathjax: true
layout: post
toc:
  sidebar: left
---
연결 문서

[a post with table of contents on a sidebar](https://alshedivat.github.io/al-folio/blog/2023/sidebar-table-of-contents/)  
[Table of Contents plugin for Bootstrap](https://afeld.github.io/bootstrap-toc/)
# al-folio toc 표시

이 글은 포스트에 사이드바 형식으로 목차(Table of Contents, TOC)를 추가하는 방법을 설명함. 요약하자면 아래와 같음:

1. **목차 추가 방법**:
   - 글의 front matter(프론트 매터)에 아래와 같은 코드를 추가하여 사이드바에 목차를 표시할 수 있음.
     ```yaml
     toc:
       sidebar: left
     ```
   - 이 코드는 왼쪽에 목차를 나타내는 예시이며, "left"를 "right"로 변경하면 목차를 오른쪽에 표시할 수 있음.
   - 목차는 글의 제목과 부제목을 기반으로 자동 생성됨.

2. **목차 커스터마이징**:
   - 더 자세히 커스터마이징 하고 싶다면, `bootstrap-toc` 문서를 참고할 것을 권장함.
   - 목차에 표시되는 제목 텍스트도 수정 가능함.

## 옵시디언 파일의 table-of-contents 와 겹치는 문제 해결 

- 옵시디언에서는  를 사용하는데 이러면 2개의 toc 가 생기는 문제가 생기고 실제로 html로는 표시가 되지 않는 문제가 발생
- 이를 해결하기 위해서 옵시디언 동기화 파일에서  를 직접 제거해주는 코드를 추가한다.
```python
# 'table-of-contents[\s\S]*?```', '', content_without_front_matter, flags=re.MULTILINE)
```

- 또한 프론트매터에 toc 표시 조건을 추가한다.
```python
# 프론트매터에 'toc: sidebar: left' 추가
metadata['toc'] = {'sidebar': 'left'}
```


## Bootstrap 기반의 웹 페이지에 자동으로 목차(Table of Contents, TOC)를 생성해주는 플러그인 사용 방법과 커스터마이징

주요 기능은 [앵커 링크](https://chanp5660.github.io/blog/2024/앵커-링크/) 를 사용해서 문서 탐색 속도를 향상 시킴.


1. **플러그인의 기능**:
   - `<h1>`, `<h2>` 등 제목 요소를 기반으로 자동으로 목차를 생성함.
   - Bootstrap v3 문서 사이트의 사이드바처럼 페이지의 목차를 자동으로 업데이트해줌.
   - 제목에 ID가 없으면 자동으로 ID가 생성되며, 이 ID는 URL로 앵커 링크를 걸 수 있게 해줌.
   
2. **설치 및 설정**:
   - jQuery와 Bootstrap(v4 또는 v5)을 세팅한 후, 아래 코드를 추가하여 플러그인을 활성화함.
     ```html
     <link rel="stylesheet" href="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.1/dist/bootstrap-toc.min.css" />
     <script src="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.1/dist/bootstrap-toc.min.js"></script>
     ```
   - 목차를 표시할 위치에 `<nav id="toc" data-toggle="toc"></nav>` 요소를 추가함.
   - Bootstrap의 Scrollspy 플러그인을 사용하여, `<body>` 요소에 추가 설정을 해야 함.

3. **레이아웃 설정**:
   - Bootstrap의 Scrollspy 기능을 이용하여 페이지 내에서 스크롤할 때, 목차가 자동으로 활성화됨.
   - 목차를 화면에 고정(sticky)하거나 모바일에서 목차를 상단에 배치할 수 있는 레이아웃 구성을 제공함.

4. **커스터마이징**:
   - `Toc.init()`을 통해 jQuery 객체로 특정 제목만 선택하거나 목차의 표시 형식을 수정할 수 있음.
   - `<h2>` 등의 제목 요소에 `data-toc-text` 속성을 추가하여 목차에 표시되는 텍스트를 사용자 정의할 수 있음.
   - 특정 제목을 목차에 포함시키지 않으려면, `data-toc-skip` 속성을 추가함.

5. **추가 사항**:
   - 작은 화면에서는 목차가 확장되지 않도록 하거나, 두 번째 레벨의 목차도 표시되도록 선택할 수 있음.