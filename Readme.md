# Gamlendar Selenium

### 겜린더의 게임 데이터를 자동으로 수집하기 위한 스크래핑 봇

잘 만들어서 Github Action으로 자동화 시켜보자!

## 수집할 게임 사이트
### 1. Steam ✅

### 수집 전략
1. [Steam upcoming](https://store.steampowered.com//search/?filter=popularwishlist&os=win) 중 인기찜 목록만 수집 ✅
2. 특정 태그가 있는 성인게임은 수집 금지(최대한 보수적으로 수집) ✅
3. Upcoming 리스트 수집, 상세 페이지(detail) 수집 ✅

   
- Exception Handling을 통해 수집 실패한 데이터는 Log 수집 ✅
- Backup 목적의 csv 형태의 파일 저장 ✅

### Progress
- 2023-11-21 1차 테스트 수집 완료
- 2023-11-24 2차 수집 & 백업 및 Log 기록 성공

---

### 2. Playstation

### 수집 전략

1. [플레이스테이션 출시 목록](https://store.playstation.com/ko-kr/pages/browse/1?next_thirty_days=conceptReleaseDate)을 수집
2. 특정 장르가 "성인"이 들어가있는 게임은 수집 금지
3. Upcoming 리스트, 상세 페이지(detail) 수집

4. 

### 3. Xbox

### 4. Nintendo Switch

----

## Core
자주 사용하게 될 기능을 Core로 분리

### Data
데이터 통합을 위한 Pandas 활용

### Database
통합한 데이터를 MariaDB에 전송

### Logs
로그 관리를 위한 기능








