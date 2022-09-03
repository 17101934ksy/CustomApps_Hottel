# 오늘은 어디서 쉬지? 나만의 숙박 예약 서비스 핫텔!

<br />

## ✨ 팀 소개

<img src="https://user-images.githubusercontent.com/88478829/186391655-470d1ac5-a34a-4dfa-b7ae-0d5754631c91.png" width="width 50%" height="height 50%"> </image>
<br/>
> 🚀 저희 팀은 협업을 중요시하는 서울과학기술대학교 산업정보시스템공학과 열정페이 동아리의 리액션팀입니다.

역할|이름|학번|Git|개발|
---|---|---|---|---|
기획|우명균|19102006|[woomk](https://github.com/woomk)|서비스 기획
팀장|고세윤|17101934|[17101934ksy](https://github.com/17101934ksy)|팀원 통합 및 개발
개발|김소연|21101039|[thdus](https://github.com/thdus)|로그인 개발
개발|황지연|21101989|[ghkdwldus0807](https://github.com/ghkdwldus0807)|로그인 개
<br/>


## ✨ 깃 소스 

> Download the code 

```bash
$ # Get the code
$ git clone https://github.com/17101934ksy/CustomApps_Hottel.git
$ cd hottel
```
<br />
<br />
## ✨ 시스템 기획 및 소개

### 👉 기획 목표

숙박 시설 예약 서비스인 "HoTTel"을 개발

<br />
### 👉 데스크 리서치 및 구현 목표

1. 메인 첫 화면에서 예약 가능한 방을 빠르게 검색할 수 있도록 하는 기능이 필요함
2. 레저를 즐기고자 하는 장소와 숙박 시설 사이의 거리를 계산하고, 추천 경 웹에서 바로 확인 가능한 기능이 필요함
3. 원하는 숙소의 모든 예약이 다 찼을 때, 알림 설정 기능을 통해, 기존 예약자가 예약 취소 시 "~방 예약 가능합니다" 라고 알림을 보내는 기능

  
### 👉 세부 시행 계획

	- 공통 기능:
		1. 로그인
		2. 숙박 시설 확인 및 상세 검색
		3. 호텔 예약 및 예약 취소, 리뷰 작성
		4. 매거진(홍보) 작성 및 게시, 댓글
	
	- 차별화 기능:
		1. 메인 화면에서 빠른 예약 적용
		2. 레저 시설과 해당 숙소의 거리 및 추천 경로 제공
		3. 알림 추가한 방 예약 가능 여부 알림 보내기 기능
		

<br />

## ✨ 시스템 구조도

### 👉 `ERD` 설계 수정 중 

`Users`: 유저(이용객, 사업자)<br />
`BusinessRegisters`: 사업자 등록(일반 이용객에서 사업자 권한 획득)<br />
`BusinessLists`: 사업자 영업 리스트(주소가 다른 숙박 시설을 운영할 수 있기 때문에 사업자와 숙박시설의 일 대 다 성립)<br />
`Accomodations`: 숙박 시설<br />
`Rooms`: 숙박시설의 다양한 방<br />
`Carts`: 이용객의 장바구니<br />
`Reservations`: 예약 상황<br />
`Reviews`: 방에 대한 리뷰<br />
`Points`: 댓글에 대한 포인트<br />
`ReviewComments`: 리뷰 코멘<br />
`Magazines`: 여행 매거진<br />
`MagazineComments`: 여행 코멘트<br />

<img src = "https://user-images.githubusercontent.com/88478829/186169072-e3fb93f0-7d6e-4fe7-8096-e86ee0602267.png" width="width 50%" height="height 50%">

### 👉 `package` 설계 

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # home
   |    |    |-- routes.py                  # routes for app(render templates, fetch data etc...)
   |    |
   |    |-- authentication/                 # authenticate for login
   |    |    |-- routes.py                  # routes for authentication 
   |    |    |-- models.py                  # database
   |    |    |-- forms.py                   # form
   |    |    |-- fetchs.py                  # fetch from database
   |    |    |-- util.py                    # function for utils 
   |    |
   |    |-- info/
   |    |    |-- ERD_system.png             # ERD_system 관계도
   |    |-- static/
   |    |    |-- <css, JS, images>          # static
   |    |
   |    |-- templates/                      # HTML
   |    |    |-- includes/                  # Static templates
   |    |    |    |-- *.html                # includes templates
   |    |    
   |    |    |-- macros/                    # Macro templates
   |    |    |    |-- macros.html           # macros templates
   |    |    
   |    |    |-- layouts/                   # Base
   |    |    |    |-- base.html             # base templates
   |    |        
   |    |    |-- accounts/                  # Login
   |    |    |    |-- login.html            # login and register templates
   |    |       
   |    |    |-- home/                      # UX/UI
   |    |         |-- index.html            # Index
   |    |         |-- *.html                # all UX/UI templates
   
   |    |    |-- errors/                    # Errors
   |    |    |    |-- *.html                # erros templates    
   |    |    
   |  config.py                             # Config
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- app.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

## ✨ 템플릿 소스 출처

- 👉 UX/UI 템플릿 소스 : https://themewagon.com/theme-categories/premium-templates/

---




