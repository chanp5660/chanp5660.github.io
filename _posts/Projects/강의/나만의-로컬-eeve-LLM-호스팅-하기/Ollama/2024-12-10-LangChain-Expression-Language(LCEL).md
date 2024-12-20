---
title: LangChain Expression Language(LCEL)
create_date: 2024-12-10 19:12
tags:
- LLM
- LLM/Langchain
aliases: null
blog: true
mathjax: true
layout: post
toc:
  sidebar: left
---
연결 문서

[랭체인노트 - # 05. LangChain Expression Language(LCEL)](https://wikidocs.net/233344)



# LangChain Expression Language(LCEL)

AI 워크플로우를 효율적으로 구성하기 위해서는 데이터 흐름, 모델 호출, 그리고 결과 처리 단계를 체계적으로 관리할 수 있는 프레임워크가 필요합니다. **LangChain**은 이러한 요구를 충족시키는 강력한 솔루션이며, 그중 **LangChain Expression Language(LCEL)** 는 LangChain의 다양한 구성 요소(프롬프트 템플릿, 모델, 출력 파서)를 언어적 표현으로 연결해, 한층 더 직관적이고 유연한 방식으로 AI 작업을 오케스트레이션할 수 있게 해줍니다.

이번 글에서는 LCEL의 개념과 역할, `invoke` 메서드의 설계 철학, `input` 데이터 구조의 이유, 그리고 **출력 파서(Output Parser)** 의 필요성과 활용 방안을 다룹니다. 또한 간단한 예제를 넘어 다단계 체인과 다양한 파서 적용 사례까지 살펴보며 LCEL을 통한 실무적 활용 방안을 제시합니다.

---

## LCEL이란 무엇인가?

LCEL은 LangChain이 제공하는 추상화 레벨 중 하나로, 사용자에게 **프롬프트 템플릿**, **모델**, **출력 파서** 등을 언어적 표현으로 연결하는 파이프(`|`) 기반 문법을 제공합니다. 이를 통해 기존에 코드 상에서 명시적으로 데이터 흐름을 제어하던 작업을 보다 직관적이고 선언적인 방식으로 표현할 수 있습니다.

- **기존 LangChain 체인 구성**: 함수나 메서드 호출로 체인을 구성.
- **LCEL을 활용한 구성**: 파이프(`|`) 연산자를 사용한 언어적 표현으로 체인의 로직을 단순화하고, 읽기 좋은 "데이터 흐름 그래프"를 쉽게 구현.

LCEL은 이처럼 **프롬프트 → 모델 호출 → 출력 파서**의 일련의 과정을 유연하고 명확하게 연결함으로써 복잡한 AI 워크플로우를 효율적으로 관리하는 데 기여합니다.

---

## 프롬프트 템플릿(Prompt Template)

프롬프트 템플릿은 사용자가 제공하는 변수를 바탕으로 모델이 이해하기 쉬운 문자열(프롬프트)을 동적으로 생성합니다. 이를 통해 단순히 하나의 질문을 던지는 것이 아니라, 상황에 따라 다양한 변수를 삽입한 맞춤형 질의를 모델에게 전달할 수 있습니다.

```python
from langchain_core.prompts import PromptTemplate

template = "{country}의 수도는 어디인가요?"
prompt_template = PromptTemplate.from_template(template)

prompt = prompt_template.format(country="대한민국")
print(prompt)  # 출력: 대한민국의 수도는 어디인가요?
````

---

## 모델 호출과 `invoke` 메서드

LCEL의 체인 상에서 입력값을 전달하고 모델을 호출할 때는 `invoke` 메서드를 사용합니다. `invoke`는 **입력을 주고, 처리 과정을 시작한다**는 의미를 잘 함축하고 있으며, AWS Lambda나 Java Reflection 등 다양한 시스템에서 함수 호출의 의미로 널리 활용되는 표현입니다.

- `invoke`를 선택한 이유:
    - **직관성**: "호출하다", "시작하다"라는 의미로 프로세스 실행 의도를 명확히 표현.
    - **관용적 사용**: 다양한 기술 스택에서 이미 유사한 의미로 사용, 친숙함 제공.
    - **대안 단어 비교**: `call`이나 `run`은 지나치게 일반적이거나 의도가 애매할 수 있으나 `invoke`는 입력 전달 및 실행 개시를 더 명확히 드러냄.

아래 예제에서는 이미 만든 프롬프트를 모델에 직접 전달합니다.

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=2048, temperature=0.1)
response = model.invoke("대한민국의 수도는 어디인가요?")
print(response)  # 출력: "대한민국의 수도는 서울입니다."
```

---

## 체인 생성과 파이프 연산자(`|`)

LCEL에서는 프롬프트 템플릿, 모델, 출력 파서 등을 파이프(`|`) 연산자로 연결할 수 있습니다. 이는 마치 Unix 파이프와 유사하게 **데이터 흐름을 직관적으로 표현**하여, 각 단계의 역할을 명확히 볼 수 있도록 합니다.

```python
prompt = PromptTemplate.from_template("{topic}에 대해 설명해주세요.")
model = ChatOpenAI()

chain = prompt | model
response = chain.invoke({"topic": "인공지능 모델의 학습 원리"})
print(response)
```

위 예제에서는 `{topic}`에 "인공지능 모델의 학습 원리"라는 입력이 전달되고, 해당 프롬프트가 모델로 흐른 뒤 결과가 반환됩니다.

---

## `input`: 왜 `dict` 형태인가?

LangChain은 입력을 딕셔너리(`dict`) 형태로 받습니다. 이는 다음과 같은 장점을 제공합니다.

1. **다중 변수 지원**: 여러 변수를 명확히 관리할 수 있습니다.
    
    ```python
    input = {"name": "홍길동", "topic": "파이썬"}
    ```
    
2. **가독성과 명확성**: 키-값 쌍으로 의미를 명확히 전달할 수 있습니다.
    
    ```python
    # 명확하지 않은 리스트
    input = ["홍길동", "파이썬"]
    
    # 명확한 딕셔너리
    input = {"name": "홍길동", "topic": "파이썬"}
    ```
    
3. **확장성**: 필요 시 쉽게 변수 추가 가능.
    
    ```python
    input = {"name": "홍길동", "topic": "파이썬", "urgency": "높음"}
    ```
    
4. **프롬프트 템플릿 연동**: `"{key}"` 형태로 템플릿에 매핑 가능.
    
    ```python
    prompt = PromptTemplate.from_template("{name}님, {topic}에 대해 설명해주세요.")
    formatted_prompt = prompt.format(**input)
    ```
    

---

## 출력 파서(Output Parser): 필요성과 활용

**출력 파서(Output Parser)** 는 모델의 응답을 특정 형식으로 변환하거나 구조화하는 역할을 합니다. 단순한 문자열 출력 이외에도 JSON, 딕셔너리, 리스트, CSV 등 다양한 형태로 가공할 수 있어, 후속 체인 처리나 다른 시스템과의 연동을 용이하게 합니다.

### 출력 파서의 역할

1. **출력 정리**: 모델 응답을 단순한 문자열 대신 정돈된 형태로 변환.
2. **구조화된 데이터 생성**: JSON, 딕셔너리 등 원하는 데이터 구조로 가공.
3. **후속 처리 준비**: 체인의 다음 단계에서 쉽게 활용할 수 있도록 출력 형식을 표준화.
4. **필수 사항은 아님**: 단순 텍스트 응답만 필요하다면 생략 가능. 하지만 복잡한 응답 처리가 필요한 경우 필수적.

### 다양한 출력 파서 예시

```python
from langchain_core.output_parsers import StrOutputParser, JSONOutputParser

# 단순 문자열 파서
str_parser = StrOutputParser()
parsed_str = str_parser.parse("이것은 AI 응답입니다.")
print(parsed_str)  # "이것은 AI 응답입니다."

# JSON 파서
json_parser = JSONOutputParser()
parsed_json = json_parser.parse('{"key": "value"}')
print(parsed_json)  # {'key': 'value'}
```

### 상황별 출력 파서 선택 가이드

- **단순 텍스트 활용**: `StrOutputParser` 사용.
- **정형 데이터 필요(후속 연산 필요)**: `JSONOutputParser` 또는 맞춤형 파서 활용.
- **커스텀 포맷 요구**: CSV나 특정 텍스트 포맷을 원하는 경우 커스텀 파서 구현 가능.

---

## 심화 예제: 다단계 체인과 다양한 파서 적용

다음 예제는 하나의 프롬프트로부터 시작하여, **여러 단계를 거치는 체인**을 보여줍니다.

1. 첫 번째 모델에서 사용자의 요청을 분석하고, **JSON 형식**으로 결과를 반환.
2. 두 번째 단계에서 JSON 응답을 파싱하고, 해당 데이터에 기반한 추가 프롬프트를 생성.
3. 최종적으로 다른 모델을 사용해 결과를 정리하고 문자열로 반환.

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JSONOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI

# 1단계: 사용자 요청 분석 및 JSON 응답
analysis_prompt = PromptTemplate.from_template("사용자의 요청: {request}\n이 요청을 'action'과 'object' 필드를 가진 JSON으로 분석하세요.")
analysis_model = ChatOpenAI()

# JSON으로 파싱하기 위한 파서
json_parser = JSONOutputParser()

analysis_chain = analysis_prompt | analysis_model | json_parser

analysis_result = analysis_chain.invoke({"request": "한국의 수도를 영어로 알려줘"})
# 예: {"action": "translate", "object": "서울"}

# 2단계: JSON 응답 기반 추가 질의
followup_prompt = PromptTemplate.from_template("action이 '{action}'이고 object가 '{object}'일 때, 결과를 한 문장으로 요약해주세요.")
followup_model = ChatOpenAI()

# JSON 출력에서 action, object를 추출하여 followup_prompt에 전달
followup_chain = followup_prompt | followup_model | StrOutputParser()

followup_response = followup_chain.invoke(analysis_result)
print(followup_response)
# 예: "서울은 영어로 Seoul이라고 합니다."
```

이 예제에서:

- 첫 번째 체인: 사용자의 요청을 분석한 뒤 JSON 형태로 결과를 반환하도록 구성.
- 두 번째 체인: JSON 파싱 결과(`analysis_result`)를 follow-up 프롬프트로 전달하고, 최종적으로 문자열로 응답.

이런 다단계 구성은 LCEL이 제공하는 문법(파이프 `|`)과 출력 파서를 활용해 복잡한 로직을 단순화하고, 각 단계를 재사용 가능하게 만드는 한 예시입니다.

---

## 결론

LangChain은 LCEL을 통해 프롬프트 템플릿, 모델, 출력 파서와 같은 구성 요소를 직관적으로 연결하고, 복잡한 AI 워크플로우를 효율적으로 관리할 수 있습니다.

- **`invoke` 메서드**: 입력 데이터 전달 및 프로세스 시작을 직관적으로 표현.
- **입력 형식(`dict`)**: 다중 변수 관리와 확장에 유리.
- **출력 파서**: 모델 응답을 구조화하고, 후속 작업에 적합한 형식으로 변환하는 핵심 도구.

LCEL은 이러한 장점을 통해, 코드의 가독성과 재사용성을 높이고 AI 파이프라인 구축을 손쉽게 해줍니다. 여러분의 프로젝트에 LCEL을 도입하여 더욱 강력하고 유연한 AI 워크플로우를 경험해보세요!