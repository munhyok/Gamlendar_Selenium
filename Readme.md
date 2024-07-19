# Gamlendar Selenium

### 겜린더의 게임 데이터를 자동으로 수집하기 위한 스크래핑 봇

잘 만들어서 자동화 시켜보자!

**robots.txt에 준수하여 수집이 불가능한 페이지는 수집하지 않습니다.**

구조와 코드를 최대한 일관성 있게 구성하여 이해하기 쉽게 작성하려고 노력했습니다... 

### Blog Post
[겜린더 스크래핑 봇 제작기 Steam편](https://velog.io/@grit_munhyeok/겜린더-스크래핑-봇-제작기-Steam)

[약 2300개의 게임을 수집해 DB에 저장하기](https://velog.io/@grit_munhyeok/약-2300개의-게임을-수집해-DB에-저장하기)

## Architecture

![](/image/Pipeline.png)


**ETL 패턴**

**E: Data 수집**
  - Selenium으로 데이터 수집
  
**T: Data Cleansing**
  - 필요없는 문자를 정리하고 정해진 CSV형식에 맞게 저장

**L: Save in MariaDB**
  - 정리된 CSV 파일을 DB에 저장

## V2
![](/image/V2.png)

## CheckList Table

### 수집 페이지
|수집 페이지|완료|비고
|:---:|:---:|:---:|
|Steam|✅|
|Playstation|✅|
|Xbox|✅|
|Switch|✅|Selenium 화면 상단에 띄우지 않으면 터짐|


### Core
|Core|완료|비고|
|:---:|:---:|:---:|
|concatData|✅|
|failedLog|✅|각 플랫폼별로 로그 생성 추후 코드 Refactoring하기
|Database|✅|DB 테이블 생성 완료
|        |✅|자원 공유를 위해 싱글톤 패턴으로 제작
|DataCleaning|✅|겜린더에 맞는 Date형태로 완성
|DataCleaning|🟡|게임 이름 통일시키기





## 1. Steam ✅
### 요약 테이블
|기능|완료|
|:---:|:---:|
|Scroll Scrap|✅|
|Detail Scrap|✅|
|Adult Pass|✅|
|Adult Game Filtering|✅|

### 수집 전략

1. [Steam upcoming](https://store.steampowered.com//search/?filter=popularwishlist&os=win) 중 인기찜 목록만 수집 ✅
2. 특정 태그가 있는 성인 게임 수집 금지(최대한 보수적으로 수집) ✅
3. Upcoming 리스트 수집, 상세 페이지(detail) 수집 ✅

   



### Progress
- 2023-11-21 1차 테스트 수집 완료
- 2023-11-24 2차 수집 & 백업 및 Log 기록 성공
- 2023-12-03 3차 수집 2023-11-29 디버깅 검증 완료


### Bug Note
- 2023-11-29 **[Critical]** **FIXED!**
  - 성인 게임 인식 후 None으로 생략해버려 생긴 gameList와 detailList 싱크 오류 수정 ✅

---

## 2. Playstation ✅
### 요약 테이블
|기능|완료|
|:---:|:---:|
|Page Scrap|✅|
|Detail Scrap|✅|
|Adult Game Filtering|✅|


### 수집 전략

1. [플레이스테이션 출시 목록](https://store.playstation.com/ko-kr/pages/browse/1?next_thirty_days=conceptReleaseDate) 수집 ✅
2. 게임 장르 중 "성인"이 들어가있는 게임 수집 금지 ✅
3. Upcoming 리스트, 상세 페이지(detail) 수집 ✅

### Progress
- 2023-12-10 테스트 수집 완료
- 2023-12-10 백업 및 Log 기록 성공

### Bug Note
- 2024-05-17 **[Critical]** **FIXED!**
  - 처음 게임 리스트 수집 시 다음 페이지로 넘어가지 못해 일부 게임 수집이 누락되는 버그 ✅

---


## 3. Xbox

### 요약 테이블
|기능|완료|
|:---:|:---:|
|Page Scrap|✅|
|Detail Scrap|✅|
|Screenshot Controler|✅|
|Tag Spliter|✅|
|Bundle Detector|✅|

### 수집 전략

1. 로그인 ✅
2. [Xbox 출시 목록](https://www.xbox.com/ko-kr/games/all-games?cat=upcoming) 수집 ✅
3. Upcoming 리스트, 상세 페이지(detail) 수집 ✅
4. 스크린샷 수집 로직 작성 ✅

### Bundle Detector 알고리즘
![](/image/Xbox_Detect_DLC.png)


## 4. Nintendo Switch ✅

|기능|완료|
|:---:|:---:|
|Page Scrap|✅|
|Detail Scrap|✅|
|Screenshot Controler|✅|
|Tag Spliter|✅|
|Eng_Translator|⛔️|
|Title Extractor|✅|

### 수집 전략

1. [Nintendo Switch](https://store.nintendo.co.kr/games/all-released-games) 수집 ✅
2. Upcoming 리스트, 상세 페이지(detail) 수집 ✅
3. popup close, Screenshot next 로직 작성 ✅
4. Extract Title을 통해 한글 영문 이름 분리 추출 ✅
   1. 괄호 안에 있는 영문 & 한글 이름을 같이 수집
   2. 괄호 안 문자열이 한글인지 영문인지 판단
   3. kor,eng 변수에 각각 저장 

### 난제
스위치는 한국어 페이지와 북미 페이지의 디자인과 디렉터리 구조가 완전 달라 어떻게 수집해야할 지 전략 구상 중

생각해 본 방법들
1. GPT를 사용해서 게임 이름 영문 번역
  - 이게 제일 합리적인 수단이라고 판단 중
  돈이 들긴해도... 😂
2. 구글 번역기를 사용
  - 일부 단어가 제대로 번역이 되질 않음
3. 직접 단어를 수집해 매칭하는 방법
  - 시간이 너무 오래걸린다.


여러가지 난제로 인해 한국어 페이지부터 수집

### 차선책
일부 게임 타이틀에 한국어와 영어를 합쳐 나온 타이틀이 있다.

Ex. 유니콘 오버로드 (Unicorn Overlord)

이런 구조의 게임들은 한글과 영문 이름을 각각 추출해 해결


### 해결 방안
- 수집하는 게임을 DB에 검색
- DB에 게임이 있으면 게임 이름을 DB에 있는 게임 이름으로 덮어쓰기



### Progress
- 2024-05-17 홈페이지 리뉴얼로 인한 이미지 수집 로직 재작성 ✅




## Core
자주 사용하게 될 기능을 Core로 분리

### Data
데이터 통합(CONCAT)을 위한 Pandas 활용
- Backup 목적의 csv 형태의 파일 저장 ✅
  
Data Cleaning Text Data를 겜린더에 맞게 수정하는 과정
- 날짜, 특정 단어 수정 및 제외 같은 필터링 작업 ✅

### Database
1. 통합한 데이터를 MariaDB에 전송

2. MariaDB에 있는 데이터를 MongoDB로 전송

3. 싱글톤 패턴 적용: Database 클래스는 하나의 인스턴스만 생성해 사용하도록 구현


#### DB ERD
![](/image/DB_ERD.png)
title에 의존하는 관계


최적화 할 부분이 있다면 적극적으로 할 예정

### Logs
로그 관리를 위한 기능
- Exception Handling을 통해 수집 실패한 데이터는 Log 수집 ✅
- Platform마다 log를 분류 ✅


### 공통 고려사항..(우선 순위 낮음)
- autokwd plain 데이터 포함시켜보기
- 근데 출시 날짜가 미정인 게임이 출시하면 어떻게 판별해야할까? hashcode가 서로 다르면 교체하는 방식..? (일단 미정)
- 중복 체크는 DB의 Unique 사용 ✅






