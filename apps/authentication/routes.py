from flask import render_template, request, redirect, url_for, session, jsonify

from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import SiteLoginForm, CreateAccountForm
from apps.authentication.models import Users, BusinessRegisters, BusinessLists, Accomodations
from apps.authentication.util import verify_pass, crawler_db

import os, hashlib, binascii, requests, re, time, random
from urllib.request import urlopen
from bs4 import BeautifulSoup


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = SiteLoginForm()
    return render_template('accounts/login.html', form=login_form)

@blueprint.route('/check_login', methods=['GET', 'POST'])
def check_login():
    error = None

    if request.method == 'POST':
        data = request.get_json()

        user = Users.query.filter_by(userName=data['username']).first()

        if not user:
            error = "입력하신 정보가 올바르지 않습니다."

        elif not verify_pass(data['password'], user.password):
            error = '입력하신 정보가 올바르지 않습니다.'

        if error is None:
            session.clear()
            session['user_id']=user.userId
            print('success')
            return jsonify({"result":"success"})

    return jsonify({"result":"fail"})


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
    return render_template('home/errors/page-403.html')


@blueprint.errorhandler(404)
def not_found_error():
    return render_template('home/errors/page-404.html')


@blueprint.errorhandler(500)
def internal_error():
    return render_template('home/errors/page-500.html')

# Simulation

@blueprint.route('/simulate_database', methods=['GET', 'POST'])
def simulate_database():

    if str(session['user_id']) == '1':  
        data = crawler_db('Accomodations')
        lst_num = int(Users.query.order_by(Users.userId.desc()).first().userId)


        for item in data['Accomodations']:
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
                accomodationName=item['accomodationName'], accomodationImage=item['accomodationImage'])

            db.session.add(accomodation)
            db.session.commit()

        return str("session clear")
    return str("session fail")


@blueprint.route('/test_test', methods=['GET', 'POST'])
def test_test():
    # url = urlopen("https://www.yanolja.com/hotel")
    # btfs = BeautifulSoup(url, "html.parser")

    # data = []
    # for a in btfs.find_all('a', {'class': 'ListItem_container__1z7jK SubhomeList_item__1IR4d'}):
    #     data.append(a)

    # return str(data)

    # user = Users.query.order_by(Users.userId.desc()).limit(5).all()
    # return str(user)
    
    accomodations = Accomodations.query.order_by(Accomodations.accomodationId.desc()).limit(5).all()

    ids, names, images = [], [], []

    for accomodation in accomodations:
        print(accomodation.accomodationId)

    return str(accomodations)

    # businesslists = BusinessLists.query.order_by(BusinessLists.businessId.desc()).limit(5).all()
    # print(type(businesslists))
    # print(businesslists[0])
    # return str(businesslists)