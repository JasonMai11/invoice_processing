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

        print(request.form.get('plot_choice1'))
        print(request.form.get('plot_choice2'))
        print(request.form.get('plot_choice3'))

        
        # input if user leaves a Note:
        plot_choice1 = request.form.get('plot_choice1')
        plot_choice2 = request.form.get('plot_choice2')
        plot_choice3 = request.form.get('plot_choice3')
        note = request.form.get('note')
        preparer = request.form.get('preparer')
        print(note)

        # extract file from form data
        file = request.files['fileToUpload']
        if file:
            # Save the file
            file.save(os.path.join('./invoice', file.filename))
        
        keyword_dict = ocr.main() # This is where the magic happens
        invoice_number = [keyword_dict['Invoice Number']]
        invoice_date = [keyword_dict['Invoice Date']]
        po_number = keyword_dict['PO Number']
        item = keyword_dict['Item']
        total = keyword_dict['Total']
        price = keyword_dict['Price']
        gl = keyword_dict['GL']

        while len(invoice_date) != len(item):
            invoice_date.append('')
            invoice_number.append('')

        #move file from invoice folder to archive folder
        os.rename('./invoice/' + file.filename, './archive/' + file.filename)

        return render_template('template.html', plot_choice1=plot_choice1, plot_choice3=plot_choice3, preparer=preparer,invoice_date=invoice_date,invoice_number=invoice_number,po_number=po_number,item=item, total=total, price=price, gl=gl, note=note, zip=zip)
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




'''
# Creating routes for the web application

@app.route('/run')
def index():
    """Homepage with links to view each table."""
    tables = ['Employees', 'Certifications', 'EmployeeCertifications', 'ClinicalEducation', 'EmployeeHealth']
    return render_template_string("""
    <h1>Welcome to the Employee Database Website</h1>
    <p>Select a table to view its contents:</p>
    <ul>
    {% for table in tables %}
        <li><a href="/view/{{ table }}">{{ table }}</a></li>
    {% endfor %}
    </ul>
    """, tables=tables)

@app.route('/view/<string:table_name>')
def view_table(table_name):
    Display the contents of the selected table.
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return render_template_string("""
    <h1>Contents of {{ table_name }}</h1>
    <table border="1">
        <thead>
            <tr>
            {% for col in columns %}
                <th>{{ col }}</th>
            {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                {% for item in row %}
                <td>{{ item }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <br>
    <a href="/">Back to homepage</a>
    """, table_name=table_name, columns=columns, rows=rows)

# Save the Flask app to a Python file for user download
app_code = """
from flask import Flask, render_template_string, g
import sqlite3

app = Flask(__name__)
DATABASE = 'employee_database.db'

# Database setup and routes from above will be included here

if __name__ == '__main__':
    app.run(debug=True)
"""

with open("/mnt/data/employee_database_app.py", "w") as f:
    f.write(app_code)

"/mnt/data/employee_database_app.py"



"""
'''