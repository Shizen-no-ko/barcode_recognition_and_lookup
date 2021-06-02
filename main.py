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
import shutil

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


def delete_image_folder():
	# clear all files from the "uploads folder"
	# construct path to folder
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


@app.route('/', methods=['POST', 'GET'])
def home():
	# resets results in reader class
	reader.results = {}
	# clear image folder
	delete_image_folder()
	# load image form
	form = ImageForm()
	# if photo selected, move on to image stage
	if form.validate_on_submit():
		photos.save(form.photo.data)
		return redirect(url_for("image_stage"))
	# else reload page
	return render_template("index.html", form=form, current_year=current_year)


@app.route('/selected-image', methods=['GET'])
def image_stage():
	# open uploaded image from "uploads" folder
	# and pass to image-stage html
	image = Image.open(get_image_file())
	data = io.BytesIO()
	image.save(data, "JPEG")
	encoded_img_data = base64.b64encode(data.getvalue())
	return render_template("image_stage.html", img_data=encoded_img_data.decode('utf-8'))


@app.route('/scan-image', methods=['POST'])
def scan_image():
	# attempt to retrieve barcode number from image, using API
	barcode_number = reader.scan_image(get_image_file())
	# if barcode number is returned, send to another API
	# to retrieve details
	if barcode_number:
		result = reader.get_product_details(barcode_number)
		# if successful redirect to results page
		if result:
			return redirect(url_for("results"))
		# otherwise flash failure message on homepage
		else:
			flash("Sorry, no results found for this barcode.")
			return redirect(url_for("home"))
	# if no barcode number returned, flash failure message on home page
	else:
		flash("Barcode on image not readable.")
		flash("Please try again.")
		return redirect(url_for("home"))


@app.route('/results', methods=['GET'])
def results():
	return render_template("results.html", results=reader.results)


if __name__ == "__main__":
	app.run(debug=True)
