# Gamlendar Selenium

### 겜린더의 게임 데이터를 자동으로 수집하기 위한 스크래핑 봇

잘 만들어서 Github Action으로 자동화 시켜보자!

## 수집할 게임 사이트
### 1. Steam &check;
    수집 전략
    1. Steam upcoming 중 인기찜 목록만 수집 ✅
    2. 특정 태그가 있는 성인게임은 수집 금지(최대한 보수적으로 수집) ✅
    3. Upcoming 리스트 수집, 상세 페이지(detail) 수집 ✅
    4. Pandas로 각 정보를 CONCAT을 하여 통합 ✅
    5. DB에 정리

    - Exception Handling을 통해 수집 실패한 데이터는 Log 수집 ✅

### Progress
- 2023-11-21 1차 테스트 수집 완료

---

### 2. Playstation

### 3. Xbox

### 4. Nintendo Switch
   






