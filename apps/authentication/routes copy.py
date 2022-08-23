from flask import render_template, request, redirect, url_for, flash, session, jsonify

from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import SiteLoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.util import hash_pass, verify_pass
import json

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = SiteLoginForm()
    error = None

    if request.method == 'POST':
        data = request.get_json()

        user = Users.query.filter_by(username=data['username']).first()

        if not user:
            error = "입력하신 정보가 올바르지 않습니다."

        elif not verify_pass(data['password'], user.password):
            error = '입력하신 정보가 올바르지 않습니다.'

        if error is None:
            session.clear()
            session['user_id']=user.id
            return redirect(url_for('home_blueprint.index'))

        flash(error)
    return render_template('accounts/login.html', form=login_form)

@blueprint.route('/check_login', methods=['GET', 'POST'])
def check_login():
    error = None

    if request.method == 'POST':
        data = request.get_json()

        user = Users.query.filter_by(username=data['username']).first()

        if not user:
            error = "입력하신 정보가 올바르지 않습니다."

        elif not verify_pass(data['password'], user.password):
            error = '입력하신 정보가 올바르지 않습니다.'

        if error is None:
            session.clear()
            session['user_id']=user.id
            return jsonify({"result":"success"})

        flash(error)
    return jsonify({"result":"fail"})


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm()

    if request.method == 'POST':
        data = request.get_json()

        # Check usename exists
        user = Users.query.filter_by(username=data['username']).first()
        if user:
            return render_template('accounts/login.html',
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return render_template('accounts/login.html',
                                   form=create_account_form)

        # else we can create the user
        user = Users(username=data['username'], password=data['password'], 
        email=data['email'], phonenum=data['phonenum'])
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

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