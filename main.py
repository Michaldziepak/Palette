from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import regexp
import re
from PIL import Image
from io import BytesIO
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class MyForm(FlaskForm):
    image = FileField("",[regexp(u'^[^/]\.jpg$')])
    submit = SubmitField('Submit')
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

@app.route("/",methods=["GET", "POST"])
def home():
    colorlist=[]
    form=MyForm()
    image_data=""
    if request.method == 'POST':
        image_data = form.image.data
        image_data = image_data.read()
        image = Image.open(BytesIO(image_data))
        # Convert the image to RGB (if it's not already in RGB mode)
        image = image.convert('RGB')

        # Convert the image to a numpy array
        image_array = np.array(image)

        # Reshape the array to a 2D array of pixels
        pixels = image_array.reshape((-1, 3))

        # Compute the histogram of colors
        histogram, _ = np.histogramdd(pixels, bins=(256, 256, 256), range=[(0, 255), (0, 255), (0, 255)])

        # Get the indices of the most frequent colors
        indices = np.unravel_index(np.argsort(histogram.ravel())[-5:], histogram.shape)

        # Get the most frequent colors
        colors = np.array(indices).T

        # Convert the colors to hexadecimal representation
        hex_colors = ['#%02x%02x%02x' % (r, g, b) for r, g, b in colors]

        # Display the extracted color palette

        for color in hex_colors:
            colorlist.append(color)

        return render_template("index.html",form=form,colorlist=colorlist,image_data=image.show)


    return render_template("index.html",form=form,colorlist=colorlist,image_data=image_data)
@app.route("/palette",methods=["GET", "POST"])
def palette():

    return render_template("palette.html")



if __name__ == '__main__':
    app.run(debug=True, port=5002)    