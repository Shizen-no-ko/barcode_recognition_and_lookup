from read_barcode import ReadBarcode
from flask import Flask, render_template, redirect, url_for, flash
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
import shutil

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





now = datetime.now()
current_year = now.strftime("%Y")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

reader = ReadBarcode()

class ImageForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])

def get_image_file():
	# returns first image file in uploads folder (should be only one there)
	file = os.listdir(os.path.join(basedir, 'uploads'))[0]
	return os.path.join(basedir, 'uploads', file)

def delete_image_file():
	# clears upload folder
	# files = glob.glob(os.path.join(basedir, 'uploads'))
	folder = os.path.join(basedir, 'uploads')
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))
	# for f in files:
	# 	os.remove(f)


@app.route('/', methods=['POST', 'GET'])
def home():
	form = ImageForm()
	if form.validate_on_submit():
		photos.save(form.photo.data)
		# filename = photos.save(form.photo.data)
		# file_url = photos.url(filename)
		return redirect(url_for("image_stage"))
	# else:
	# 	file_url = None
	return render_template("index.html", form=form, current_year=current_year)
# , file_url=file_url

@app.route('/selected-image', methods=['POST', 'GET'])
def image_stage():
	image = Image.open(get_image_file())
	data = io.BytesIO()
	image.save(data, "JPEG")
	encoded_img_data = base64.b64encode(data.getvalue())
	return render_template("image_stage.html", img_data=encoded_img_data.decode('utf-8'))

@app.route('/scan-image', methods=['POST', 'GET'])
def scan_image():
	# reader = ReadBarcode()
	barcode_number = reader.scan_image(get_image_file())
	if barcode_number:
		result = reader.get_product_details(barcode_number)
		if result:
			return redirect(url_for("results"))
		else:
			flash("Sorry, no results found for this barcode.")
			return redirect(url_for("home"))
	else:
		# print(barcode_number)
		# print("Barcode on image not readable")
		flash("Barcode on image not readable.")
		flash("Try again.")
		delete_image_file()
		return redirect(url_for("home"))
	# return redirect(url_for('home'))

@app.route('/results', methods=['POST', 'GET'])
def results():
	return render_template("results.html", results=reader.results)






if __name__ == "__main__":
    app.run(debug=True)