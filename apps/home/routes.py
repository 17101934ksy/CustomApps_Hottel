from apps import db
from apps.home import blueprint
from apps.home.fetchs import fetch_accomodations, fetch_testimonials, fetch_magazines, fetch_rooms, fetch_room_details
from apps.authentication.models import Accomodations, Magazines, PaymentMethods, Reservations, Rooms, UserCoupons, Points
from apps.authentication.forms import MagazineForm, ReservationForm, PaymentForm

from wtforms.validators import DataRequired, NumberRange

from flask import render_template, request, session, redirect, url_for
from flask_login import login_required

from jinja2 import TemplateNotFound, TemplateAssertionError
from werkzeug.utils import secure_filename

from sqlalchemy import or_, and_

import datetime, math, os, shutil
from datetime import date, datetime, timedelta

@blueprint.route('/<template>')
def route_template(template):

    try:
        if not template.endswith('.html'):
            template += '.html'

        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)

    except TemplateAssertionError:
        return render_template('errors/page-403.html'), 403
    except TemplateNotFound:
        return render_template('errors/page-404.html'), 404
    except:
        return render_template('errors/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None


@blueprint.route('/index')
def index():
    ids, names, images, prices = fetch_accomodations(20)
    uids, unames, comments = fetch_testimonials(8)
    return render_template('home/index.html', accomodationId=ids, accomodationName=names, accomodationImage=images, \
        accomodationPrice=prices, userId=uids, userName=unames, testimonialComment=comments, zip=zip, enumerate=enumerate) 


@blueprint.route('/about')
def view_about():
    uids, unames, comments = fetch_testimonials(8)
    return render_template('home/about.html', templateName='about', userId=uids, userName=unames, testimonialComment=comments, zip=zip)

@blueprint.route('/contact')
def view_contact():
    return render_template('home/contact.html', templateName='연락처')

@blueprint.route('/gallery')
def view_gallery():
    return render_template('home/gallery.html', templateName='HoTTel 갤러리')


@blueprint.route('/elements')
def view_elements():
    return render_template('home/elements.html', templateName='지울 예정')


#---------------------------------------------------------------- Magazine Start --------------------------------------------------------------------------#

@blueprint.route('/magazine/<page_number>', methods=['GET', 'POST'])
def view_magazine(page_number):

    magazine = fetch_magazines('all')
    contents_subject = ["여행", "미식", "숙소"]
    contents_thema = [0] * 3
    for thema in magazine['magazineThema']:
        if thema == contents_subject[0]:
            contents_thema[0] += 1
        elif thema == contents_subject[1]:
            contents_thema[1] += 1
        elif thema == contents_subject[2]:
            contents_thema[2] += 1

    for idx, tag in enumerate(magazine['magazineTag']):
        magazine['magazineTag'][idx] = tag.split('#')
        
    
    return render_template('home/magazine.html', templateName='magazine', magazine=magazine, pageNumber=page_number, userId=session['user_id'],\
        contentsSubject=contents_subject, contentsThema=contents_thema, nowDate=datetime.now(), zip=zip, enumerate=enumerate, len=len, ceil=math.ceil, int=int)
    

@blueprint.route('/magazine-detail/<magazine_id>')
def view_magazine_detail(magazine_id, magazine_writer, magazine_date, magazine_view, magazine_comment, magazine_title, magazine_content, magazine_link, \
    magazine_image, magazine_tag, magazine_thema):

    return render_template('home/magazine-detail.html', templateName='매거진 상세 정보', \
        nowDate=datetime.now(), zip=zip, enumerate=enumerate, len=len, ceil=math.ceil, int=int)


@blueprint.route('/magazine-write/Write<user_id>', methods=['GET', 'POST'])
@login_required
def view_magazine_write(user_id):

    magazine_data = fetch_magazines(1)

    magazine_seq = int(magazine_data['magazineSeq'][0]) + 1

    magazine_form = MagazineForm(request.form)

    if 'magazine' in request.form:
        if magazine_form.validate_on_submit():

            magazine_title = request.form['visibleTitle']
            magazine_thema = request.form['hiddenThema']
            magazine_content = request.form['hiddenContent']
            magazine_image = request.files['visibleFile']
            magazine_tag = request.form['visibleTag']

            if str(magazine_image.filename) == "":
                path = "./apps/static/image/magazines/" 

                if os.path.exists(path + str(magazine_seq)):
                    shutil.rmtree(path + str(magazine_seq))
            
                os.mkdir(path + str(magazine_seq))
                new_path = str(magazine_seq) + '/noimg.jpg'

                shutil.copyfile(path + "noimg.jpg", path + str(magazine_seq) +'/noimg.jpg')
            
            else:
                path = "./apps/static/image/magazines/" + str(magazine_seq)

                if os.path.exists(path):
                    shutil.rmtree(path)
                os.mkdir(path)
                new_path = str(magazine_seq) + "/" + secure_filename(magazine_image.filename)
                magazine_image.save(path + "/" + secure_filename(magazine_image.filename))

            new_path = '/static/image/magazines/' + new_path

            magazine = Magazines(userId=user_id, magazineThema=magazine_thema, magazineWriter='Writer_'+f'{user_id}',
            magazineDate=datetime.now(), magazineView=0, magazineTitle=magazine_title, magazineSubTitle='', magazineContent=magazine_content,
            magazineLink=str(magazine_seq), magazineTag=magazine_tag, magazineImage=new_path)

            db.session.add(magazine)
            db.session.commit()

            
            return redirect(url_for('home_blueprint.view_magazine', page_number=1))

    return render_template('home/magazine-write.html', templateName='매거진 글쓰기', \
        userId=user_id, magazineSeq=magazine_seq, nowDate=datetime.now(), zip=zip, enumerate=enumerate, \
            form = magazine_form)


#---------------------------------------------------------------- Magazine End --------------------------------------------------------------------------#

#---------------------------------------------------------------- Accomodation Start --------------------------------------------------------------------------#

@blueprint.route('/accomodation')
def view_accomodation():
    ids, names, images, prices = fetch_accomodations(20)
    return render_template('home/accomodation.html', templateName='accomodation', accomodationId=ids, accomodationName=names, accomodationImage=images, accomodationPrice=prices, \
        zip=zip, enumerate=enumerate)    

@blueprint.route('/room', methods=['GET', 'POST'])
def view_room():

    accomodation_id = request.args.get('accomodationId')
    rooms = fetch_rooms(accomodation_id)
    accomodation_name = Accomodations.query.filter_by(accomodationId=accomodation_id).first().accomodationName
    
    return render_template('home/room.html', templateName='객실', rooms=rooms, accomodationName=accomodation_name, zip=zip, enumerate=enumerate)    

@blueprint.route('/room-detail', methods=['GET', 'POST'])
def view_room_detail():

    reservation_form = ReservationForm(request.form)
    
    room_id = request.args.get('roomId')
    room, already_reservations = fetch_room_details(room_id)

    print(already_reservations)

    today = date.today()
    now_time = datetime.now()
    room_check_in_hour, room_check_in_minute = map(int, room.roomCheckIn.split(':'))

    # 체크인 시간보다 두시간은 여유가 있어야 당일 예약이 가능
    reservation_same_day = False
    if now_time < datetime(today.year, today.month, today.day, room_check_in_hour-2, room_check_in_minute):
        reservation_same_day = True

    if 'reservation' in request.form:
        print(session['user_id'])
        
        py1, pm1, pd1 = map(int, request.form["period1"].split('-'))
        py2, pm2, pd2 = map(int, request.form["period2"].split('-'))
        period1, period2 = date(py1, pm1, pd1), date(py2, pm2, pd2)

        reservation = Reservations.query.filter(and_(Reservations.roomId==room_id, \
            or_(and_(period1 <= Reservations.roomCheckInDate, Reservations.roomCheckInDate < period2), \
                and_(Reservations.roomCheckInDate <= period1, period1 < Reservations.roomCheckOutDate)))).first()
                
        if reservation is not None:
            print("이미 객실이 존재합니다.")
            return render_template('home/room-detail.html', template='객실 상세 정보', room=room, zip=zip, enumerate=enumerate, form=reservation_form, today=date.today(), \
        alreadyReservations=already_reservations, reservationSameDay=reservation_same_day)


        reservation = Reservations(userId=session['user_id'], roomId=room_id, roomCheckInDate=period1, roomCheckOutDate=period2, paymentMethodSeq=1, \
            couponSeq=None, paymentDateTime=datetime.now(), paymentName='', paymentPoint=0, paymentAccount=None, paymentRefundAccount='')

        db.session.add(reservation)
        db.session.commit()

        print('예약 체인 완료')

        return redirect(url_for('home_blueprint.view_room_reservation_payment', reserve_seq=reservation.reserveSeq))
    
    return render_template('home/room-detail.html', template='객실 상세 정보', room=room, zip=zip, enumerate=enumerate, form=reservation_form, today=today, \
        alreadyReservations=already_reservations, reservationSameDay=reservation_same_day)


@blueprint.route('/room-reservation-payment/<reserve_seq>', methods=['GET', 'POST'])
@login_required
def view_room_reservation_payment(reserve_seq):

    try:
        if session['user_id'] is None:
            return redirect(url_for('authentication_blueprint.login'))

    except:
        print("허가 받지 않는 사용자입니다.")
        return redirect(url_for('authentication_blueprint.login'))

    # query
    reservation = Reservations.query.filter_by(reserveSeq=reserve_seq).first()
    room = Rooms.query.filter_by(roomId=reservation.roomId).first()
    payment_method_dict = PaymentMethods.query.all()    
    user_coupon = UserCoupons.query.filter_by(userId=session['user_id']).all()
    point = Points.query.filter_by(userId=session['user_id']).first()
    
    # dict-list data -> list-dict 처리
    payment_method = [pmd.paymentMethod for pmd in payment_method_dict]
    coupon = "사용 가능한 쿠폰 없습니다." if user_coupon is None else [cou.couponId for cou in user_coupon]

    # room price calculate
    check_in = reservation.roomCheckInDate
    check_out = reservation.roomCheckOutDate
    total_room_price = 0

    # form attribute
    point = 0 if point is None else point.pointSum

    payment_form = PaymentForm(request.form)
    payment_form.paymentPoint.validators = [DataRequired("포인트를 입력하세요"), NumberRange(min=0, max=point)]
    today = date.today()

    while check_in != check_out:
        if check_in.weekday() not in [4, 5]:
            total_room_price += room.roomSalePrice if room.roomSalePrice is not None else room.roomOriginalPrice
        else:
            total_room_price += room.roomHolidayPrice
        check_in += timedelta(days=1)

    # request
    if 'payment' in request.form and payment_form.validate_on_submit():

        payment_name = request.form['paymentName']
        payment_method = request.form['paymentMethod']
        payment_sale = request.form['saleCoupon']
        payment_point = request.form['paymentPoint']
        payment_account = request.form['paymentAccount']
        payment_refund_account = request.form['paymentRefundAccount']
            
        return "session clear"

    return render_template('home/room-payment.html', template='객실 예약', room=room, zip=zip, enumerate=enumerate, form=payment_form, today=today, \
        reservation=reservation, totalRoomPrice=total_room_price, point=point, userCoupon=user_coupon, paymentMethod=payment_method)


#---------------------------------------------------------------- Accomodation End --------------------------------------------------------------------------#



#---------------------------------------------------------------- Reservarion Start --------------------------------------------------------------------------#

@blueprint.route('/reservation/selectroom/<user_id>')
def view_select_room(user_id):
    
    form = ReservationForm(request.form)
    
    if 'reservation' in request.form:
        return "hello"

    return redirect('url_for(home_blueprint.accomodation)')

@blueprint.route('/reservation/selectaccount/<user_id>')
def view_select_account(user_id):
    return "clear"

@blueprint.route('/reservation/account/<user_id>')
def view_account(user_id):
    return "clear"