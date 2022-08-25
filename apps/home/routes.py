from apps.authentication.models import Accomodations
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound




@blueprint.route('/index')
def index():
    accomodations = Accomodations.query.order_by(Accomodations.accomodationId.desc()).limit(8).all()
    ids, names, images = [], [], []

    for accomodation in accomodations:
        ids.append(accomodation.accomodationId)
        names.append(accomodation.accomodationName)
        images.append(accomodation.accomodationImage)

    return render_template('home/index.html', accomodationId=ids, accomodationName=names, accomodationImage=images, \
        zip=zip, enumerate=enumerate) 

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


@blueprint.route('/accomodation')
def view_accomodation():

    accomodations = Accomodations.query.order_by(Accomodations.accomodationId.desc()).limit(20).all()
    ids, names, images = [], [], []

    for accomodation in accomodations:
        ids.append(accomodation.accomodationId)
        names.append(accomodation.accomodationName)
        images.append(accomodation.accomodationImage)

    return render_template('home/accomodation.html', accomodationId=ids, accomodationName=names, accomodationImage=images, \
        zip=zip, enumerate=enumerate)    
