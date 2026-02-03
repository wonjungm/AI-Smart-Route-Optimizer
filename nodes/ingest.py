'''
from typing import Dict, Any, List
from state import GraphState
from utils import get_coordinates_kakao


# Node 1: 데이터 전처리 및 초기화 노드
def ingest_data_node(state: GraphState):
    # 💡 1. raw_input 정의
    raw_input = state 
    
    print("\n--- [NODE 1] 데이터 처리를 시작합니다 ---")

    # (1) Meta Data 처리 및 좌표 변환
    start_coords = get_coordinates_kakao(raw_input["start_point"]["address"])
    end_coords = get_coordinates_kakao(raw_input["end_point"]["address"])
    print(f"DEBUG: Start Coords = {start_coords}, End Coords = {end_coords}")

    meta = {
        "user_id": raw_input.get("user_id"),
        "target_date": raw_input.get("target_date"),
        "user_house_address": raw_input.get("user_house_address"),
        "user_workplace_address": raw_input.get("user_workplace_address"),
        "start_point": {
            **raw_input["start_point"],
            "coordinates": start_coords
        },
        "end_point": {
            **raw_input["end_point"],
            "coordinates": end_coords
        }
    }

    # (2) Fixed Schedules 처리
    # 수정: STATE에 있는 'fixed_events' 키를 직접 참조하거나 
    # main.py에서 보낸 'fixed_schedules'가 있다면 그것도 참조하도록 보강
    raw_fixed = raw_input.get("fixed_events") or raw_input.get("fixed_schedules") or []
    
    print(f"DEBUG [Ingest]: 원본 데이터에서 찾은 일정 개수 = {len(raw_fixed)}")

    fixed_events = []
    for idx, item in enumerate(raw_fixed, 1):
        loc = item.get("location", item.get("address", ""))
        print(f"고정 일정 좌표 변환 중: {loc}")
        coords = get_coordinates_kakao(item["location"])
        print(f"DEBUG: 고정일정[{item['title']}] 좌표 = {coords}")
        
        processed_item = {
            "id": f"fixed_{idx}",
            "type": "fixed",
            "title": item["title"],
            "location": item["location"],
            "coordinates": coords,
            "start_time": item["start_time"],
            "end_time": item["end_time"],
            "category": item["category"]
        }
        fixed_events.append(processed_item)

    # (3) Todo Items 처리
    todo_items = []
    # 💡 수정: todo_list_raw 키 참조
    for idx, item in enumerate(raw_input.get("todo_list_raw", []), 1):
        processed_item = {
            "id": f"todo_{idx}",
            "type": "todo",
            "title": item["task"],
            "duration": item["user_duration"],
            "center_place": item.get("center_place", ""),
            "search_words": item.get("search_words", []),
            "status": "need_recommendation",
            "candidates": [],
            "final_choice": None
        }
        todo_items.append(processed_item)

    print("--- [NODE 1] 데이터 처리 완료 ---")
    print(f"DEBUG [Ingest]: 최종 생성된 고정 일정 개수 = {len(fixed_events)}")
    
    return {
        "meta": meta,
        "fixed_events": fixed_events,
        "todo_items": todo_items,
    }
'''

from typing import Dict, Any, List
import json
from state import GraphState
from utils import get_coordinates_kakao

def unwrap_data(data):
    """
    Playground UI 이슈로 인해 [{'': [...]}] 형태로 감싸진 데이터를
    원래 리스트인 [...] 형태로 벗겨내는 함수
    """
    # 1. 리스트인데 요소가 1개이고, 그 요소가 딕셔너리이며, 키가 ''(빈문자열)인 경우
    if isinstance(data, list) and len(data) == 1:
        first_item = data[0]
        if isinstance(first_item, dict) and "" in first_item:
            print("DEBUG: 불필요한 껍데기(wrapper)를 감지하여 제거합니다.")
            return first_item[""]
    
    # 2. 문자열로 들어온 경우 (JSON 파싱 시도)
    if isinstance(data, str):
        try:
            return json.loads(data)
        except:
            pass
            
    return data

def ingest_data_node(state: GraphState):
    raw_input = state 
    print("\n--- [NODE 1] 데이터 처리를 시작합니다 ---")

    # ------------------------------------------------------------------
    # 1. Start / End Point 좌표 변환
    # ------------------------------------------------------------------
    start_addr = raw_input.get("start_point", {}).get("address", "")
    end_addr = raw_input.get("end_point", {}).get("address", "")

    start_coords = get_coordinates_kakao(start_addr)
    end_coords = get_coordinates_kakao(end_addr)
    
    meta = {
        "user_id": raw_input.get("user_id", "unknown"),
        "target_date": raw_input.get("target_date", ""),
        "user_house_address": raw_input.get("user_house_address", ""),
        "user_workplace_address": raw_input.get("user_workplace_address", ""),
        "start_point": {
            "name": raw_input.get("start_point", {}).get("name", "출발지"),
            "address": start_addr,
            "coordinates": start_coords
        },
        "end_point": {
            "name": raw_input.get("end_point", {}).get("name", "도착지"),
            "address": end_addr,
            "coordinates": end_coords
        }
    }

    # ------------------------------------------------------------------
    # 2. Fixed Events (고정 일정) 처리
    # ------------------------------------------------------------------
    # (1) 데이터 가져오기 및 껍질 벗기기
    raw_fixed = unwrap_data(raw_input.get("fixed_events", []))
    
    print(f"DEBUG [Ingest]: 원본 데이터 리스트(처리후) = {raw_fixed}")

    fixed_events = []
    # 데이터가 리스트가 아니면 빈 리스트로 취급
    if not isinstance(raw_fixed, list):
        raw_fixed = []

    for idx, item in enumerate(raw_fixed, 1):
        if not isinstance(item, dict): 
            continue
            
        # 1. 필수 데이터 확인
        if not item.get("title") and not item.get("location"):
            continue

        # 2. 좌표 변환
        loc = item.get("location", item.get("address", ""))
        if loc:
            coords = get_coordinates_kakao(loc)
        else:
            coords = {"x": "0", "y": "0"}

        processed_item = {
            "id": f"fixed_{idx}",
            "type": "fixed",
            "title": item.get("title", "일정 없음"),
            "location": loc,
            "coordinates": coords,
            "start_time": item.get("start_time", ""),
            "end_time": item.get("end_time", ""),
            "category": item.get("category", "etc")
        }
        fixed_events.append(processed_item)

    # ------------------------------------------------------------------
    # 3. Todo Items (할 일) 처리
    # ------------------------------------------------------------------
    # (1) 데이터 가져오기 및 껍질 벗기기
    raw_todos = unwrap_data(raw_input.get("todo_list_raw", []))
    print(f"DEBUG [Ingest]: 원본 할일 리스트(처리후) = {len(raw_todos)}개 발견")

    todo_items = []
    if not isinstance(raw_todos, list):
        raw_todos = []

    for idx, item in enumerate(raw_todos, 1):
        if not isinstance(item, dict):
            continue

        processed_item = {
            "id": f"todo_{idx}",
            "type": "todo",
            "title": item.get("task", "할 일 없음"),
            "duration": item.get("user_duration", 60),
            "center_place": item.get("center_place", ""),
            "search_words": item.get("search_words", []),
            "status": "need_recommendation", 
            "candidates": [],
            "final_choice": None
        }
        todo_items.append(processed_item)

    print(f"--- [NODE 1] 완료: Meta, Fixed({len(fixed_events)}), Todo({len(todo_items)}) 생성됨 ---")

    return {
        "meta": meta,
        "fixed_events": fixed_events,
        "todo_items": todo_items
    }