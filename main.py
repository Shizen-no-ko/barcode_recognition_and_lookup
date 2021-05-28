from read_barcode import ReadBarcode
from flask import Flask, render_template, redirect, url_for
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from dotenv import load_dotenv
from PIL import Image
import os
import io
import base64
import glob

# for deleting
# files = glob.glob('/YOUR/PATH/*')
# for f in files:
#     os.remove(f)

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

# In flask_uploads.py
# Change
# from werkzeug import secure_filename,FileStorage
# to
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage


reader = ReadBarcode()


now = datetime.now()
current_year = now.strftime("%Y")

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
# Bootstrap(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

class ImageForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])

def get_image_file():
	# returns first image file in uploads folder (should be only one there)
	file = os.listdir(os.path.join(basedir, 'uploads'))[0]
	return os.path.join(basedir, 'uploads', file)

def delete_image_file():
	# clears upload folder
	files = glob.glob(os.path.join(basedir, 'uploads'))
	for f in files:
		os.remove(f)


@app.route('/', methods=['POST', 'GET'])
def home():
	form = ImageForm()
	if form.validate_on_submit():
		filename = photos.save(form.photo.data)
		file_url = photos.url(filename)
		return redirect(url_for("image_stage"))
	else:
		file_url = None
	return render_template("index.html", form=form, current_year=current_year, file_url=file_url)


@app.route('/selected_image', methods=['POST', 'GET'])
def image_stage():
	image = Image.open(get_image_file())
	# image = Image.open("uploads/Image_Palette_Finder_1.jpg")
	data = io.BytesIO()
	image.save(data, "JPEG")
	encoded_img_data = base64.b64encode(data.getvalue())
	return render_template("image_stage.html", img_data=encoded_img_data.decode('utf-8'))





if __name__ == "__main__":
    app.run(debug=True)