import json
import os
import re

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from auth import requires_auth

# the all-important app variable:
application = Flask(__name__)


@application.route('/')
def home():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    about_path = os.path.join(application.static_folder, 'db/about.json')

    db = json.loads(open(db_path, 'r').read())
    for section in db:
        for im in section['images']:
            im['offset'] = (100 - int(im['display_width'])) / 2

    about = json.loads(open(about_path, 'r').read())['text']
    return render_template(
        'index.html',
        links=db,
        about=about
    )


@application.route('/admin/', methods=['GET', 'POST'])
@requires_auth
def sections():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':  # Delete section
        section_id = request.form.get('section_id')

        section = [section for section in db if section['id'] == section_id][0]
        for image in section['images']:
            delete_image_file(image['url'])
        db.remove(section)

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return jsonify({'success': True})
    else:
        return render_template('sections.html', db=db)


@application.route('/new_section/', methods=['GET', 'POST'])
@requires_auth
def new_section():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        section_name = request.form.get('section')
        section_id = re.sub('[^A-Za-z0-9]+', '_', section_name).lower()
        section_dict = {'name': section_name, 'id': section_id, 'text': '', 'images': []}
        db.append(section_dict)
        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        return render_template('new_section.html')


@application.route('/edit_section/<string:section_id>/', methods=['GET', 'POST'])
@requires_auth
def edit_section(section_id):
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    if request.method == 'POST':
        section_name = request.form.get('name')
        section_id = re.sub('[^A-Za-z0-9]+', '_', section_name).lower()
        section_text = request.form.get('text')

        section['name'] = section_name
        section['id'] = section_id
        section['text'] = section_text

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        return render_template('edit_section.html', section=section)


@application.route('/edit_image/<string:section_id>/<int:image_id>/', methods=['GET', 'POST'])
@requires_auth
def edit_image(section_id, image_id):
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    if request.method == 'POST':
        title = request.form.get('title')
        section_name = request.form.get('section')
        year = request.form.get('year')
        width = request.form.get('width')
        height = request.form.get('height')
        materials = request.form.get('materials')
        container_width = request.form.get('container_width')
        display_width = request.form.get('display_width')
        align = request.form.get('align')

        db_section = [s for s in db if s['id'] == section_name][0]

        if db_section != section:
            db_section['images'].append(image)
            section['images'].remove(image)

        image["title"] = title
        image["year"] = year
        image["width"] = width
        image["height"] = height
        image["materials"] = materials
        image["container_width"] = container_width
        image["display_width"] = display_width
        image["align"] = align

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        sections = [{"name": section["name"], "id": section['id']} for section in db]
        return render_template(
            'edit_image.html',
            image=image,
            section=section['id'],
            sections=sections
        )


@application.route('/edit_image/', methods=['POST'])
@requires_auth
def delete_image():
    section_id = request.form.get('section_id')
    image_id = int(request.form.get('image_id'))

    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    filename = image['url']

    section['images'].remove(image)
    delete_image_file(filename)

    with open(db_path, 'w') as db_write:
        db_write.write(json.dumps(db))

    return jsonify({'success': True})


@application.route('/upload/', methods=['GET', 'POST'])
@application.route('/upload/<string:section_id>/', methods=['GET', 'POST'])
@requires_auth
def upload(section_id=None):
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        section = request.form.get('section')

        image_ids = []
        for s in db:
            image_ids += [image['id'] for image in s['images']]
        image_id = max(image_ids + [0]) + 1

        db_section = [s for s in db if s['id'] == section][0]

        title = request.form.get('title')
        year = request.form.get('year')
        width = request.form.get('width')
        height = request.form.get('height')
        materials = request.form.get('materials')
        container_width = request.form.get('container_width')
        display_width = request.form.get('display_width')
        align = request.form.get('align')

        image_file = request.files.get('file')
        file_extension = image_file.filename.split('.')[-1]
        upload_folder = os.path.join(application.static_folder, 'images/uploads')
        filename = secure_filename(str(image_id) + '.' + file_extension)
        image_file.save(os.path.join(upload_folder, filename))

        image_dict = {
            "id": image_id,
            "url": filename,
            "title": title,
            "year": year,
            "width": width,
            "height": height,
            "materials": materials,
            "container_width": container_width,
            "display_width": display_width,
            "align": align,
          }

        db_section['images'].append(image_dict)
        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        sections = {section['name']: section['id'] for section in db}
        return render_template('upload.html', sections=sections, section=section_id)


@application.route('/new_home_image/', methods=['GET', 'POST'])
@requires_auth
def new_home_image():
    if request.method == 'POST':
        image_file = request.files.get('file')
        upload_folder = os.path.join(application.static_folder, 'images')
        filename = "home.jpg"
        image_file.save(os.path.join(upload_folder, filename))

        return redirect(url_for('sections'))
    else:
        return render_template('upload_file.html', form_label='New Home Image (must be jpg)')


@application.route('/new_cv/', methods=['GET', 'POST'])
@requires_auth
def new_cv():
    if request.method == 'POST':
        cv_file = request.files.get('file')
        upload_folder = os.path.join(application.static_folder, 'pdf')
        filename = "CV.pdf"
        cv_file.save(os.path.join(upload_folder, filename))

        return redirect(url_for('sections'))
    else:
        return render_template('upload_file.html', form_label='New CV (must be pdf)')


@application.route('/cv')
def cv():
    return application.send_static_file('pdf/CV.pdf')


@application.route('/about/', methods=['GET', 'POST'])
@requires_auth
def about():
    about_path = os.path.join(application.static_folder, 'db/about.json')
    about_json = json.loads(open(about_path, 'r').read())
    if request.method == 'POST':
        about_txt = request.form.get('text')
        about_json['text'] = about_txt
        with open(about_path, 'w') as db_write:
            db_write.write(json.dumps(about_json))

        return redirect(url_for('sections'))
    else:
        return render_template('about.html', about_txt=about_json['text'])


@application.route('/shift_section_position', methods=['POST'])
def shift_section_position():
    section_id = request.form.get('section_id')
    shift = int(request.form.get('shift'))

    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())

    section = [s for s in db if s['id'] == section_id][0]
    section_index = db.index(section)

    if section_index == 0 and shift < 0:  # can't shift up if at top
        return jsonify({'success': False})
    if section_index == len(db) - 1 and shift > 0:  # Can't shift down if at bottom
        return jsonify({'success': False})

    db[section_index], db[section_index + shift] = db[section_index + shift], db[section_index]

    with open(db_path, 'w') as db_write:
        db_write.write(json.dumps(db))

    return jsonify({'success': True})


@application.route('/shift_image_position', methods=['POST'])
def shift_image_position():
    section_id = request.form.get('section_id')
    image_id = int(request.form.get('image_id'))
    shift = int(request.form.get('shift'))

    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())

    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    image_index = section['images'].index(image)

    if image_index == 0 and shift < 0:  # can't shift up if at top
        return jsonify({'success': False})
    if image_index == len(section['images']) - 1 and shift > 0:  # Can't shift down if at bottom
        return jsonify({'success': False})

    section['images'][image_index], section['images'][image_index + shift] = section['images'][image_index + shift], section['images'][image_index]

    with open(db_path, 'w') as db_write:
        db_write.write(json.dumps(db))

    return jsonify({'success': True})


def delete_image_file(filename):
    upload_folder = os.path.join(application.static_folder, 'images/uploads')
    os.remove(os.path.join(upload_folder, filename))


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=800)
