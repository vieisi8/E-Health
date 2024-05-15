from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import pandas as pd
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# API 키
client = OpenAI(api_key='')


# 프롬프트 엔지니어링
system_instruction1 = """ 

모든 질문에 대한 정보를 찾을때 무조건 DB에서 정보를 찾을수 있게 sql문으로 만들어서 sql문을 반환
/ ```sql ~~ ''' 이런형식 금지 -> SELECT로 시작

exercises 테이블
exercises 테이블 컬럼: Exercise_code, Exercise_name, Agonist, Synergist, Stabilizers, Mechanics, Force, MachineORfreeweight, Level, Starting_position, Execution, Comments_and_tips, Image_url, Video_url
(exercises 테이블 컬럼)Agonist에는 상완근, 상완 삼두근, 복직근, 척추 기립근, 대퇴사두근, 후면 삼각근, 상완 이두근, 대흉근, 둔근, 장요근, 전거근, 전면 삼각근, 측면 삼각근, 외복사근, 내복사근, 상완 요골근, 손목 신근, 손목 굴곡근, 소흉근, 극하근, 상부 승모근, 광배근, 대퇴이두근, 대원근, 중하부 승모근, 능형근, 비복근, 햄스트링, 가자미근, 회외근, 회내근, 흉쇄유돌근, 슬건근, 고관절 외전근,대퇴근막장근, 대내전근, 장내전근, 단내전근이 존재함
/
~~ 운동 추천해줘 => where절 'Agonist' like %~~% 사용, ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 'Exercise_name'만을 검색 
/
~~ 에 대해 자세히 알고싶어 =>  where절 'Exercise_name' like %~~% 사용, ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 Exercise_name, Agonist, Synergist, Stabilizers, Mechanics, Force, Starting_position, Execution, Comments_and_tips, Image_url, Video_url을 전부 검색
/
~~ 는(은) 어떻게 하는건데? => where절 'Exercise_name' like %~~% 사용, ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 Exercise_name, Starting_position, Execution, Comments_and_tips, Image_url, Video_url을 전부 검색
/
~~ 자세 알려줘 => where절 'Exercise_name' like %~~% 사용, ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 Exercise_name, Starting_position, Execution, Comments_and_tips, Image_url, Video_url을 전부 검색
/
~~ 머신 운동 알려줘 => where절 'Agonist' like %~~% 사용, MachineORfreeweight like %머신% 사용, ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 'Exercise_name'만을 검색 
/
~~ 프리웨이트 운동 알려줘 => where절 'Agonist' like %~~% 사용, MachineORfreeweight like %프리웨이트% 사용, ~~에 띄어쓰기도 적용 exercises 테이블 컬럼의 'Exercise_name'만을 검색 
/
초급자 ~~ 운동 추천해줘  => where절 'Agonist' like %~~% 사용, 'Level' like %초급자% 사용,  ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 'Exercise_name'만을 검색 
/
(가슴,어깨,팔,복근,등,하체,목)운동 추천해줘 => where절 'Agonist' like %~~% 사용, ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 'Exercise_name'만을 검색
(가슴,어깨,팔,복근,등,하체,목)운동 알려줘 => where절 'Agonist' like %~~% 사용, ~~에 띄어쓰기도 적용, exercises 테이블 컬럼의 'Exercise_name'만을 검색
/
다음은 가슴,어깨,팔,복근,등,하체,목이 나타내는 Agonist를 적어둔거야
가슴:대흉근, 상부 대흉근, 소흉근, 하부 대흉근
어깨:후면 삼각근, 극하근, 전면 삼각근, 측면 삼각근
팔:상완 이두근, 상완 삼두근, 장두, 상완근, 상완 요골근, 손목 굴곡근, 손목 신근, 회내근, 회외근
복근: 복직근, 내부 복사근, 외부 복사근, 내복사근, 외복사근, 
등:광배근, 대원근, 중하부 승모근, 능형근, 척추 기립근, 등 전체, 상부 승모근, 뒷면, 전거근
하체:대둔근, 장요근, 가자미근, 고관절 외전근, 대내전근, 장내전근, 단내전근, 대퇴근막장근, 중둔근, 소둔근, 대퇴 사두근, 비복근, 햄스트링, 슬건근
목: 흉쇄유돌근
이제부터 가슴,어깨,팔,복근,등,하체,목을 각 나타내는 Agonist로 인식해
/
삼두 => 상완 삼두근
복근 => 복직근
이두 => 상완 이두근
엉덩이 => 둔근
종아리 => 비복근으로 인식
/
초보자는 초급자로 인식
""" 
system1 = {"role": "system", "content": system_instruction1} 

sql_translator=[]
sql_translator.append(system1)

# 질문을 프롬프트에 추가하는 함수
def ask(text):
    question = {"role": "user", "content": text} 
    sql_translator.append(question)

