# E-Health
![E-Health 메인 화면](https://github.com/vieisi8/E-Health/assets/146730344/b1ded5be-779d-4205-a93c-d979e492b6a9)
캡스톤디자인에서 진행 한 졸업 작품<br>
본 프로젝트는 <strong>웨이트 초보자가 더욱 쉽고 직관적인 운동 데이터를 통해 부상을 미리 방지하자는 취지</strong>가 담겨 있음<br>
저를 포함한 4명이 팀을 꾸려 약 8개월가량 개발 진행 (23.09 ~ 24.04)<br>
[![image](https://github.com/vieisi8/E-Health/assets/146730344/f5ad5be3-1c4e-4231-aac6-429d8d91e0c3)](http://54.180.219.227:8080/) => 저희 사이트는 현재 비활성화 상태임을 알림.

## 프로젝트 배경
코로나로 인해 사람들의 비만율이 증가하게 됨. 그로 인해 많은 사람들이 다이어트를 목표로 헬스장을 방문하게 됨.<br>
하지만 웨이트 운동은 기본 지식 없이는 부상당하기 쉬운 운동이기에 저희가 그런 점을 보안하고자 본 프로젝트를 고안하게 됨.

## 프로젝트 목표
- 웨이트 초보자가 더욱 쉽고 직관적인 운동 데이터를 통해 부상을 미리 방지 하는 것

## 📚 기술 스택
- LLM & AI
  - GPT
  - Prompt Engineering
- Front-end
  - Html
  - CSS
  - JavaScript
- Back-end
  - Java
  - Pyton
  - Flask
  - REST API
  - Selenium
  - Sqlite3
- IDE
  - Spring Boot
  - Visual Studio Code

## 프로젝트 flowchart
![작동 원리](https://github.com/vieisi8/E-Health/assets/146730344/3e5d4e22-a2fa-4f52-87a1-5702cf45b595)

- 클라이언트 서버 와 Chat-bot 서버는 <strong>REST API</strong> 방식으로 통신.

## 프로젝트 기여
  - 팀장으로서 프로젝트를 이끄는 역할 수행
  - 저는 주로 <strong>클라이언트 Back-end</strong> 맡아 개발 진행.
  - 백업을 위해 <strong> 제가 맡지 않은 파트(Front-End, Chat-bot 서버)</strong> 도 단위 테스트가 가능한 수준의 <strong>프로토타입을 개발</strong> 진행.


## 주요 기능
- 부위별 다양한 웨이트 운동 제공
- 다양한 웨이트 운동에 대한 상세 설명
- 효율적인 트레이닝을 위한 팁 제공
- 직관적으로 이해 할 수 있는 이미지 및 동영상 제공

## DB 구축
[![New-Site-Logo-with-Ring-Updated](https://github.com/vieisi8/E-Health/assets/146730344/d22ecfda-cc87-47f1-a1f1-2390d049ecad)](https://weighttraining.guide/)
<br>
Python 패키지인 <strong>Selenium</strong>을 활용해 위 사이트에서 정보를 수집후 데이터 클리닝 작업을 통해 DB 구축를 진행함.

## 핵심 기술
본 프로젝트에서의 핵심 기술은 OPEN AI 사의 GPT를 프롬프트 엔지니어링 방법을 이용해 <strong>사용자의 질문을 DB에 접근할 수 있는 SQL 문으로 변환</strong>하는 기술임.<br>
즉, <strong>프롬프트 엔지니어링을 통해 LLM을 SQL 특화</strong> 했다고 볼 수 있음.

## E-Health 시연

  - 질문 ▶ 예상 질문 👌

https://github.com/user-attachments/assets/5addd5e6-7568-4a59-9d29-8b8a704fe69a

  - 질문 ▶ 예상 질문 ❌

https://github.com/user-attachments/assets/d37873a2-f5a7-4792-9b71-8cc93b9a01a0

  - 질문 ▶ 웨이트 관련 질문 ❌

https://github.com/user-attachments/assets/d9a1f962-b841-4cee-98d1-cd3e3bebd5cc

## 프로젝트 결과/성과
  - 웨이트 운동 이미지, 자세, 주의 사항, 동영상으로 초보자가 봐도 쉽게 이해 가능하도록 답변이 잘 나옴
    - 졸업 작품 전시회 당시 이런 피드백을 상당히 많이 받음

## 시사점 및 한계
  - 웨이트 운동 초보자들을 위한 맞춤형 솔루션을 성공적으로 구현했다는 점⁠
  - 건강과 안전이라는 사회적 니즈에 부합하는 서비스를 개발했다는 점⁠
  - 웨이트 운동 외적인 운동 관련질문에는 한계가 명확함

## 프로젝트를 통해 배운 점과 아쉬운 점이나 보완할 점
  - 프롬프트 엔지니어링 만으로도 원하는 답변 유형으로 수정 가능하다는 것을 알게 됨
  - DB를 SQL로 데이터 선택하는 방법 말고 RAG를 사용했으면 어땠을까 하는 아쉬움이 남음


# 프로젝트 관리

## 프로젝트 개발 방법론
스크럼

## 협업 및 진척 관리
WBS를 작성해 각 팀원의 할 일을 지정, 매주 회의를 통한 진척 관리 진행.

> [WBS](https://github.com/vieisi8/E-Health/blob/main/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B4%80%EB%A6%AC/WBS.xlsx) 자세한 내용은 파일 참조 바람.

## 품질 관리
종합 테스트 시나리오서를 작성해 품질 관리 진행.

> [종합 테스트 시나리오서](https://github.com/vieisi8/E-Health/blob/main/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B4%80%EB%A6%AC/%EC%A2%85%ED%95%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4.xlsx) 자세한 내용은 파일 참조 바람.
