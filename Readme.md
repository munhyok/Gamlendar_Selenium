# Gamlendar Selenium

### 겜린더의 게임 데이터를 자동으로 수집하기 위한 스크래핑 봇

잘 만들어서 Github Action으로 자동화 시켜보자!


## 1. Steam ✅

### 수집 전략

1. [Steam upcoming](https://store.steampowered.com//search/?filter=popularwishlist&os=win) 중 인기찜 목록만 수집 ✅
2. 특정 태그가 있는 성인 게임 수집 금지(최대한 보수적으로 수집) ✅
3. Upcoming 리스트 수집, 상세 페이지(detail) 수집 ✅

   



### Progress
- 2023-11-21 1차 테스트 수집 완료
- 2023-11-24 2차 수집 & 백업 및 Log 기록 성공
- 


### Bug Note
- 2023-11-29 **[Critical]**
  - 성인 게임 인식 후 None으로 생략해버려 생긴 gameList와 detailList 싱크 오류 수정

---

## 2. Playstation

### 수집 전략

1. [플레이스테이션 출시 목록](https://store.playstation.com/ko-kr/pages/browse/1?next_thirty_days=conceptReleaseDate) 수집 ✅
2. 특정 장르가 "성인"이 들어가있는 게임 수집 금지
3. Upcoming 리스트, 상세 페이지(detail) 수집



## 3. Xbox

## 4. Nintendo Switch



## Core
자주 사용하게 될 기능을 Core로 분리

### Data
데이터 통합을 위한 Pandas 활용
- Backup 목적의 csv 형태의 파일 저장 ✅

### Database
통합한 데이터를 MariaDB에 전송

### Logs
로그 관리를 위한 기능
- Exception Handling을 통해 수집 실패한 데이터는 Log 수집 ✅








