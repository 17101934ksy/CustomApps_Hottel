from apps import db
from apps.home import blueprint
from apps.authentication.fetchs import fetch_accomodations, fetch_testimonials, fetch_magazines, fetch_rooms_detail
from apps.authentication.models import Accomodations, Magazines
from apps.authentication.forms import MagazineForm

from flask import render_template, request, session, redirect, url_for
from flask_login import login_required

from jinja2 import TemplateNotFound, TemplateAssertionError
from werkzeug.utils import secure_filename


import datetime, math, os, shutil

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
    return render_template('home/contact.html', templateName='contact')

@blueprint.route('/gallery')
def view_gallery():
    return render_template('home/gallery.html', templateName='gallery')


@blueprint.route('/elements')
def view_elements():
    return render_template('home/elements.html', templateName='elements')


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
        contentsSubject=contents_subject, contentsThema=contents_thema, nowDate=datetime.datetime.now(), zip=zip, enumerate=enumerate, len=len, ceil=math.ceil, int=int)
    

@blueprint.route('/magazine-detail/<magazine_id>')
def view_magazine_detail(magazine_id, magazine_writer, magazine_date, magazine_view, magazine_comment, magazine_title, magazine_content, magazine_link, \
    magazine_image, magazine_tag, magazine_thema):

    return render_template('home/magazine-detail.html', templateName='magazine-detail', \
        nowDate=datetime.datetime.now(), zip=zip, enumerate=enumerate, len=len, ceil=math.ceil, int=int)


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
            print("**** request ****")

            print(magazine_content)

            magazine = Magazines(userId=user_id, magazineThema=magazine_thema, magazineWriter='Writer_'+f'{user_id}',
            magazineDate=datetime.datetime.now(), magazineView=0, magazineTitle=magazine_title, magazineSubTitle='', magazineContent=magazine_content,
            magazineLink=str(magazine_seq), magazineTag=magazine_tag, magazineImage=new_path)

            db.session.add(magazine)
            db.session.commit()

            print("**** end ****")
            
            return redirect(url_for('home_blueprint.view_magazine', page_number=1))

    return render_template('home/magazine-write.html', templateName='magazine-write', \
        userId=user_id, magazineSeq=magazine_seq, nowDate=datetime.datetime.now(), zip=zip, enumerate=enumerate, \
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

    rooms = fetch_rooms_detail(accomodation_id)
    
    accomodation_name = Accomodations.query.filter_by(accomodationId=accomodation_id).first().accomodationName

    print(rooms)
    
    return render_template('home/room.html', templateName='room', rooms=rooms, accomodationName=accomodation_name, zip=zip, enumerate=enumerate)    

#---------------------------------------------------------------- Accomodation End --------------------------------------------------------------------------#

#---------------------------------------------------------------- Reservarion Start --------------------------------------------------------------------------#

@blueprint.route('/reservation/selectroom/<user_id>')
def view_select_room(user_id):
    return redirect('url_for(home_blueprint.accomodation)')

@blueprint.route('/reservation/selectaccount/<user_id>')
def view_select_account(user_id):
    return "clear"

@blueprint.route('/reservation/account/<user_id>')
def view_account(user_id):
    return "clear"