# 오늘은 어디서 쉬지? 나만의 숙박 예약 서비스 핫텔!

<br />

- 👉 서비스 소개

<img src="https://user-images.githubusercontent.com/88478829/186391655-470d1ac5-a34a-4dfa-b7ae-0d5754631c91.png" width="width 50%" height="height 50%"> </image>
<br/>
> 🚀 '열정페이'동아리의 페이팀 소개

역할|이름|학번|Git|개발|
---|---|---|---|---|
기획|우명균|19102006|[woomk](https://github.com/woomk)|서비스 기획
팀장|고세윤|17101934|[17101934ksy](https://github.com/17101934ksy)|백엔드, 프론트
개발|김소연|21101039|[thdus](https://github.com/thdus)|프론트
개발|황지연|21101989|[ghkdwldus0807](https://github.com/ghkdwldus0807)|프론트
<br/>
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


---




