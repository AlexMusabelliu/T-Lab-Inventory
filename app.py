from flask import Flask, render_template, redirect, request
from flaskext.mysql import MySQL
# import sqlite3, os

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = 'tetris1234' #alex's pwd is tetris1234, pranav's is ProblemTRT?

app.config['MYSQL_DATABASE_DB'] = 'inventory'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()
# os.chdir(os.path.abspath(os.path.dirname(__file__)))
# connection = sqlite3.connect("database.db")
# cursor = connection.cursor()

# This is a test class I created so I can do offline tests with sqlite3
# class request():
#     form = {"tool":"wrench", "box_number":None,"quantity":1337,"year_of_acquisition":3,"cost":None,"owner":None,"course":"misat","equipment_supply":None,
#             "manufacturer_link":None, "link_to_image":None,"link_to_video":None,"quantity_type":"???",'link_to_acquisition_form':None}
#     method = "POST"

class paramDict():
    def __init__(self):
        self.mostParam = {"tool":request.form['tool'],
                        "box_number":request.form['box_number'],
                        "quantity":request.form['quantity'],
                        "year_of_acquisition":request.form['year_of_acquisition'],
                        "cost":request.form['cost'],
                        "owner":request.form.get('owner'),
                        "course":request.form.get('course'),
                        "equipment_supply":request.form.get('equipment_supply'),
                        "manufacturer_link":request.form['manufacturer_link'],
                        "link_to_image":request.form['link_to_image'],
                        "link_to_video":request.form['link_to_video'],
                        "quantity_type":request.form['quantity_type'],
                        'link_to_acquisition_form':request.form['link_to_acquisition_form']}


@app.route('/query', methods=['GET', 'POST'])
def query():
    '''
    Here is an explanation for what is going on in query:
    We have allParam, a dictionary containing all the values from our form, located on query.html and add.html.
    Then, we get the values and keys to make a conditional statement, in the format of:

        [key]='[value]', [key]='[value]', etc.
        e.g. tool='wrench', quantity='3'

    Which is stored in queryParam and then appended to our SQL query, making:

        SELECT * FROM tools WHERE [key]='value'...
        e.g. SELECT * FROM tools WHERE tool='wrench'...

    This gets all rows from tools where our values are matching.
    queryParam ignores entries that are None and entries that are blank, i.e. ''.
    '''
    if request.method == 'POST':
        allParam = paramDict().mostParam
        #Here are the rows where each param = the value given:
        queryParams = " AND ".join([x + "=" + "'" + str(allParam.get(x)) + "'" for x in allParam if allParam.get(x) != None and allParam.get(x) != "''"])
        values = cursor.execute("SELECT * FROM tools WHERE " + queryParams + ";")

        #To view what values has found, you can do this:
        [print(x) for x in values]

    return render_template('query.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    '''
    Here, allParam and queryParam are the same as in the query() function.
    Before we decided whether or not to reject the attempt to add an entry to the database, we make sure it is in the database. This is done as such:
    First, we get all the rows in our table, which we then store in the appropriately named 'allRows' list.
    Then, we create a tuple containing all the values that were given for the object we are adding. All the values are standardized as strings.
    Finally, we created the boolean variable 'idCheck' to store whether or not the parameters specified in add.html are already in our table.
    If they are, we insert and send a success message. Otherwise, we reject the attempt.
    We end by committing all changes to the current database.
    '''
    message = ""
    if request.method == 'POST':
        allParam = paramDict().mostParam

        #im assuming this is all to check if the tool already exists in the database and then create (from here to the connection commit)
        #^ Yes, this is correct. -A



        #create querying parameters
        queryParams = " AND ".join([x + "=" + "'" + str(allParam.get(x)) + "'" for x in allParam if allParam.get(x) != None and allParam.get(x) != "''"])

        allRows = [x for x in cursor.execute("SELECT * FROM tools")]

        assembleTuple = tuple([str(allParam.get(x)) for x in allParam])

        idCheck = assembleTuple not in allRows

        if idCheck:
            cursor.execute("INSERT INTO tools VALUES (" + "?, " * (len(allParam) - 1) + "?)", [str(allParam.get(x)) for x in allParam])
            message = "Success!"
        else:
            message = "<img src = https://web.archive.org/web/20091025230433/http://geocities.com/Athens/Styx/5649/genie.gif>This tool already has an entry!"

        print(message)

        connection.commit()


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
    add()
    query()