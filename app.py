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
        keyword_dict = ocr.main() # This is where the magic happens
        invoice_number = keyword_dict['Invoice Number']
        invoice_date = keyword_dict['Invoice Date']
        po_number = keyword_dict['PO Number']
        item = keyword_dict['Item']
        total = keyword_dict['Total']
        price = keyword_dict['Price']
        
        return render_template('template.html',invoice_date=invoice_date,invoice_number=invoice_number,po_number=po_number,item=item, total=total, price=price)
    else:
        return render_template('index.html')



