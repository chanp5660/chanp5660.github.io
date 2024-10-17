---
title: gitignore 에 있는 파일 원격 저장소 에서 제거
create_date: 2024-08-14 16:13
status_complete: false
tags:
- git
- github
aliases: null
blog: true
mathjax: true
layout: post
toc:
  sidebar: left
---
연결 문서

[Git에 tracking중인 file을 ignore 하는 방법](https://cppmaster.tistory.com/entry/Git%EC%97%90-tracking%EC%A4%91%EC%9D%B8-file%EC%9D%84-ignore-%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95)

# gitignore 에 있는 파일 원격 저장소 에서 제거

```bash
git rm -r --cached .  
git add . 
git commit -am "Remove ignored files"
```

위 명령어들은 `.gitignore` 파일에 새롭게 추가된 항목들이 Git 저장소에서 무시되도록 설정하고, 이미 Git에 추적되던 파일들을 제거한 후, 그 변경 사항을 커밋하는 과정임. 각 명령어의 자세한 설명은 다음과 같음:

### 1. `git rm -r --cached .`
- **`git rm`**: Git에서 파일이나 디렉터리를 삭제할 때 사용되는 명령어임.
- **`-r` (recursive)**: 디렉터리와 그 안의 모든 파일을 재귀적으로 삭제하라는 의미임. 즉, 모든 하위 디렉터리와 파일들도 포함됨.
- **`--cached`**: 이 옵션은 실제 파일을 삭제하지 않고, Git의 인덱스(스테이징 영역)에서만 해당 파일을 삭제하겠다는 의미임. 즉, 파일들은 로컬 디스크에 그대로 남아 있고, Git이 더 이상 이 파일들을 추적하지 않게 됨.
- **`.` (dot)**: 현재 디렉터리와 그 하위 모든 파일과 디렉터리를 대상으로 함.

**결과**: 이 명령어는 현재 디렉터리와 그 하위 모든 파일 및 디렉터리를 Git의 인덱스에서 제거함으로써, 이후에 `.gitignore`에 추가된 항목들이 제대로 무시되도록 만듦.

### 2. `git add .`
- **`git add`**: 변경된 파일들을 Git의 인덱스에 추가하는 명령어임. 커밋하기 전에 Git이 어떤 변경 사항을 추적해야 하는지를 지정함.
- **`.` (dot)**: 현재 디렉터리와 그 하위 모든 파일과 디렉터리를 대상으로 함.

**결과**: 이 명령어는 현재 디렉터리와 그 하위 모든 파일들을 다시 Git의 인덱스에 추가함. 그러나 `.gitignore`에 의해 무시된 파일들은 인덱스에 포함되지 않음.

### 3. `git commit -am "Remove ignored files"`
- **`git commit`**: Git에 스냅샷을 저장하는 명령어로, 인덱스에 있는 모든 변경 사항을 로컬 저장소에 기록함.
- **`-a` (all)**: 추적되고 있는 모든 파일들에 대한 변경 사항을 자동으로 스테이징하여 커밋함. 단, 새로운 파일들은 포함되지 않음.
- **`-m` (message)**: 커밋 메시지를 인라인으로 제공할 수 있게 해줌.
- **`"Remove ignored files"`**: 이 커밋의 메시지로, 제거된 파일들에 대한 설명임.

**결과**: 이 명령어는 현재 인덱스에 있는 모든 파일들의 변경 사항을 커밋하고, 커밋 메시지로 "Remove ignored files"를 남김.

### 요약
이 세 가지 명령어는 다음과 같은 순서로 작동함:
1. `.gitignore`에 의해 무시될 파일들을 인덱스에서 제거함 (`git rm -r --cached .`).
2. 변경 사항들을 인덱스에 다시 추가함 (`git add .`).
3. 제거된 파일들에 대한 변경 사항을 커밋함 (`git commit -am "Remove ignored files"`).

이를 통해 Git이 더 이상 무시해야 할 파일들을 추적하지 않도록 설정하고, 그 결과를 저장소에 반영하게 됨.