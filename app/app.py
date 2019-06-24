import json
import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from auth import requires_auth

# the all-important app variable:
application = Flask(__name__)


@application.route('/')
def home():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    return render_template(
        'index.html',
        links=db
    )


@application.route('/sections', methods=['GET', 'POST'])
@requires_auth
def sections():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':  # Delete section
        section_id = request.form.get('section_id')
        section = [section for section in db if section['id'] == section_id][0]
        db.remove(section)

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return jsonify({'success': True})
    else:
        return render_template('sections.html', db=db)


@application.route('/new_section', methods=['GET', 'POST'])
@requires_auth
def new_section():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        section_name = request.form.get('section')
        section_id = section_name.replace(' ', '_').lower()
        section_dict = {'name': section_name, 'id': section_id, 'images': []}
        db.append(section_dict)
        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('home'))
    else:
        return render_template('new_section.html')


@application.route('/edit_image/<string:section_id>/<int:image_id>/', methods=['GET', 'POST'])
@requires_auth
def edit_image(section_id, image_id):
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        width = request.form.get('width')
        height = request.form.get('height')
        materials = request.form.get('materials')

        image["title"] =  title
        image["year"] = year
        image["width"] = width
        image["height"] = height
        image["materials"] = materials

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        sections = [section['name'] for section in db]
        return render_template(
            'edit_image.html',
            image=image,
            section=section['name'],
            sections=sections
        )


@application.route('/upload', methods=['GET', 'POST'])
@requires_auth
def upload():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        section = request.form.get('section')
        images = []
        for section in db:
            images += section['images']
        image_id = max(image['id'] for image in images) + 1

        db_section = [s for s in db if s['name'] == section][0]

        title = request.form.get('title')
        year = request.form.get('year')
        width = request.form.get('width')
        height = request.form.get('height')
        materials = request.form.get('materials')

        image_file = request.files.get('file')
        upload_folder = os.path.join(application.static_folder, 'images/uploads')
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(upload_folder, filename))

        image_dict = {
            "id": image_id,
            "url": filename,
            "title": title,
            "year": year,
            "width": width,
            "height": height,
            "materials": materials
          }

        db_section['images'].append(image_dict)
        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('home'))
    else:
        sections = [section['name'] for section in db]
        return render_template('upload.html', sections=sections)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=800)
