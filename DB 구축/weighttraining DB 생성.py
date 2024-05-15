import sqlite3
import pandas as pd

# SQLite 데이터베이스 연결
conn = sqlite3.connect('weighttraining.db')
cursor = conn.cursor()

# 기존 테이블 제거 (만약 존재하는 경우)
cursor.execute("DROP TABLE IF EXISTS exercises")

# 테이블 생성 (Exercise code를 기본 키로 설정)
cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (
               Exercise_code TEXT PRIMARY KEY,
               Exercise_name TEXT,
               Agonist TEXT,
               Synergist TEXT,
               Stabilizers TEXT,
               Mechanics TEXT,
               Force TEXT,
               Starting_position TEXT,
               Execution TEXT,
               Comments_and_tips TEXT,
               Image_url TEXT,
               Video_url TEXT
                )''')

# Excel 파일 읽기
xlsx_file = pd.ExcelFile('weighttraining.guide.en.ko(수정본) - 복사본.xlsx')
df = xlsx_file.parse(xlsx_file.sheet_names[0])
exercise_code = 1001

# 데이터베이스에 데이터 삽입 (중복된 값 무시)
for index, row in df.iterrows():
    cursor.execute("INSERT INTO exercises VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (str(exercise_code), row['운동명'], row['주동근'], row['협응근'], row['안정근'], row['역학'], row['힘의 방향'], row['시작 위치'],
                    row['실행'], row['의견 및 팁'], row['이미지_URL'], row['video_url']))
    exercise_code = exercise_code + 1

# 커밋
conn.commit()

# 삽입된 행의 개수 확인
cursor.execute("SELECT COUNT(*) FROM exercises")
row_count = cursor.fetchone()[0]
print(f"Inserted {row_count} rows.")

# 연결 닫기
conn.close()