# 답변을 프롬프트에 추가하는 함수
def reply(text):
    answer = {"role": "assistant", "content": text} 
    sql_translator.append(answer)

# GPT 사용 함수
def GPT(messages,max_tokens):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=1,
    max_tokens=max_tokens,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content


# 프롬프트 엔지니어링
system_instruction2='''

너는 정보를 분석해 웨이트 운동 관련 질문이면 exercise 아니면 else를 반환
/ weighttrianing name=
'원 암 크로스 덤벨 트라이셉 익스텐션
씰 푸쉬업
크로스 푸쉬업
시티드 바벨 오버헤드 트라이셉스 익스텐션
디클라인 플랭크
스트레이트 바 시티드 로우
체스트 서포트 T바로우
스태빌리티 볼 백 익스텐션
피스톨 박스 스쿼트
인버티드 리어 델트 로우
스탠딩 덤벨컬
리버스 그립 덤벨 벤치 프레스
스탠딩 오버헤드 바벨 트라이셉스 익스텐션
스탠딩 덤벨 오버헤드 트라이셉스 익스텐션
덤벨 오버헤드 캐리
프론트 킥에서 리어 런지
크로스 덤벨 트라이셉 익스텐션
시티드 넥 익스텐션
인클라인 덤벨 숄더 레이즈
인클라인 덤벨 프론트 레이즈
하이 프론트 플랭크 암 레이즈
벤치 바벨 롤아웃
하이 원 레그 사이드 플랭크
하이사이드 플랭크
개구리 펌프
트라이셉스 바 해머 컬
아이언 크로스 플랭크
밴드 숄더 프레스
원암 덤벨 리버스 컬
어시스트 풀업 트라이셉스 딥스
스탠딩 하이 로우 케이블 플라이
EZ 바 와이드 그립 업라이트 로우
케틀벨 래터럴 레이즈
크런치 레그 레이즈
덤벨 스팰 캐스터
플로어 T-레이즈
하이 프론트 플랭크
덤벨 스쿼트 to 덤벨 컬
덤벨 사이드 런지
손목 롤러
무릎을 꿇고 플랭크
엑스트라 디클라인 윗몸일으키기
스태빌리티 덤벨 러시안 트위스트
덤벨 머신 시시 스쿼트
리어 런지
인벌티드 리어 델트 로우
스카퓰라 딥스
벤치에서 90도 크런치
덤벨 익스터널 숄더 로테이션
덤벨 해머 컬 to 덤벨 리버스 컬
물구나무서기
밴드 프론트 레이즈
롱 암 크런치
바벨 프런트 스쿼트 오버헤드 프레스
스탠딩 원암 오버헤드 덤벨 트라이셉스 익스텐션
데드버그(팔 움직임 없음)
풀다운 바 케이블 슈러그
인클라인 EZ 바 삼두근 익스텐션
원 암 레이즈 푸쉬업
덤벨 컬
시티드 올터네이팅 니 턱
원 레그 V업
저쳐캐리
하이트 덤벨 플라이
클로즈 뉴트럴 그립 풀업
플랫 벤치 프로그 리버스 하이퍼익스텐션
시터드 크로스 시저 킥
라잉 올터네이팅 덤벨 트라이셉스 익스텐션
더블 덤벨 풀오버
얼터네이팅 밴드 바이셉스 컬
스탠딩 바벨 컨센트레이션 컬
스탠딩 와이드 그립 바벨 오버헤드 프레스
덤벨 리스트 컬 오버 벤치
벤치 오버 덤벨 리버스 리스트 컬
덤벨 원암 업라이트 로우
스태빌리티 볼 위의 덤벨 컨센트레이션 컬
디클라인 푸시업 어겐스트 월
디클라인 벤치 리버스 하이퍼익스텐션
로우먼 체어 싯 업 플랫 벤치
로우먼 체어 싯 업
스테빌리티 볼 라잉 원 암 덤벨 트라이셉스 익스텐션
스테빌리티 볼 프론트 플랭크
인클라인 덤벨 컬
스태빌리티 볼 오버 인클라인 덤벨 플라이
케틀벨 데드리프트
벤트 니 인버티드 쉬러그 페럴렐 바아즈
플랫 벤치 리버스 하이퍼 익스텐션
니즈 클로우즈 그립 푸쉬업
서스펜데드 파이크
스탠딩 덤벨 킥백
덤벨 고블릿 스플릿 스쿼트
덤벨 프론트 스쿼트
더블 케틀벨 프론트 스쿼트
덤벨 데퍼셋 푸쉬업
디클라인 니 푸쉬업
스태빌리티 볼 오버 인클라인 원암 덤벨 플라이
인클라인 원암 덤벨 플라이
스태빌리티 볼 인클라인 원암 덤벨 프레스
클로우스 그립 디클라인 스태빌리티 볼 푸시업
서스펜더드 잭나이프
스탠딩 얼터네이팅 덤벨 킥백
인클라인 원암 덤벨 벤치 프레스
어시스터드 풀 업
원 레그 힙 쓰러스트
메디신볼 크런치
덤벨 스모 스쿼트(버전 2)
L-싯 풀업
믹스그립 풀업
플로어 L-싯
불가리안 스플릿 스쿼트
고릴라 친 크런치
인클라인 덤벨 해머 컬
시티드 투 암 오버헤드 덤벨 트라이셉스 익스텐션
덤벨 스퀴즈 벤치 프레스
스태빌리티 볼 오버 덤벨 프레스
시티드 얼터네이팅 덤벨 컬
시티드 바벨 벤트 니 굿 모닝
덤벨 스트레이트 레그 데드리프트
시티드 덤벨 원암 숄더 프레스
어시스트 딥스
덤벨 캐리어 캐리
스탠딩 양팔 덤벨 킥백
원 암 니 푸시업
덤벨 스플릿 스쿼트
잭나이프 윗몸일으키기
턱걸이
가슴 딥스
스태빌리티 볼 케이블 러시안 트위스트
바벨 오버헤드 슈러그
시티드 케이블 크로스암 트위스트
바벨 글루트 브릿지
스태빌리티 볼 백 익스텐션
벤치 위의 바벨 리버스 리스트 컬
캡틴 체어 스트레이트 레그 레이즈
머신 트라이셉스 딥스
언더그립 인버티드 로우
파이크 푸쉬업
하이 파이크 프레스
파이크 프레스
덤벨 레니게이드 로우
벤트 니 인버티드 리어 델트 로우
바벨 프론트 레이즈
바벨 언더그립 벤트오버 로우
바벨 비트윈 레그 스플릿 스쿼트
바벨 스플릿 스쿼트
계단 오르기
중량 전면 플랭크
케이블 Y-레이즈
핵 스쿼트
스태빌리티 볼 오버 덤벨 플라이
힙 쓰러스트
와이드 리버스 그립 바벨 벤치 프레스
덤벨 파머 워크
덤벨 오버헤드 스쿼트
핵 머신 원 레그 카프레이즈
핵머신 카프레이즈
덤벨 원 암 리버스 프리처 컬
원 암 데드행
맨몸 삼두근 익스텐션
스태빌리티 볼 오버 인클라인 덤벨 프레스
라잉 시저 킥
윗몸일으키기
행잉 레그 언드 힙 레이즈
바벨 오버헤드 런지
바벨 스모 루마니안 데드리프트
박스 오버 인클라인 푸쉬업
중량 풀업
바벨 벤트 니 굿 모닝
스텝 업
스미스 머신 와이드 그립 업라이트 로우
바벨 굿모닝
케이블 사이드 벤드
바벨 리어 델트 로우
바벨 드래그 컬
시티드 스미스 머신 비하인드 넥 숄더 프레스
시티드 덤벨 원 레그 카프레이즈
케이블 리버스 프리처 컬
사이드 푸쉬업
스미스 머신 스쿼트
라이딩 하이 케이블 컬
트랩 바 파머스 워크
트랩바 데드리프트
어시스트 랫 풀다운 인버스 레그 컬
인클라인 푸쉬업
케이블 리버스 리스트 컬
클로즈 그립 EZ 바 컬
머신 시티드 힙 어브덕션
라잉 덤벨 수퍼네이션
라잉 덤벨 프러네이션
원암 덤벨 프리처 컬
개구리 크런치
스미스 머신 슈러그
덤벨 박스 스쿼트
행잉 레그 레이즈
스미스 머신 JM 프레스
덤벨 와이드 그립 업라이트 로우
프론트 스미스 머신 카프레이즈
스미스 머신 예이츠 로우
머신 프론트 풀다운
디클라인 푸시업
덤벨 원암 래터럴 레이즈
시티드 바벨 리스트 컬
크런치 with 스터빌리티 볼 레그 레이즈
머신 프리처 컬
스미스 머신 인클라인 벤치 프레스
바벨 스텝업
중량 스터빌리티 볼 사이드 벤드
라잉 케이블 스컬 크러셔
사이드 라잉 리버스 덤벨 플라이
원암 리버스 덤벨 플라이
라잉 웨잇 넥 플렉션
런지
스탠딩 케이블 로우
바벨 JM 프레스
바벨 스컬 크러셔
인버스 레그 컬 온 랏 풀 다운 머신
프라그 크런치 레그 레이즈
디클라인 크런치
머신 트라이셉스 익스텐션
라잉 덤벨 래터럴 레이즈
케이블 다운-업 트위스트
바벨 프런트 박스 스쿼트
시티드 케이블 트위스트
덤벨 스콧 프레스
라잉 케이블 컬
비하인드 더 백 케이블 리스트 컬
슈퍼맨 푸쉬업
스미스 머신 숄더 프레스
벤트 니 오블리크 V-업
덤벨 w-프레스
EZ 바 리버스 프리처 컬
로프 랫 풀다운
맨몸 스쿼트
바벨 프리처 컬
프론트 인클라인 와이드 그립 업라이트 로우
디클라인 EZ 바 스컬 크러셔
원암 해머 그립 덤벨 벤치 프레스
수파인 덤벨 컬
라잉 리버스 덤벨 플라이
인버스 레그 컬
스태빌리티 볼 레그 컬
시터드 엘보우 인 올터네이팅 덤벨 오버헤드 프레스
원암 오버헤드 케이블 삼두근 익스텐션
인클라인 덤벨 플라이
인클라인 덤벨 트라이셉스 익스텐션
케이블 수직 Palof 프레스
케이블 수평 Palof 프레스
사이드 플랭크 힙 어브덕션
사이드 라잉 바이셉스 바디웨잇 컬
닐링 바디웨잇 트라이셉스 익스텐션
사이드 플랭크 힙 어브덕션
팔꿈치 리프트
바이셉스 레그 컬
원 암 타월 로우
라잉 싱글 스트레이트 레그 힙 익스텐션
스파이더맨 푸쉬업
스탠딩 트위스트 케이블 로우
로프 스탠딩 케이블 리어 델트 로우
덤벨 원암 리버스 리스트 컬
케이블 고관절 어브덕션
행잉 윈드쉴드 와이퍼
디클라인 윗몸일으키기
EZ 바 리버스 컬
닐링 벤치 딥스
스탠딩 트위스트 케이블 하이 로우
라잉 케이블 플라이
케이블 컬
라잉 바벨 삼두근 익스텐션
하이버드 개 플랭크
비하인드 더 백 스미스 머신 리스트 컬
어깨 탭 푸쉬업
스미스 머신 벤트 니 굿모닝
케이블 프리처 컬
더블 케이블 뉴트럴 그립 랫 풀다운
케이블 트위스트
디클라인 덤벨 벤치 프레스
어시스트 클로즈 뉴트럴 그립 풀업
인클라인 케이블 벤치 프레스
웨이트 스태빌리티 볼 크런치
어시스트 삼두근 딥스
점프 스쿼트
디클라인 바벨 풀오버
덤벨 리버스 컬
시티드 덤벨 오버헤드 트라이셉스 익스텐션
플랫 벤치 하이퍼 익스텐션
캡턴즈 체어 레그 레이즈
더블 케이블 프론트 레이즈
원 레그 푸쉬업
라잉 웨이트 레터럴 넥 플렉션
시티드 덤벨 프론트 레이즈
웨이트 원 레그 힙 쓰러스트
시티드 넥 비하인드 바벨 숄더 프레스
머신 싯 크런치
디클라인 덤벨 플라이
시티드 엘보우 인 덤벨 오버헤드 프레스
트위스트 크런치
벤트오버 바벨 리버스 레이즈
스트레이트 레그 케이블 풀스루
트위스트 힙 익스텐션
스미스 머신 언더핸드 예이츠 로우
스탠딩 덤벨 프리처 컬
스미스 머신 시티드 오버헤드 프레스
인클라인 케이블 트라이셉스 익스텐션
헤드 서포티드 리버스 덤벨 플라이
스트레이트 백 시트 언더핸드 케이블 로우
랜드마인 로우
디클라인 케이블 플라이
클로즈 그립 바벨 벤치 프레스
라잉 얼터네이팅 스트레이트 레그 레이즈
스탠딩 케이블 힙 익스텐션
다이아몬드 푸쉬업
트위스팅 케이블 오버헤드 프레스
시티드 트위스트 케이블 로우
원암 오버헤드 케이블 컬
머신 시티드 원 레그 카프레이즈
원암 랫 풀다운
인클라인 리버스 그립 덤벨 벤치 프레스
웨이트 캡턴즈 체어 레그 힙 레이즈
케이블 후면 드라이브
시티드 크로스 덤벨 프론트 레이즈
시티드 덤벨 리스트 컬
케이블 원 암 프론트 레이즈
원 레그 앞 플랭크
바벨 원 레그 힙 쓰러스트
니 푸시업
케이블 트라이셉스 킥백
덤벨 원 레그 스플릿 스쿼트
시티드 오버헤드 EZ 바 트라이셉스 익스텐션
케이블 힙 애브덕션
해머 그립 덤벨 벤치 프레스
스탠딩 덤벨 원 레그 카프레이즈
라잉 스트레이트 레그 레이즈
니 다이아몬드 푸쉬업
트위스팅 하이퍼릭스텐션
웨이트 인버티드 로우
케이블 우드 찹
디클라인 덤벨 삼두근 익스텐션
스미스 머신 닐링 리어 킥
중량 푸시업
덤벨 포어루어드 리닝 런지
원 레그 하이퍼릭스텐션
캡턴즈 체어 레그 언드 힙 레이즈
바벨 스모 스쿼트
스탠딩 케이블 체스트 프레스
바벨 힙 쓰러스트
스태빌리티 볼 잭나이프
바벨 사이드 런지
케이블 스트레이트 암 풀다운
비하인드 더 백 바벨 리스트 컬
케이블 와이드 그립 업라이트 로우
바벨 스트레이트 백 스티프 레그 데드리프트
스탠딩 AB 휠 롤아웃
맨몸 플라이
인클라인 덤벨 프론트 레이즈
케틀벨 스윙
닐링 ​​케이블 힙 익스텐션
벤트 오버 원 암 케이블 풀
덤벨 리버스 프리처컬 컬
디클라인 벤트 암 바벨 풀오버
프론트 인클라인 바벨 컬
언더핸드 예이츠 로우
맨몸 스모 스쿼트
덤벨 스모 스쿼트
덤벨 사이드 벤드
덤벨 리어 런지
아이소메트릭 와이퍼
스트레이트 백 시트 케이블 로우
바벨 스모 데드리프트
바벨 불가리안 스플릿 스쿼트
케이블 프론트 레이즈
바벨 닐링 스쿼트
스태빌리티 볼 푸쉬업
인클라인 덤벨 컬
미디엄 그립 랫 풀다운
기계 보조 풀업
덤벨 해머 프리처 컬
바벨 롤아웃
덤벨 레그 컬
케이블 원암 리버스 그립 삼두근 푸시다운
벤트오버 투 암 덤벨 로우
웨이트 시시 스쿼트
스미스 머신 체어 스쿼트
라잉 원암 리버스 덤벨 플라이
머신 백 익스텐션
머신 원암 로우
디클라인 해머 그립 덤벨 벤치 프레스
스태빌리티 볼 사이드 벤드
원암 벤치 딥스
라잉 벤트 니 어블릭 트위스트
제퍼슨 스쿼트
디클라인 바벨 스컬 크러셔
그립리스 슈러그
시터드 벤트 오버 투 암 덤벨 킥백
플레이트 프론트 레이즈
머신 레그 레이즈 크런치
행잉 스트레이트 레그 언드 힙 레이즈
바벨 랙 풀
스태빌리티 볼 레그 익스텐션 크런치
스태빌리티 볼 디클라인 푸쉬업
테이트프레스
닐링 레그 컬
스벤드 프레스
케이블 스쿼트
머신 하이 로우
시티드 덤벨 래터럴 레이즈
슬레드 카프레이즈
케이블 칸선트레이션 트라이셉스 익스텐션
덤벨 스쿼트
머신 체스트 프레스
시티드 바벨 트위스트
시티드 리버스 덤벨 플라이
머신 플라이
수파인 케이블 리버스 플라이
바벨 스미스 스쿼트
클로즈 그립 푸쉬업
오버헤드 케이블 컬
덤벨 불가리안 스플릿 스쿼트
웨이트 플레이트 리버스 컬
머신 리버스 하이퍼익스텐션
라잉 원암 덤벨 삼두근 익스텐션
덤벨 플라이
수직 다리 크런치
웨이트 러시안 트위스트
덤벨 스텝업
바이시클 크런치
인클라인 덤벨 벤치 프레스
인클라인 스트레이트 암 풀다운
비하인드 넥 랫 풀다운
인버티드 로우
슈퍼맨
저처 스쿼트
클로즈 뉴트럴 그립 풀업
V-업
케이블 벤치 프레스
인클라인 바벨 벤치프레스
시티드 레그 레이즈
싱글 레그 글룻 브리지
덤벨 리버스 그립 컨센트레이션 컬
케이블 리어 델트 로우
하이 리버스 플랭크
덤벨 해머 컬
덤벨 쿠바 로테이션
케이블 원 암 사이드 레터럴레이즈
디클라인 트위스트
시티드 원암 케이블 로우
크로스 덤벨 프론트 레이즈
덤벨 암핏 로우
덤벨 데드리프트
디클라인 바벨 벤치 프레스
스탠딩 케이블 플라이
라잉 올터네이팅 니 레이즈
케이블 풀스루
행잉 레그 힙 레이즈
덤벨 라잉 익스터널 숄더 로우테이션
라잉 사이드 힙 레이즈
라잉 레그 힙 레이즈
케이블 페이스 풀
인클라인 리버스 그립 바벨 벤치 프레스
인클라인 케이블 플라이
닐링 ​​케이블 크런치
바벨 루마니안 데드리프트
덤벨 원암 숄더 프레스
벤트오버 바벨 로우
벤치 딥스
EZ 바 컬
풀업
덤벨 런지
시티드 바벨 숄더 프레스
프론트 플랭크
바벨 런지
리버스 그립 랫 풀다운
바벨 프론트 스쿼트
덤벨 크로스 바디 해머 컬
케이블 익스터널 숄더 로우테이션
원암 덤벨 프리처 컬
시티드 레그 컬
머신 스탠딩 카프 레이즈
푸쉬 업
클로즈 뉴트럴 그립 랫 풀다운
라잉 레그 컬
덤벨 슈러그
와이드 그립 케이블 로우
오버헤드 바벨 삼두근 익스텐션
바벨 리버스 컬
바벨 숄더 프레스
하이퍼익스텐션
아놀드 프레스
머신 시티드 카프 레이즈
벤트오버 덤벨 로우
바벨 스쿼트
T바 로우
휠 롤아웃
덤벨 풀오버
행잉 스트레이트 레그 힙 레이즈
바벨 와이드 그립 업라이트 로우
로프 트라이셉스 푸시다운
덤벨 컬
시티드 케이블 로우
와이드 그립 랫 풀다운
스탠딩 인클라인 케이블 플라이
스탠딩 케이블 플라이
덤벨 벤치 프레스
바벨 벤치 프레스
바벨 슈러그
리버스 덤벨 플라이
레그 익스텐션
덤벨 리베이트
리버스 크런치
인클라인 스트레이트 레그 힙 레이즈
트라이셉스 딥스
인클라인 레그 프레스
바벨 데드리프트
덤벨 래터럴 레이즈
시티드 덤벨 오버헤드 프레스
바벨 컬
덤벨 컨센트레이션 컬
크런치'
/ 질문 ''weighttraining name'에 대해 자세히 알고싶어'는 웨이트 운동 관련 질문이므로 exercise를 반환
/ 질문 '~~ 운동 추천해줘'는 웨이트 운동 관련 질문이므로 exercise를 반환
/ 정보를 분석할때 웨이트 운동 관련 질문과 웨이트 운동 관련되지 않은 질문이 한문장에 둘다 존재하는 경우에도 else를 반환
/ 질문 ''weighttraining name'과(와) ~~ 을(를)알고싶어(알려줘)'도 웨이트 운동 관련 질문과 웨이트 운동 관련되지 않은 질문이 한문장에 둘다 존재하는 경우이므로 else를 반환
/ 질문 '웨이트 트레이닝 전문가 사이트를 추천해줘'는 웨이트 운동 관련 질문이 아니므로 else를 반환
/ 반환값은 exercise, else만 가능 '''

