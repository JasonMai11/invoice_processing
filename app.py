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
        
        # input if user leaves a Note:
        note = request.form.get('note')
        print(note)

        # extract file from form data
        file = request.files['fileToUpload']
        if file:
            # Save the file
            file.save(os.path.join('./invoice', file.filename))
        
        keyword_dict = ocr.main() # This is where the magic happens
        invoice_number = keyword_dict['Invoice Number']
        invoice_date = keyword_dict['Invoice Date']
        po_number = keyword_dict['PO Number']
        item = keyword_dict['Item']
        total = keyword_dict['Total']
        price = keyword_dict['Price']
        gl = keyword_dict['GL']
        #move file from invoice folder to archive folder
        os.rename('./invoice/' + file.filename, './archive/' + file.filename)

        return render_template('template.html',invoice_date=invoice_date,invoice_number=invoice_number,po_number=po_number,item=item, total=total, price=price, gl=gl, note=note, zip=zip)
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




# Uploading Manual Form Code

# I had two approaches, the current approach I went with is 
# to divide all rows with a row incrementer

# My approach:
# make them into arrays
# i.e. date array = [2023-08-20, 2023-07-23]
#       price array = [...]

@app.route('/manualUpload', methods=['GET', 'POST'])
def manual_upload():
    if request.method == 'POST':
        rows = request.form.to_dict(flat=False)

        # Initialize separate lists for each field.
        invoice_date = []
        invoice_number = []
        item = []
        gl = []
        price = []
        total = 0

        # input: if user leaves a Note:
        note = request.form.get('note')
        # input: gets the preparer
        preparer = request.form.get('preparer')

        # Get all unique row indices.
        indices = len([key for key in rows.keys() if 'date' in key])

        # Iterate over row indices and append to corresponding list.
        for i in range(indices):
            invoice_date.append(rows['row['+str(i)+'][date]'][0])
            invoice_number.append(rows['row['+str(i)+'][number]'][0])
            item.append(rows['row['+str(i)+'][memo]'][0])
            gl.append(rows['row['+str(i)+'][glCode]'][0])
            price.append('$' + rows['row['+str(i)+'][priceAmount]'][0])
            total += float(rows['row['+str(i)+'][priceAmount]'][0])

 
        return render_template('template.html', preparer=preparer, note=note, invoice_date=invoice_date, invoice_number=invoice_number, item=item, gl=gl, price=price, total=total, zip=zip)
    else:
        return render_template('index.html')



"""
@app.route('/manualUpload', methods=['GET', 'POST'])
def manual_upload():
    if request.method == 'POST':
        rows = request.form.to_dict(flat=False)
        row_data = []

        # Iterate over row data to convert to list of tuples.
        for i in range(len(rows['row[0][date]'])): # Use any row[] index here.
            date = rows['row['+str(i)+'][date]'][0]
            number = rows['row['+str(i)+'][number]'][0]
            memo = rows['row['+str(i)+'][memo]'][0]
            glCode = rows['row['+str(i)+'][glCode]'][0]
            priceAmount = rows['row['+str(i)+'][priceAmount]'][0]
            row_data.append((date, number, memo, glCode, priceAmount))
        print(row_data)
        return render_template('template.html')
    else:
        return render_template('index.html')
"""