import os
import base64
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_uploads import UploadSet, configure_uploads, ALL
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/exported'

# Configure file uploads
photos = UploadSet('photos', ALL)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return redirect(request.url)

    file = request.files['photo']
    if file.filename == '':
        return redirect(request.url)

    if file and photos.file_allowed(file, file.filename):
        filename = photos.save(file)
        return redirect(url_for('uploaded_file', filename=filename))

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded.html', filename=filename)

@app.route('/image/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/export', methods=['POST'])
def export():
    img_data = request.form['imgData']
    img_type = request.form['imgType']
    img_name = request.form['imgName']

    # Decode and save the image
    img_data = img_data.split(',')[1]
    img_data = base64.b64decode(img_data)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img_name))

    with open(img_path, 'wb') as f:
        f.write(img_data)

    return 'Image saved', 200

if __name__ == '__main__':
    app.run(debug=True)