system2={"role": "system", "content": system_instruction2}

tag_appraiser=[]
tag_appraiser.append(system2)


# 프롬프트 엔지니어링
system_instruction3='''

너는 운동 정보를 받아서 질문에 맞는 답변을 만드는 시스템이야.
/ 답변을 생성할때 받은 운동 정보가 수십개일때 '~~ 등 다양한 종류의 운동이 있어'처럼 운동 정보를 생략하지말고 '1. ~~ 2. ~~' 이런식으로 숫자를 붙여 받은 운동 정보 수십개를 전부다 포함해서 답변을 생성해
/ 아무리 많아도 운동 정보 생락하지 말라니까!!!!! 1000개 운동 정보가 있으면 1000개 전부다 포함해
/ 받은 정보외에는 절대 다른 정보를 가져오면 안 돼!
/ 받은 정보가 아무것도 없으면 없다고 해!
/ 친근한 말투(존댓말)로 답변 생성해
/ 답변을 생성할때 줄 바꿈을 무조건 해줘 그래야 정돈된 느낌의 답변이 완성돼!'''

system3={"role": "system", "content": system_instruction3}

write=[]
write.append(system3)


# 예상 질문 (딕셔너리 자료형)
Expected_QandA={'스트레칭 방법 알려줘':'''현재 스트레칭에 관한 DB는 없습니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '웨이트 트레이닝 전문가가 누구야?':'''하니 램보드가 아닐까 조심스럽게 생각해 봅니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '웨이트 트레이닝 전문 사이트 추천해줘':'''저는 저를 추천하고 싶습니다! ⁀⊙﹏☉⁀
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '최적의 유산소 운동은 무엇인가요?':'''사람의 몸상태에 따라 달라질 수 있습니다.
무릎이 건강하신 분들은 계단 오르기,달리기,줄넘기,걷기 등이 있습니다. 
무릎이 건강하지 못하신 분들은 무릎에 부담이 덜하는 수영과 자전거를 추천합니다. 
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '근력 훈련의 중요성은 무엇인가요?':'''근력향상을 시켜 일상생활에 필요한 활동을 수행하는데 도움을 두고 운동 성능을 향상시킵니다. 
그리고 근육과 인대를 강화 시켜 부상예방에 도움을 줍니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                   '스트레칭의 이점은 무엇인가요?':'''스트레칭은 근육과 인대를 늘이고 유연성을 향상시키고 유연한 근육과 인대는 일상 생활에서의 움직임을 향상시키고, 운동 및 활동 중 발생할 수 있는 부상의 위험을 줄여줍니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '건강한 식습관과 운동의 관련성은 어떤가요?':'''건강한 식습관과 꾸준한 운동은 혈당 조절, 혈압 관리 및 콜레스테롤 수준 유지에 도움이 됩니다. 이는 대사 질환 예방과 심혈관 질환의 위험을 줄이는 데 도움이 됩니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '심혈관 운동의 종류와 이점은 무엇인가요?':'''유산소 운동, 근력운동, 고강도 간격운동 입니다.
이3개의 운동 종류는 심장 및 폐 기능에 도움을 주고 혈액 순환을 촉진하고 산소 공급을 개선 합니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '운동 전후에 스트레칭을 해야 하는 이유는 무엇인가요?':'''운동 전 스트레칭은 운동으로 인한 부상의 위험을 줄여주는데 도움을 주고
운동 후 스트레칭은 긴장된 근육을 이완 시켜 빠르고 효과적인 회복을 돕습니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                   '정기적인 운동이 심리적 안녕에 미치는 영향은 무엇인가요?':'''운동은 몸에 대한 자아 존중감을 향상시키고 자신감을 증진시킵니다. 몸을 움직이고 성취감을 느끼는 것은 자아 존중감을 높이는데 중요한 역할이 될 수 있습니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '체지방률을 감소시키기 위한 효과적인 운동은 어떤 것이 있나요?':'''운동은 몸에 대한 자아 존중감을 향상시키고 자신감을 증진시킵니다. 몸을 움직이고 성취감을 느끼는 것은 자아 존중감을 높이는데 중요한 역할이 될 수 있습니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                    '운동을 시작하는 사람들에게 권장되는 조언은 무엇인가요?':'''명확한 목표를 설정하고 그에 맞는 계획을 세우는 것이 중요합니다. 목표는 현실적이고 구체적이며 달성 가능한 것이어야 합니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!''',
                   '다양한 연령대에게 적합한 운동 방법은 무엇인가요?':'''어린이(7세 이하): 놀이를 통한 활동을 통해 뛰기, 뛰어넘기 공놀이를 통해 활동성을 늘립니다.
청소년(8세~19세): 구기 스포츠와 같은 활동성이 강한 운동으로 심폐 지구력 을 늘리고 가벼운 저항운동으로 성장가능성을 늘립니다.
성인: 유산소 운동: 걷기,조깅,수영,자전거 타기 등으로 체지방 조절 
근력운동: 근력을 키워 몸의 밸런스 와 신체 건강 조절
노인: 부상의 위험성을 최대로 낮춰
걷기, 스트레칭, 수영을 통해 관절의 부담과 근육 강화를 시킬 수 있습니다.
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다.'''}

# 예상 질문만 추출
Expected_Question = list(Expected_QandA.keys())

# 질문이 예상 질문이 존재 하는지 확인 하는 함수
def Check_Expected_Question(input_value, array):
    for item in array:
        if item in input_value:
            return True
    return False


# 프롬프트 엔지니어링
system_instruction4=f'''
너는 질문이 {Expected_Question}와 뉘앙스가 비슷한지 아닌지 판단해서 맞으면 T 아니면 F를 반환해
/ 질문이 웨이트 관련된 질문 일때도 T를 반환해
/ '심혈관 운동의 종류와 이점은 무엇인가요?'는 T 반환
/ '정기적인 운동이 심리적 안녕에 미치는 영향은 무엇인가요?'는 T 반환
/ 반환값은 T, F만 가능'''

system4={"role": "system", "content": system_instruction4}

else_write=[]
else_write.append(system4)

# 모두 초기화 하는 함수
def reset():
    sql_translator.clear()
    tag_appraiser.clear()
    write.clear()
    else_write.clear()

    sql_translator.append(system1)
    tag_appraiser.append(system2)
    write.append(system3)
    else_write. append(system4)

# 답변 도출 과정 저장
Process=[]
# 에러 저장
Error=[]

@app.route('/', methods=['POST'])
def get_data():
    # SQLite 연결
    conn = sqlite3.connect("weighttraining.db")
    cursor = conn.cursor()
    
    process=[]
    error=[]
    error_causes=[]

    # 전달된 JSON 데이터 받기
    data = request.get_json()
    question=data.get('Question')

    # 초기화 진행
    reset()

    process.append(question)
    
    # 태그 감별하기
    tag_appraiser.append({"role": "user", "content": question})
    tag = GPT(tag_appraiser,8)

    process.append(tag)

    # 태그가 운동일 경우
    if(tag=='exercise'):
        
        # 프롬프트에 질문 추가
        ask(question) 

        # GPT 호출
        translated_sql = GPT(sql_translator,256)

        # 프롬프트에 답변 추가
        reply(translated_sql)

        process.append(translated_sql)
        
        try:

            # 전달된 SQL 실행
            cursor.execute(translated_sql)

            # 쿼리 결과 가져오기
            query_result = cursor.fetchall()

            # 결과 저장
            conn.commit()

            # SQLite 연결 종료
            conn.close()

            # 결과를 Pandas DataFrame으로 변환
            columns = [description[0] for description in cursor.description]
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            df = pd.DataFrame(query_result, columns=columns)
            process.append(str(df))

            # Image_url, Video_url 컬럼만 선택하여 새로운 DataFrame 생성
            try:
                url_df = df[['Image_url', 'Video_url']]
            except KeyError as e:
                # KeyError가 발생했을 때, 빈 문자열로 채운 DataFrame 생성
                url_df = pd.DataFrame(columns=['Image_url', 'Video_url'])

            # Image_url, Video_url 컬럼 삭제한 DataFrame 생성
            try:
                df = df.drop(['Image_url', 'Video_url'], axis=1)
            except KeyError as e:
                pass

            Image_url = []
            Video_url = []

            if not url_df.empty:
                for index, row in url_df.iterrows():
                    # 이미지, 동영상 주소 값들 추가
                    Image_url.append(row['Image_url'])
                    Video_url.append(row['Video_url'])
            else:
                Image_url = None
                Video_url = None
            
            # 질문과 쿼리 결과 프롬프트에 추가
            write.append({"role": "user", "content": question})
            write.append({"role": "user", "content": df.to_string(index=False)})

            # GPT 호출
            answer = GPT(write,4096)
            
            # 답변 프롬프트에 추가
            write.append({"role": "assistant", "content": answer})

            process.append(answer)

            # JSON 응답 생성
            response = {
                'Answer': answer,
                'Image_url':Image_url,
                'Video_url':Video_url
            }
            
        except Exception as e:
            # 에러 발생시 프롬프트에 추가된 정보 삭제
            for i in range(2):
                sql_translator.pop()
            
            error_causes.append(f'{e}')
            answer=f'''정보를 찾을 수 없습니다.
다시 한번 질문 부탁드려요!'''
            process.append(answer)
            error.append(answer)
            error.append(error_causes)
            Error.append(error)

            response = {
                'Answer': answer,
                'Image_url':None,
                'Video_url':None
            }
            
        finally:
            Process.append(process)

        return jsonify(response)
    
    # 태그가 그 외 일경우
    else:

        #질문 프롬프트에 추가
        else_write.append({"role": "user", "content": question})

        # 질문이 웨이트 트레이닝 관련한 질문인지 판단
        TorF = GPT(else_write,8)
        
        # 웨이트 트레이닝 관련한 질문이 맞다면
        if(TorF=='T'):

            # 예상 질문에 있는지 확인
            result = Check_Expected_Question(question, Expected_Question)

            # 예상 질문에 존재 할 경우
            if(result==True):
                
                #예상 답변 추출
                if question in Expected_QandA:
                    corresponding_answer = Expected_QandA[question]
                answer=corresponding_answer

                process.append(answer)
                Process.append(process)

                response = {
                    'Answer': answer,
                    'Image_url':None,
                    'Video_url':None
                    }
                
                return jsonify(response)
            
            # 예상 질문에 존재 하지 않을 경우
            else:
                answer='''아직 데이터가 존재 하지 않습니다ㅠ
추후 업데이트를 통해 고품질의 대답을 드릴 수 있도록 노력 하겠습니다!'''

                process.append(answer)
                Process.append(process)

                response = {
                    'Answer': answer,
                    'Image_url':None,
                    'Video_url':None
                    }
                
                return jsonify(response)
            
        # 웨이트 트레이닝 관련 질문이 아닐경우
        else:
            answer='''저는 웨이트 관련된 질문 외에는 답변해드릴 수 없어요ㅜ
다른 질문을 해보시겠어요?'''

            process.append(answer)
            Process.append(process)

            response = {
                'Answer': answer,
                'Image_url':None,
                'Video_url':None
                }
            
            return jsonify(response)

@app.route('/read_date')
def get_exercise_names():
    # SQLite 연결
    conn = sqlite3.connect("weighttraining.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Exercise_name FROM exercises")
    exercise_names = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT Agonist FROM exercises")
    exercise_types = [row[0] for row in cursor.fetchall()]
    
    response = {
                'exercise_names': exercise_names,
                'exercise_types': exercise_types
                }
    return jsonify(response)

@app.route('/admin/process')
def get_process():
    response = {
        'Process': Process,
        'Error': None
        }
    return jsonify(response)


@app.route('/admin/error')
def get_ErrorAndPrompt():
    response = {
        'Process': None,
        'Error': Error
        }
    return jsonify(response)

if __name__ == "__main__":
    app.run()
