# 오늘은 어디서 쉬지? 나만의 숙박 예약 서비스 HotTel

<br />

> 🚀 Built with Flask

- 👉 UX/UI 템플릿 소스 : https://themewagon.com/theme-categories/premium-templates/
<br />

> Features

- `Up-to-date dependencies`
- Database: `mysql`
- `DB Tools`: SQLAlchemy ORM, Flask-Migrate (schema migrations)
- Session-Based authentication (via **flask_login**), Forms validation

<br />



## ✨ 깃 소스 

> Download the code 

```bash
$ # Get the code
$ git clone https://github.com/17101934ksy/CustomApps_Hottel.git
$ cd hottel
```

<br />

#### `LINUX`, `Unix`, `MacOS` 셋 업 

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />


```bash
$ flask run
```

<br />

#### `Windows` 셋 업

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ # CMD 
$ set FLASK_APP=run.py
$ set FLASK_ENV=development
$
$ # Powershell
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

<br />

> Start the app

```bash
$ flask run
```

<br />

## ✨ 시스템 소개



<br />

## ✨ 시스템 구조도

### 👉 `ERD` 설계 

`Users`: 유저(이용객, 사업자)<br />
`BusinessRegisters`: 사업자 등록(일반 이용객에서 사업자 권한 획득)<br />
`BusinessLists`: 사업자 영업 리스트(주소가 다른 숙박 시설을 운영할 수 있기 때문에 사업자와 숙박시설의 일 대 다 성립)<br />
=> 보완 사항: 공동 사업자일 경우가 있음<br />
`Accomodations`: 숙박 시설<br />
`Rooms`: 숙박시설의 다양한 방<br />
`Carts`: 이용객의 장바구니<br />
`Reservations`: 예약 상황<br />

<img src = "https://user-images.githubusercontent.com/88478829/186169072-e3fb93f0-7d6e-4fe7-8096-e86ee0602267.png" width="width 50%" height="height 50%">

### 👉 `package` 설계 

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # HTML을 다루기 위한 home
   |    |    |-- routes.py                  # app의 라우트
   |    |
   |    |-- authentication/                 # 로그인 사용자 등록 및 인증
   |    |    |-- routes.py                  # 인증 처리 라우트 
   |    |    |-- models.py                  # 인증 데이터 베이스  
   |    |    |-- forms.py                   # 폼 구성 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # static 파일
   |    |
   |    |-- templates/                      # HTML 페이지 
   |    |    |-- includes/                  # HTML jinja2 템플릿 구성요소
   |    |    |    |-- scripts.html          # Scripts
   |    |    
   |    |    |-- layouts/                   # Base 파일
   |    |        
   |    |    |-- accounts/                  # 로그인 관련 폴더
   |    |    |    |-- login.html            # 로그인
   |    |    |    |-- register.html         # 등록
   |    |    |
   |    |    |-- home/                      # UI 폴더
   |    |         |-- index.html            # Index
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # 모든 HTML 파
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


---

