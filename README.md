# E-Health
![E-Health 메인 화면](https://github.com/vieisi8/E-Health/assets/146730344/b1ded5be-779d-4205-a93c-d979e492b6a9)
캡스톤디자인에서 진행 한 졸업 작품입니다.<br>
이 프로젝트는 <strong>웨이트 초보자가 더욱 쉽고 직관적인 운동 데이터를 통해 부상을 미리 방지하자는 취지</strong>입니다.<br>
저를 포함한 4명이 팀을 꾸려 약 8개월가량 진행하였습니다.(23.09 ~ 24.04)<br>
[![image](https://github.com/vieisi8/E-Health/assets/146730344/f5ad5be3-1c4e-4231-aac6-429d8d91e0c3)](https://54.180.219.227:8080) => 현재 사이트는 활성화 상태 입니다.

### 개발 배경
코로나로 인해 사람들의 비만율이 증가하게 되었습니다. 그로 인해 많은 사람들이 다이어트를 목표로 헬스장을 방문하게 됩니다.<br>
하지만 웨이트 운동은 기본 지식 없이는 부상당하기 쉬운 운동이기에 저희가 그런 점을 보안하고자 이 프로젝트를 고안하게 되었습니다.

### 📚 기술 스택
- Front-end
  - Html
  - CSS
  - JavaScript
- Back-end
  - Java
  - Pyton
  - Sqlite3
- IDE
  - Spring Boot
  - Visual Studio Code

### 작동 원리
![작동 원리](https://github.com/vieisi8/E-Health/assets/146730344/3e5d4e22-a2fa-4f52-87a1-5702cf45b595)
클라이언트 서버 와 Chat-bot 서버는 <strong>REST API</strong> 방식으로 통신을 합니다.

### 주요 기능
- 부위별 다양한 웨이트 운동 제공
- 다양한 웨이트 운동에 대한 상세 설명
- 효율적인 트레이닝을 위한 팁 제공
- 직관적으로 이해 할 수 있는 이미지 및 동영상 제공

### DB 구축
[![New-Site-Logo-with-Ring-Updated](https://github.com/vieisi8/E-Health/assets/146730344/d22ecfda-cc87-47f1-a1f1-2390d049ecad)](https://weighttraining.guide/)
<br>
Python 패키지인 <strong>Selenium</strong>을 이용해 위 사이트에서 정보를 수집후 데이터 클리닝 작업을 통해 DB를 구축 했습니다.

### 핵심 기술
이 프로젝트에서의 핵심 기술은 OPEN AI 사의 GPT를 프롬프트 엔지니어링 방법을 이용해 <strong>사용자의 질문을 DB에 접근할 수 있는 SQL 문으로 변환</strong>하는 기술입니다.<br>
즉, <strong>프롬프트 엔지니어링을 통해 LLM을 SQL 특화</strong> 시켰다고 볼 수 있습니다.


# 프로젝트 관리

### 프로젝트 개발 방법론
스크럼

### 협업 및 진척 관리
WBS를 작성하여 각 팀원의 할 일을 지정, 매주 회의를 통한 진척 관리를 했습니다.

> WBS 파일을 참조 해주세요!

### 품질 관리
종합 테스트 시나리오서를 작성하여 품질 관리를 했습니다.

> 종합 테스트 시나리오서 파일을 참조 해주세요!

# 프로젝트 기여
저는 팀장으로서 프로젝트를 이끄는 역할을 하였습니다.

### 프로젝트 개발
저는 주로 <strong>클라이언트 Back-end</strong> 맡아 개발을 진행했습니다.<br>
하지만 팀장으로서 백업을 위해 <strong> 제가 맡지 않은 부분</strong> 도 단위 테스트가 가능한 수준의 <strong>프로토타입을 개발</strong>해봤습니다.
