# AI-Smart-Route-Optimizer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangGraph-Orchestration-orange?logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/LLM-Solar--Pro-green?logo=openai&logoColor=white)

**사용자의 고정 일정(Fixed Events)과 할 일(To-do List)을 입력받아, 최적의 장소를 검색·선정하고 이동 효율을 고려한 최종 스케줄링 경로를 제안하는 AI 에이전트.**

<br>

## 📌 주요 기능 (Key Features)

* **자연어 의도 분석**: "분위기 좋은 카페 가기" 같은 추상적인 할 일을 검색 가능한 키워드로 변환합니다.
* **실시간 장소 탐색**: 네이버 지도 크롤링(Playwright)을 통해 실제 영업 중인 최적의 장소 후보를 수집합니다.
* **지능형 장소 선정**: 사용자의 현재 위치와 동선을 고려하여 LLM이 최적의 장소를 최종 선택합니다.
* **동선 최적화**: 카카오맵 API를 활용한 거리 계산 및 논리적 추론을 통해 이동 거리를 최소화하는 스케줄을 확정합니다.

<br>

## 🏗️ 시스템 구조 (Architecture)

이 프로젝트는 **LangGraph**를 사용하여 상태 기반(Stateful) 워크플로우로 동작합니다.

1.  **Ingest Node**: 사용자 입력 데이터 전처리 및 좌표 변환
2.  **Candidate Node**: 할 일(Todo) 분석 및 네이버 지도 크롤링
3.  **Selection Node**: 후보지 중 최적의 장소 확정 (LLM)
4.  **Distance Node**: 모든 지점 간 거리 행렬(Distance Matrix) 계산
5.  **Optimization Node**: 전체 동선 효율성 분석 및 최종 스케줄 생성

<br>

## 🚀 시작 가이드 (Getting Started)

### 1. 설치 (Installation)

**가상환경 생성 (권장)**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**의존성 설치**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**Playwright 브라우저 설치 (크롤링용 필수)**
```bash
playwright install
```

### 2. 환경 변수 설정 (.env)
프로젝트 루트에 .env 파일을 생성하고 API Key를 입력하세요.
```Ini, TOML
# [필수] Upstage (Solar) API Key
UPSTAGE_API_KEY=up_sk_xxxxxxxxxxxxxxxxxxxxxxxx  <-- 실제 키 입력

# [필수] Kakao Map REST API Key
KAKAO_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  <-- 실제 키 입력

# [선택] LangSmith (디버깅용, 없으면 false로 변경)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=smart-route-optimizer
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_xxxxxxxxxxxxxxxxxxxxxx   <-- 실제 키 입력
```

### 3. 실행 (Run Server)
```bash
uvicorn server:app --reload
```
서버 실행 후 http://localhost:8000/playground 에 접속하여 테스트할 수 있습니다.

<br>

## 🧩 Playground 입력 가이드 (Input Guide)
LangServe Playground에서 테스트할 때, 각 필드에 아래와 같은 JSON 데이터를 넣어주세요.

<img width="1051" height="863" alt="image" src="https://github.com/user-attachments/assets/254f66f0-ff33-402b-b55c-b785a23798de" />
<img width="942" height="590" alt="image" src="https://github.com/user-attachments/assets/1c708fe4-c218-442d-be79-4b9c5b9bd8d9" />

