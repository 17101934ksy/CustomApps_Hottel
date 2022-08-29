from apps.authentication.fetch import fetch_accomodations, fetch_testimonials, fetch_magazines
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound, TemplateAssertionError
import datetime
import math

@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateAssertionError:
        return render_template('errors/page-403.html'), 403


    except TemplateNotFound:
        return render_template('errors/page-404.html'), 404

    except:
        return render_template('errors/page-500.html'), 500


# Helper - Extract current page name from request
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

@blueprint.route('/magazine/<page_number>')
def view_magazine(page_number):

    ids, themas, writers, dates, views, titles, subtitles, contents, links, tags, images = fetch_magazines(8)
    contents_subject = ["여행", "미식", "숙소"]
    contents_thema = [0] * 3
    for thema in themas:
        if thema == contents_subject[0]:
            contents_thema[0] += 1
        elif thema == contents_subject[1]:
            contents_thema[1] += 1
        elif thema == contents_subject[2]:
            contents_thema[2] += 1

    for idx, tag in enumerate(tags):
        tags[idx] = tag.split('#')
          
    return render_template('home/magazine.html', templateName='magazine', blogWriters=writers, blogDates=dates, blogViews=views, blogComments=contents, \
        blogTitles=titles, blogContents=contents, blogLinks=links, blogImages=images, blogTags=tags, blogThemas=themas, pageNumber=page_number, postTitles=titles,  postLinks=links, \
        contentCounts=contents_thema , contentSubjects=contents_subject, nowDate=datetime.datetime.now(), zip=zip, enumerate=enumerate, len=len, ceil=math.ceil, int=int)

@blueprint.route('/magazine-single')
def view_magazine_single():
    return render_template('home/magazine-single.html', templateName='magazine-single')

@blueprint.route('/contact')
def view_contact():
    return render_template('home/contact.html', templateName='contact')

@blueprint.route('/gallery')
def view_gallery():
    return render_template('home/gallery.html', templateName='gallery')


@blueprint.route('/elements')
def view_elements():
    return render_template('home/elements.html', templateName='elements')

