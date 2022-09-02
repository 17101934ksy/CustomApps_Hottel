from apps.authentication.fetchs import fetch_accomodations, fetch_testimonials, fetch_magazines
from apps.authentication.models import Magazines
from apps.home import blueprint
from flask import render_template, request, session, jsonify, redirect, url_for
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


@blueprint.route('/accomodation')
def view_accomodation():
    ids, names, images, prices = fetch_accomodations(20)
    return render_template('home/accomodation.html', templateName='accomodation', accomodationId=ids, accomodationName=names, accomodationImage=images, accomodationPrice=prices, \
        zip=zip, enumerate=enumerate)    


@blueprint.route('/about')
def view_about():
    uids, unames, comments = fetch_testimonials(8)
    return render_template('home/about.html', templateName='about', userId=uids, userName=unames, testimonialComment=comments, zip=zip)


@blueprint.route('/magazine/<page_number>', methods=['GET', 'POST'])
def view_magazine(page_number):

    print("rendering Test")

    magazine = fetch_magazines(8)
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

    if request.method == 'POST':
        print("success")

    # elif request.method == 'GET':
    #     data = request.data_json()

    #     if 'wirtesuccess' in data.keys():

    return render_template('home/magazine-write.html', templateName='magazine-write', \
        userId=user_id, magazineSeq=magazine_seq, nowDate=datetime.datetime.now(), zip=zip, enumerate=enumerate)


@blueprint.route('/uploads/magazines/<magazine_seq>', methods = ['GET', 'POST'])
def upload_files(magazine_seq):

    if request.method == 'POST':
        f = request.files['image']
      
        path = "./apps/static/image/magazines/" + str(magazine_seq)

        if os.path.exists(path):
            print("before shutil")
            shutil.rmtree(path)
            print("after shutil")
        os.mkdir(path)
        f.save(path + "/" + secure_filename(f.filename))
        print("after save")
        
        return jsonify({"result": "success"})
    return jsonify({"result": "fail"})


@blueprint.route('/uploads/none/magazines/<magazine_seq>', methods = ['GET', 'POST'])
def upload_no_files(magazine_seq):

    if request.method == 'POST':

        print("test")
      
        path = "./apps/static/image/magazines/" 

        if os.path.exists(path + str(magazine_seq)):
            print("before shutil")
            shutil.rmtree(path + str(magazine_seq))
            print("after shutil")
        
        os.mkdir(path + str(magazine_seq))

        shutil.copyfile(path + "noimg.jpg", path + str(magazine_seq) +'/noimg.jpg')
      
        print({"result": "success"})

        return jsonify({"result": "success"})

    return jsonify({"result": "fail"})


@blueprint.route('/contact')
def view_contact():
    return render_template('home/contact.html', templateName='contact')

@blueprint.route('/gallery')
def view_gallery():
    return render_template('home/gallery.html', templateName='gallery')


@blueprint.route('/elements')
def view_elements():
    return render_template('home/elements.html', templateName='elements')

