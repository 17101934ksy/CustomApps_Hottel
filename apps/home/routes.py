from apps.authentication.fetch import fetch_accomodations, fetch_testimonial
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/errors/page-404.html'), 404

    except:
        return render_template('home/errors/page-500.html'), 500


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
    uids, unames, comments = fetch_testimonial(8)

    return render_template('home/index.html', accomodationId=ids, accomodationName=names, accomodationImage=images, \
        accomodationPrice=prices, userId=uids, userName=unames, testimonialComment=comments, zip=zip, enumerate=enumerate) 

@blueprint.route('/accomodation')
def view_accomodation():

    ids, names, images, prices = fetch_accomodations(20)

    return render_template('home/accomodation.html', templateName='accomodation', accomodationId=ids, accomodationName=names, accomodationImage=images, accomodationPrice=prices, \
        zip=zip, enumerate=enumerate)    

@blueprint.route('/about')
def view_about():

    uids, unames, comments = fetch_testimonial(8)

    return render_template('home/about.html', templateName='about', userId=uids, userName=unames, testimonialComment=comments, zip=zip)

@blueprint.route('/blog')
def view_blog():
    
    return render_template('home/blog.html', templateName='blog', blogWriters='', blogDates='', blogViews='', blogComments='', \
        blogHeads='', blogContents='', blogLinks='', blogTags='', pageFocus='', postHeads='',  postLinks='', \
        contentCounts='' , contentSubjects='', zip=zip, enumerat=enumerate)

@blueprint.route('/blog-single')
def view_blog_single():
    return render_template('home/blog-single.html', templateName='blog-single')

@blueprint.route('/contact')
def view_contact():
    return render_template('home/contact.html', templateName='contact')

@blueprint.route('/gallery')
def view_gallery():
    return render_template('home/gallery.html', templateName='gallery')


@blueprint.route('/elements')
def view_elements():
    return render_template('home/elements.html', templateName='elements')