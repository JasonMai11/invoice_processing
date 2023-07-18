from flask import Flask, render_template, request, redirect, url_for
import os
import io
import base64
import glob
import ocr as ocr

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # extract file from form data
        file = request.files['fileToUpload']
        if file:
            # Save the file
            file.save(os.path.join('./invoice', file.filename))
        
        # Extract 'plot_choice' values
        plot_choice = request.form.getlist('plot_choice')
        print(plot_choice)
        
        # Handle plot_choice values and file as needed here...
        
        return render_template('template.html')
    else:
        return render_template('index.html')



