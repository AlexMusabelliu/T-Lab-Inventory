from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ashburn@20148'
app.config['MYSQL_DATABASE_DB'] = 'inventory'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()

@app.route('/query', methods=['GET', 'POST'])
def query():
    return render_template('query.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        tool = request.form['tool']
        print(tool)
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

        cursor.execute("INSERT INTO stuff (name, box_number,year_of_acquisition, quantity, quantity_type,cost,owner,manufacturer_link, equipment_supply, link_to_image, link_to_video, link_to_acquisition_form, course ) VALUES ( 'tool', '1','2019','10','dozens','400','LAB','manufacturer.link.com','EQUIPMENT','image.link.com','video.link.com','acquisitionform.link.com','ENG' );")
        connection.commit()

    return render_template('add.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    print('setting')
    cursor.execute("SHOW TABLES LIKE 'stuff'")
    result = cursor.fetchone()
    print(result)
    if result is None:
        print('making table')
        cursor.execute("CREATE TABLE stuff (id INT unsigned NOT NULL AUTO_INCREMENT, name VARCHAR(150) NOT NULL, box_number VARCHAR(150) NOT NULL, year_of_acquisition VARCHAR(150) NOT NULL, quantity VARCHAR(150) NOT NULL, quantity_type VARCHAR(150) NOT NULL, cost VARCHAR(150) NOT NULL,  owner VARCHAR (150) NOT NULL, manufacturer_link VARCHAR(500) NOT NULL, equipment_supply VARCHAR(150) NOT NULL, link_to_image VARCHAR(500) NOT NULL, link_to_video VARCHAR(500) NOT NULL, link_to_acquisition_form VARCHAR(500) NOT NULL, course VARCHAR(150) NOT NULL, PRIMARY KEY (id) );")
        connection.commit()
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()
