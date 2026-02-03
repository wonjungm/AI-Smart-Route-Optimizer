'''
# server.py
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from dotenv import load_dotenv

# 기존 main.py에서 그래프 생성 함수 가져오기
from main import build_graph

# 1. 환경 변수 로드
load_dotenv()

# 2. FastAPI 앱 생성
app = FastAPI(
    title="Route Optimization Agent",
    version="1.0",
    description="LangGraph로 만든 경로 최적화 에이전트 API 서버"
)

# CORS 설정 (나중에 프론트엔드 연결 시 필요, 지금은 기본 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 그래프 빌드 (컴파일된 Runnable 가져오기)
# main.py의 build_graph 함수를 실행해 컴파일된 앱 객체를 받습니다.
graph = build_graph()

# 4. LangServe 라우트 추가
# path="/agent"로 설정하면 -> /agent/playground 경로가 생깁니다.
add_routes(
    app,
    graph,
    path="/agent",
)

if __name__ == "__main__":
    # 서버 실행 (localhost:8000)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
'''
# server.py

# 1. 환경 변수 로드 (가장 먼저!)
from dotenv import load_dotenv
load_dotenv()

# 2. 라이브러리 임포트
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from pydantic import BaseModel, Field  # <-- 추가됨
from typing import List, Dict, Any     # <-- 추가됨

# 3. main.py에서 그래프 가져오기
from main import build_graph

# ==============================================================================
# [핵심] Playground 입력창을 깔끔하게 만들기 위한 "입력 전용 모델" 정의
# ==============================================================================
class AgentInput(BaseModel):
    user_id: str = Field(..., description="사용자 ID (예: user_123)")
    target_date: str = Field(..., description="날짜 (예: 2026-01-01)")
    user_house_address: str = Field(..., description="집 주소")
    user_workplace_address: str = Field(..., description="직장/학교 주소")
    
    start_point: Dict[str, Any] = Field(
        ..., 
        description="출발지 정보", 
        examples=[{"name": "집", "address": "서울시 용산구 독서당로 111"}]
    )
    
    end_point: Dict[str, Any] = Field(
        ..., 
        description="도착지 정보", 
        examples=[{"name": "집", "address": "서울시 용산구 독서당로 111"}]
    )
    
    fixed_events: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="고정된 일정 (강의, 운동 등)"
    )
    
    todo_list_raw: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="할 일 목록 (Todo)"
    )

# ==============================================================================
# FastAPI 앱 설정
# ==============================================================================
app = FastAPI(
    title="Route Optimization Agent",
    version="1.0",
    description="LangGraph로 만든 경로 최적화 에이전트 API 서버"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 그래프 빌드
graph = build_graph()

# ==============================================================================
# [핵심] 라우트 추가 시 with_types(input_type=...) 적용
# ==============================================================================
# 이렇게 하면 Playground가 GraphState 전체가 아니라, AgentInput만 입력으로 보여줍니다.
runnable = graph.with_types(input_type=AgentInput)

add_routes(
    app,
    runnable,
    path="/agent",
)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)