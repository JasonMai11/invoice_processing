from flask import Flask, render_template, request, redirect, url_for
import os
import io
import base64
import glob
import ocr as ocr
import database as db

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
        #move file from invoice folder to archive folder
        os.rename('./invoice/' + file.filename, './archive/' + file.filename)

        return render_template('template.html',invoice_date=invoice_date,invoice_number=invoice_number,po_number=po_number,item=item, total=total, price=price, zip=zip)
    else:
        return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.form
        db.insert_item_data(data['pname'],data['pid'], data['glcode'])
        return render_template('admin.html', data=data)

    else:
        items = db.get_item_data()
        return render_template('admin.html', items=items)


