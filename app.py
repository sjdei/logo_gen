from weblogo import *
from flask import Flask,render_template, request, send_file
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField 
from io import BytesIO
import numpy as np

class Newform(FlaskForm):
    text = StringField('Please select a download format.')
    submit1 = SubmitField('JPG')
    submit2 = SubmitField('PNG')
    submit3 = SubmitField('SVG')
app = Flask(__name__)
app.secret_key = "shawroot"
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def index():
    form = Newform()
    if request.method=='POST':
        if form.submit1.data:
           print("1")
           return send_file('./static/J.jpg', as_attachment=True)
        elif form.submit2.data:
           print("2")
           return send_file('./static/P.png', as_attachment=True)
           #return "<a href=\"./P.png\" download=\"範例P.png\"></a>"
        elif form.submit3.data:
           print("3")
           return send_file('./static/S.svg', as_attachment=True)
           #return "<a href=\"./S.svg\" download=\"範例S.svg\"></a>"
        else:
            file = request.files['file']
            Input = file.read().decode().split("\n")
            if len(Input[0])==0:
                Input = request.form['Input'].split('\n')
                Input = request.form['Input'].split('\n')
            Input = [i.strip() for i in Input]
            for I in Input:
                if len(Input)>16 or len(I)>16 or (not I.isalpha()) or len(I)!=len(Input[0]):
                    return render_template('index.html')
            gen(Input)
        return render_template('home.html',form=form, image_path='P.png')
    return render_template('index.html')

def toSVG(infile, outfile):
    image = Image.open(infile).convert('RGBA')
    data = image.load()
    width, height = image.size
    out = open(outfile, "w")
    out.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    out.write('<svg id="svg2" xmlns="http://www.w3.org/2000/svg" version="1.1" \
                width="%(x)i" height="%(y)i" viewBox="0 0 %(x)i %(y)i">\n' % \
            {'x': width, 'y': height})
    for y in range(height):
        for x in range(width):
            rgba = data[x, y]
            rgb = '#%02x%02x%02x' % rgba[:3]
            if rgba[3] > 0:
                out.write('<rect width="1" height="1" x="%i" y="%i" fill="%s" \
                    fill-opacity="%.2f" />\n' % (x, y, rgb, rgba[3]/255.0))
    out.write('</svg>\n')
    out.close()

def gen(Input):
    custom_alphabet = 'ACDEFGHIKLMNPQRSTVWY'
    letter_to_index = {letter: index for index, letter in enumerate(custom_alphabet)}
    counts = []
    sequences=['']*len(Input[0])
    for line in Input:
        for i in range(0,len(line)):
            sequences[i]+=line[i]
    # 创建字母到索引的映射
    letter_to_index = {letter: index for index, letter in enumerate(custom_alphabet)}

    # 创建计数数组
    counts = np.zeros((len(sequences), len(custom_alphabet)))
    for i, sequence in enumerate(sequences):
        for letter in sequence:
            if letter in custom_alphabet:
                index = letter_to_index[letter]
                counts[i, index] += 1
    #logodata = LogoData.from_seqs(seqs)
    #logodata.alphabet='ACDEFGHIJKLMNOPQRSTUVWXYZ'
    logodata = LogoData.from_counts(custom_alphabet, counts)
    logooptions = LogoOptions()
    logooptions.scale_width=False
    logoformat = LogoFormat(logodata, logooptions)
    logoformat.color_scheme = chemistry 
    jpg=jpeg_formatter(logodata, logoformat)
    png=png_print_formatter(logodata, logoformat)
    image = Image.open(BytesIO(png))
    image.save("./static/J.jpg", "JPEG")
    image.save("./static/P.png", "PNG")
    #image.save("./static/S.svg", "SVG")
    toSVG('./static/J.jpg', './static/S.svg')
if __name__=='__main__':
    app.run(debug=True)