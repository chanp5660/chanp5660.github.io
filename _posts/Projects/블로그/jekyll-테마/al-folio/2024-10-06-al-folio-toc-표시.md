---
title: al-folio toc 표시
create_date: 2024-10-06 01:14
status_complete: false
tags:
- al-folio
- 블로그
aliases: null
blog: true
featured: true
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
	   - Bootstrap : **Bootstrap**은 웹 페이지를 쉽게 디자인할 수 있도록 도와주는 오픈소스 도구 모음임.
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

## Toc 목차 H4 까지 표시하기

al-folio Jekyll 테마에서 **H4**까지의 제목을 목차(TOC) 사이드바에 표시하려면, TOC가 초기화되는 JavaScript 파일을 수정해야 함. 관련 파일은 `common.js`임.

**수정 방법:**

1. **`common.js` 파일 찾기:**

   이 파일은 일반적으로 al-folio Jekyll 테마의 `assets/js/` 디렉터리에 있음.

2. **TOC 초기화 코드 수정:**

   `common.js`에서 TOC가 초기화되는 부분을 찾음. 대략 다음과 같이 생김:

   ```javascript
   // bootstrap-toc
   if ($("#toc-sidebar").length) {
     // remove related publications years from the TOC
     $(".publications h2").each(function () {
       $(this).attr("data-toc-skip", "");
     });
     var navSelector = "#toc-sidebar";
     var $myNav = $(navSelector);
     Toc.init($myNav);
     $('body').scrollspy({
       target: navSelector,
     });
   }
   ```

3. **TOC 초기화 코드에서 H4 제목을 포함하도록 수정:**

   `Toc.init()` 함수 호출을 `$scope` 옵션으로 수정하여 포함할 제목 레벨을 지정함.

   **이 부분을:**

   ```javascript
   Toc.init($myNav);
   ```

   **다음과 같이 변경:**

   ```javascript
   Toc.init({
     $nav: $myNav,
     $scope: $('h2, h3, h4'), // H2, H3, H4 제목 포함
   });
   ```

   이 수정은 TOC 플러그인에 `<h2>`, `<h3>`, `<h4>` 제목을 포함하도록 지시함.

4. **변경 사항 저장 후 사이트 재빌드:**

   `common.js` 파일을 저장한 후, Jekyll 사이트를 재빌드하여 업데이트된 TOC를 확인함.

**설명:**

- **왜 `common.js` 파일을 수정하는가?**: 이 파일은 al-folio 테마에서 TOC 플러그인을 초기화하는 코드를 포함하고 있음.
- **`$scope` 사용 이유:** 기본적으로 TOC 플러그인은 여러 번 나타나는 제목 수준을 기준으로 포함할 제목을 결정함. `$scope` 옵션을 사용하면 명시적으로 포함할 제목 레벨을 정의할 수 있음.
- **H4 제목 포함:** `$scope` 선택기에 `'h4'`를 추가하면 `<h4>` 제목도 TOC에 포함됨.

**최종 수정된 `common.js` 코드:**

```javascript
$(document).ready(function () {
  // add toggle functionality to abstract, award and bibtex buttons
  $("a.abstract").click(function () {
    $(this).parent().parent().find(".abstract.hidden").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.award").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.bibtex").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden").toggleClass("open");
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init({
      $nav: $myNav,
      $scope: $('h2, h3, h4'), // H2, H3, H4 제목 포함
    });
    $('body').scrollspy({
      target: navSelector,
    });
  }

  // add css to jupyter notebooks
  // ... 나머지 코드 ...
});
```

이 과정을 따르면 목차 사이드바에 **H4**까지의 제목이 표시됨.

---

**추가 참고사항:**

- 더 깊은 제목 수준(H5, H6 등)을 포함하려면 `$scope` 선택기를 다음과 같이 확장 가능:

```javascript
Toc.init({
  $nav: $myNav,
  $scope: $('h2, h3, h4, h5, h6'),
});
```

컨텐츠 구조에 따라 제목 레벨을 조정하면 됨.

- Header 에 `## 1. 제목`
 과 같은 형태는 bootstrap-toc 움직임이 제대로 따라가지 않음, `## 제목 1.2` 이런 형태는 움직임이 제대로 따라감

 움직임을 따라가는 예시  
 
![](https://i.imgur.com/R1zxXGK.png)

움직임을 못 따라가는 예시  

![](https://i.imgur.com/Z5316pC.png)


### toc 가 한칸 위가 표시되는 문제

`.` 이 있지만 따라가는 형식 ( 한칸 위가 표시되는 것은 원래부터 그랬기도 하고 내용을 이해하는데 크게 문제가 있을 것 같지 않아서 해결하지 않음 )
![](https://i.imgur.com/EfvFIMb.png)

