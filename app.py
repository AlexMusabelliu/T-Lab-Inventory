from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ProblemTRT?'
app.config['MYSQL_DATABASE_DB'] = 'inventory'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        tool = request.form['tool']
        box_number = request.form['box_number']
        quantity = request.form['quantity']
        quantity_type = request.form['quantity_type']
        year_of_acquisition = request.form['year_of_acquisition']
        cost = request.form['cost']
        owner = request.form.get('owner')
        course = request.form.get('course')
        equipment_supply = request.form.get('equipment_supply')
        manufacturer_link = request.form['manufacturer_link']
        link_to_image = request.form['link_to_image']
        link_to_video = request.form['link_to_video']
        link_to_acquisition_form = request.form['link_to_acquisition_form']
        values = " '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' ".format(
            tool, box_number, year_of_acquisition, quantity, quantity_type, cost, "owner", manufacturer_link, "equipment_supply", link_to_image, link_to_video, link_to_acquisition_form, course)

    return render_template('query.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    message = ""
    if request.method == 'POST':
        tool = request.form['tool']
        box_number = request.form['box_number']
        quantity = request.form['quantity']
        quantity_type = request.form['quantity_type']
        year_of_acquisition = request.form['year_of_acquisition']
        cost = request.form['cost']
        owner = request.form.get('owner')
        course = request.form.get('course')
        equipment_supply = request.form.get('equipment_supply')
        manufacturer_link = request.form['manufacturer_link']
        link_to_image = request.form['link_to_image']
        link_to_video = request.form['link_to_video']
        link_to_acquisition_form = request.form['link_to_acquisition_form']
        values = " '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' ".format(
            tool, box_number, year_of_acquisition, quantity, quantity_type, cost, owner, manufacturer_link, equipment_supply, link_to_image, link_to_video, link_to_acquisition_form, course)

        cursor.execute("INSERT INTO tools (name, box_number, year_of_acquisition, quantity, quantity_type, cost, owner, manufacturer_link, equipment_supply, link_to_image, link_to_video, link_to_acquisition_form, course) VALUES({});".format(values))
        connection.commit()
        message = "Success"

    return render_template('add.html', message=message)


@app.route('/', methods=['GET', 'POST'])
def home():
    setup()
    return render_template('home.html')


def setup():
    cursor.execute("USE INVENTORY;")
    cursor.execute("SHOW TABLES LIKE 'tools';")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("CREATE TABLE tools (id INT unsigned NOT NULL AUTO_INCREMENT, name VARCHAR(150) NOT NULL, box_number VARCHAR(150) NOT NULL, year_of_acquisition VARCHAR(150) NOT NULL, quantity VARCHAR(150) NOT NULL, quantity_type VARCHAR(150) NOT NULL, cost VARCHAR(150) NOT NULL,  owner VARCHAR (150) NOT NULL, manufacturer_link VARCHAR(500) NOT NULL, equipment_supply VARCHAR(150) NOT NULL, link_to_image VARCHAR(500) NOT NULL, link_to_video VARCHAR(500) NOT NULL, link_to_acquisition_form VARCHAR(500) NOT NULL, course VARCHAR(150) NOT NULL, PRIMARY KEY (id) );")
        connection.commit()
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()
