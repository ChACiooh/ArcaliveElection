# ArcaliveElection
아카라이브에서 나눔 이벤트 댓글 이벤트용. 웹 크롤링을 통해 손쉽게 당첨자들을 가려냅니다.

# Patches
## 0.0.1
2023-07-23 released, 인원수 n명을 뽑아 뽑힌 n명의 이름과 사용자 정보 URL 제공. 반고닉인 경우에도 가능하며 이 버전에서는 반고닉, 고닉만 해당될 경우에 적용할 수 있음
## 0.0.2
2023-07-24 released, 참여자 수가 매우 많아 코멘트 페이지 수가 생길 경우 이에 대한 집계를 모두 진행. 또한 글 작성자가 마감한 댓글 이후 뒤늦게 참여한 사람을 제외하도록 버그 수정

# Usage
## Installation
```bash
pip3 install bs4
pip3 install requests
```
## Run
```python
python3 wctest.py
```
