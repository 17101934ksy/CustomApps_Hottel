# 오늘은 어디서 쉬지? 나만의 숙박 예약 서비스 핫텔!

<br />

## ✨ 시스템 기획 및 소개

		
<br />

## ✨ 시스템 구조도

`Users`: 유저(이용객, 사업자)<br />
`BusinessRegisters`: 사업자 등록(일반 이용객에서 사업자 권한 획득)<br />
`BusinessLists`: 사업자 영업 리스트(주소가 다른 숙박 시설을 운영할 수 있기 때문에 사업자와 숙박시설의 일 대 다 성립)<br />
`Accomodations`: 숙박 시설<br />
`Rooms`: 숙박시설의 다양한 방<br />
`Carts`: 이용객의 장바구니<br />
`Reservations`: 예약 상황<br />
`RoomReviews`: 방에 대한 리뷰<br />
`Points`: 댓글에 대한 포인트<br />
`RoomReviewComments`: 리뷰 코멘트<br />
`PaymentMethods`: 지불 수단 <br/>
`PaymentSaleMethods`: 할인 수단 <br/>
`UsedComplete`: 사용 완료 <br/>
`Magazines`: 여행 매거진<br />
`MagazineComments`: 여행 코멘트<br />
`Testimonials`: 테스트 리뷰 <br />

<img src = "https://user-images.githubusercontent.com/88478829/188262699-44628000-6038-4bfe-9a62-8b658b4f02a8.png" width="width 50%" height="height 50%">

### 👉 `package` 설계 

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # home
   |    |    |-- routes.py                  # routes for app(render templates, fetch data etc...)
   |    |    |-- fetchs.py                  # fetch from database
   |    |
   |    |-- authentication/                 # authenticate for login
   |    |    |-- routes.py                  # routes for authentication 
   |    |    |-- models.py                  # database
   |    |    |-- forms.py                   # form
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




