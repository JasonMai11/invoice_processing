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
        gl = keyword_dict['GL']
        #move file from invoice folder to archive folder
        os.rename('./invoice/' + file.filename, './archive/' + file.filename)

        return render_template('template.html',invoice_date=invoice_date,invoice_number=invoice_number,po_number=po_number,item=item, total=total, price=price, gl=gl, zip=zip)
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
    """Display the contents of the selected table."""
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


