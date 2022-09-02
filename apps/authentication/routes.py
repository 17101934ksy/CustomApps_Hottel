from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import SiteLoginForm, CreateAccountForm
from apps.authentication.models import Magazines, Testimonials, Users, BusinessRegisters, BusinessLists, Accomodations, PaymentMethods, Rooms
from apps.authentication.util import verify_pass, crawler_db

import random
from datetime import datetime, date

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    login_form = SiteLoginForm(request.form)

    if 'login' in request.form:

        username = request.form['userName']
        password = request.form['password']
        user = Users.query.filter_by(userName=username).first()

        if not user:
            error = "입력하신 정보가 올바르지 않습니다."

        elif not verify_pass(password, user.password):
            error = '입력하신 정보가 올바르지 않습니다.'

        if error is None:
            session.clear()
            session['user_id']=user.userId       
            login_user(user)
            return redirect(url_for('home_blueprint.index'))

    return render_template('accounts/login.html', form=login_form, error=error)

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm()

    if request.method == 'POST':
        data = request.get_json()

        # Check usename exists
        user = Users.query.filter_by(userName=data['username']).first()
        if user:
            return render_template('accounts/login.html',
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return render_template('accounts/login.html',
                                   form=create_account_form)

        # else we can create the user
        user = Users(userName=data['username'], password=data['password'], 
        email=data['email'], phoneNumber=data['phonenum'])
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        print('session clear!')

        return render_template('accounts/login.html', form=create_account_form)

    else:
        return render_template('accounts/login.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler

@blueprint.errorhandler(403)
def access_forbidden():
    return render_template('errors/page-403.html')


@blueprint.errorhandler(404)
def not_found_error():
    return render_template('errors/page-404.html')


@blueprint.errorhandler(500)
def internal_error():
    return render_template('errors/page-500.html')

# Simulation

@blueprint.route('/simulate_database', methods=['GET', 'POST'])
@login_required
def simulate_database():

    if str(session['user_id']) == '1':  
        data_accomodation = crawler_db('Accomodations')
        data_magazine = crawler_db('Magazines')

        lst_num = int(Users.query.order_by(Users.userId.desc()).first().userId)

        comments = [
            "숙박업소 기춘 예약가는 다른 사이트에 비해 합리적인 가격을 제시하며, 디자인이 깔끔합니다.",
            "모텔, 호텔, 리조트.콘도, 펜션/풀빌라 등 다양한 숙박 시설을 예약할 수 있습니다.",
            "예약 시설에 대한 상세 정보를 제공합니다.",
            "출장이 있어서 숙박을 잡다보면, 출장 위치와 숙박 장소가 먼 경우가 있는데, 거리 계산 기능을 제공하여 손 쉽게 확인할 수 있습니다."
            ]

        for idx, item in enumerate(data_accomodation['Accomodations']):
            accomodation = Accomodations.query.filter_by(accomodationId=item['accomodationId']).first()
            if accomodation is not None:
                continue
            
            lst_num += 1
            # databases 생성
            user = Users(userName=f'user{lst_num}', password='1234', \
                email=f'user{lst_num}@test.com', phoneNumber='01011111111')
            db.session.add(user)
            db.session.commit()

            business_register = BusinessRegisters(userId=user.userId, businessNumber=f'1010-{str(user.userId)}')
            db.session.add(business_register)
            db.session.commit()

            business_list = BusinessLists(businessId=item['accomodationId'], businessAddr=f'seoul-{item["accomodationName"]}', userId=user.userId)    
            db.session.add(business_list)
            db.session.commit()

            accomodation = Accomodations(accomodationId=item['accomodationId'], accomodationType=item['accomodationType'],\
                accomodationName=item['accomodationName'], accomodationImage=item['accomodationImage'], accomodationPrice=item['accomodationPrice'])

            db.session.add(accomodation)
            db.session.commit()

            testimonial = Testimonials(userId=lst_num, testimonialComment=comments[idx%len(comments)])
            
            db.session.add(testimonial)
            db.session.commit()

        for idx, item in enumerate(data_magazine['Magazines']):
            magazine = Magazines.query.filter_by(userId=idx+1).first()
            if magazine is not None:
                continue
            
            user = Users.query.filter_by(userId=idx+1).first()
            item['userId'] = user.userId

            magazine = Magazines(userId=item['userId'], magazineThema=item['magazineThema'], magazineWriter=item['magazineWriter'], \
                magazineDate=item['magazineDate'], magazineView=item['magazineView'], magazineTitle=item['magazineTitle'], \
                    magazineSubTitle=item['magazineSubTitle'], magazineContent=item['magazineContent'], \
                        magazineLink=item['magazineLink'], magazineTag=item['magazineTag'], magazineImage=item['magazineImage'])

            db.session.add(magazine)
            db.session.commit()


        return str("session clear")
    return str("session fail")



@blueprint.route('/test_test', methods=['GET', 'POST'])
def test_test():

    accomodations = Accomodations.query.order_by(Accomodations.accomodationId.desc()).limit(5).all()

    ids, names, images = [], [], []

    for accomodation in accomodations:
        print(accomodation.accomodationId)

    return str(accomodations)


@blueprint.route('/simulate_database/account', methods=['GET', 'POST'])
@login_required
def simulate_database_account():

    if str(session['user_id']) == '1':

        for idx, name in enumerate(['(구)KB국민은행', '(신)KB국민은행', 'IBK기업은행', 'NH농협은행', '(구)신한은행', \
            '(신)신한은행', '우리은행', 'KEB하나은행', '(구)외한은행', '씨티은행', \
                'DGB대구은행', 'BNK부산은행', 'SC제일은행', '케이뱅크', '카카오뱅크']):

            payment_method = PaymentMethods.query.filter_by(paymentMethodSeq=(idx+1)).first()
            if payment_method is not None:
                continue

            payment_method = PaymentMethods(paymentMethod=name, paymentDepositAccount=None)
            
            db.session.add(payment_method)
            db.session.commit()

        return "db_clear"

@blueprint.route('/simulate_database/room', methods=['GET', 'POST'])
@login_required
def simulate_database_room():

    if str(session['user_id']) == '1':

        accomodations = Accomodations.query.order_by(Accomodations.accomodationId.desc()).all()

        ad_list = []
        for ad in accomodations:
            ad_list.append(ad.accomodationId)

        room = Rooms.query.filter_by(Rooms.roomId).first()

        if room is not None:
            return "db clear"

        for idx, ad in enumerate(ad_list):
            for dt in [i for i in range(1, 31)]:
                for number, sp, up, name, image in zip([110, 120, 205, 300], [2, 4, 5, 6], [3, 4, 7, 8], ["Deluxe", "Double Deluxe", "Special", "Royal"], ['room1.jpg', 'room2.jpg', \
                    'room3.jpg', 'room4.jpg']):
                        
                    if sp == 2:
                        rsp = 40000 + idx * 1000
                        rop = 50000 + idx * 1000
                    elif sp == 4:
                        rsp = 47000 + idx * 1000
                        rop = 55000 + idx * 1000
                    elif sp == 5:
                        rsp = 70000 + idx * 1000
                        rop = 80000 + idx * 1000
                    else:
                        rsp = 90000 + idx * 1000
                        rop = 110000 + idx * 1000
                    
                    room = Rooms(roomDateTime=date(2022, 8, dt), roomNumber=number, roomName=name, \
                        roomCheckIn=datetime(2022, 8, dt, 14), roomCheckOut=datetime(2022, 8, dt+1, 11), \
                        roomStandardPopulation=sp, roomUptoPopulation=up, roomImage='/static/image/'+image, roomSalePrice=rsp, \
                            roomOriginalPrice=rop, roomRate=round(random.random()*5, 1), accomodationId=ad)

                    print(room) 
                    db.session.add(room)
                    db.session.commit()

    return "db clear"
