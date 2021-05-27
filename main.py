from read_barcode import ReadBarcode
from flask import Flask, render_template, redirect
# from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import SubmitField
from dotenv import load_dotenv
from PIL import Image
import os
import glob

files = glob.glob('/YOUR/PATH/*')
for f in files:
    os.remove(f)

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

@app.route('/', methods=['POST', 'GET'])
def home():
	form = ImageForm()
	if form.validate_on_submit():
		print("la la la")
		# print(form.file.data.filename)
		filename = photos.save(form.photo.data)
		file_url = photos.url(filename)
		print(file_url)
		# with Image.open(form.file) as im:
		# 	im.rotate(45).show()
	else:
		file_url = None
	return render_template("index.html", form=form, current_year=current_year, file_url=file_url)




if __name__ == "__main__":
    app.run(debug=True)