from os import urandom, path, remove
from collections import defaultdict
from random import choice
from string import digits
from flask import render_template, redirect, request, url_for, flash, session
from werkzeug.utils import secure_filename
from app import app, mysql

app.secret_key = urandom(32)
sound_dict = {}
categories = {}
messages = {
    'upload_success' : "Upload Success!",
    'upload_failed' : "Upload Failed!",
    'delete_success' : "Delete Success!",
    'delete_failed' : "Delete Failed!",
    'update_success' : "Update Success!",
    'update_failed' : "Update Failed!",
    'add_category_success' : "Add Category Success!",
    'add_category_failed' : "Add Category Failed!",
    'reset_success' : "Reset Success!",
    'reset_failed' : "Reset Failed!"
}

"""

https://stackoverflow.com/questions/35570958/how-to-remove-session-variable-in-a-template-after-its-job-is-done-in-django

"""

def get_db_data():
    """ Get necessary data from the database """
    """ Expected Query Output
      0      1      2      3         4            5             6             7
    +----+--------+----+-------+------------+---------------+---------+
    | id | name   | id | title | audio_path | author        | license |
    +----+--------+----+-------+------------+---------------+---------+
    |  1 | Nature |  7 | Birds | birds.wav  | kvgarlic      | CC0     |
    |  2 | Travel | 11 | Boat  | boat.wav   | Falcet        | CC0     |
    |  2 | Travel | 10 | City  | city.wav   | gezortenplotz | CC BY   |
    +----+--------+----+-------+------------+---------------+---------+
    """
    """ Restructure:
        category = {
            categoryName1 = [(soundTitle1, soundAudioPath1, soundAuthor1, soundLicense1), (soundTitle2, soundAudioPath2, soundAuthor2, soundLicense2)]
            categoryName2 = [(soundTitle3, soundAudioPath3, soundAuthor3, soundLicense3), (soundTitle4, soundAudioPath4, soundAuthor4, soundLicense4)]
        }
    """

    con = mysql.connection
    cur = con.cursor()
    
    cur.execute("SELECT c.id, c.name,\
                s.id, s.title, s.audio_path,\
                sl.author, sl.license\
                FROM sounds AS s\
                JOIN sound_details AS sd ON (s.id = sd.id_sound)\
                JOIN categories AS c ON (sd.id_category = c.id)\
                JOIN sound_legals AS sl ON (s.id = sl.id_sound)\
                ORDER BY c.id, s.title")
    sound_db_data = cur.fetchall()

    cur.execute("SELECT id, name FROM categories ORDER BY id")
    categories_db_data = cur.fetchall()
    
    cur.close()

    sound_list = [(data[1], data[0], data[2], data[3], data[4], data[5], data[6]) for data in sound_db_data]
    tmp_sound_dict = defaultdict(list)

    # [id_cat, id_sound, title, audio_path]
    for k, v1, v2, v3, v4, v5, v6 in sound_list:
        tmp_sound_dict[k].append((v1, v2, v3, v4, v5, v6))

    global sound_dict
    sound_dict = dict(tmp_sound_dict)

    global categories
    categories = {name: id for id, name in categories_db_data}

    return sound_dict, categories

def get_latest_id_sound():
    id_sound_latest = 1
    
    try:
        con = mysql.connection
        cur = con.cursor()
        cur.execute("SELECT id FROM `sounds`\
                    ORDER BY id DESC LIMIT 1")

        id_sound_latest = cur.fetchall()[0][0]
        cur.close()
    except:
        pass

    return id_sound_latest


@app.route('/')
def index():
    """ Main Page """
 
    sound_dict, categories = get_db_data()

    operation_success = False

    if 'operation_success' in session:
        operation_success = session['operation_success']
        alert_messages = session['alert_messages']
    else:
        alert_messages = False

    return render_template('index.html', sound_dict = sound_dict, categories = categories, operation_success = operation_success, alert_messages = alert_messages)
    

@app.route('/debug-page')
def debug_page():
    if 'debug_session' in session:
        debug_session = session['debug_session']
    else:
        debug_session = False

    try:
        con = mysql.connection
        con.autocommit = False
        cur = con.cursor()

        message = "Yahaloo"

        cur.execute("INSERT INTO `debug_table` (content) VALUES (%s)", (message,))

        con.commit()

    except:
        print("There some error")
        con.rollback()

    finally:
        con.close()

    return render_template('debug-page.html', debug_session = debug_session)


def allowed_file(filename):
    return '.' in filename and\
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'] 

def check_file_exist(filename):
    exist_file_path = path.join(app.config['UPLOAD_FOLDER'], filename)

    if (path.isfile(exist_file_path)):
        name, ext = filename.rsplit('.' ,1)
        name = name + '_' + ''.join([choice(digits) for i in range(4)])
        filename = name + '.' + ext

        return check_file_exist(filename)

    else:
        return filename

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        category = request.form['category']
        id_category = categories[category]
        title = request.form['title']
        file = request.files['file']
        author = request.form['author']
        license = request.form['license']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '' or title == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = check_file_exist(filename)
            
            try:
                con = mysql.connection
                con.autocommit = False
                cur = con.cursor()
                
                cur.execute("INSERT INTO `sounds` (title, audio_path)\
                            VALUES (%s, %s)", (title, filename,))

                id_sound_latest = get_latest_id_sound()
                
                cur.execute("INSERT INTO `sound_legals` (author, license, id_sound)\
                            VALUES (%s, %s, %s)", (author, license, id_sound_latest,))

                cur.execute("INSERT INTO `sound_details`\
                            VALUES (%s, %s)", (id_sound_latest, id_category,))

                con.commit()
                file.save(path.join(app.config['UPLOAD_FOLDER'], filename))

                session['operation_success'] = True
                session['alert_messages'] = messages['upload_success']

            except Exception as e:
                con.rollback()
                session['alert_messages'] = messages['upload_failed']
            
            finally:
                con.close()
            
            # session['debug_session'] = True

            return redirect(url_for('index'))

    session['alert_messages'] = messages['upload_failed']

    return redirect(url_for('index'))


@app.route('/delete/<string:id_sound>', methods=["GET", "POST"])
def delete(id_sound):
    if request.method=='GET':
        try:
            con = mysql.connection
            con.autocommit = False
            cur = con.cursor()

            cur.execute("SELECT audio_path FROM `sounds` WHERE id = %s", (id_sound,))
            filename = cur.fetchall()[0][0]

            cur.execute("DELETE FROM `sounds` WHERE id=%s", (id_sound,))
            cur.execute("DELETE FROM `sound_legals` WHERE id_sound = %s", (id_sound,))
            cur.execute("DELETE FROM `sound_details` WHERE id_sound = %s", (id_sound,))

            con.commit()
            remove(path.join(app.config['UPLOAD_FOLDER'], filename))

            session['operation_success'] = True
            session['alert_messages'] = messages['delete_success']

        except:
            con.rollback()
            session['alert_messages'] = messages['delete_failed']

        finally:
            con.close()
    
    return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        id_sound = request.form['id']
        category = request.form['category']
        id_category = categories[category]
        title = request.form['title']
        file = request.files['file']
        author = request.form['author']
        license = request.form['license']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '' or title == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = check_file_exist(filename)
            
            con = mysql.connection
            con.autocommit = False
            cur = con.cursor()

            cur.execute("SELECT audio_path FROM sounds WHERE id = %s", (id_sound,))
            old_filename = cur.fetchall()[0][0]

            try:
                cur.execute("UPDATE `sounds` SET\
                            title = %s, audio_path = %s\
                            WHERE id = %s", (title, filename, id_sound,))
                
                cur.execute("UPDATE `sound_legals` SET\
                            author = %s, license = %s\
                            WHERE id_sound = %s", (author, license, id_sound,))

                cur.execute("UPDATE `sound_details` SET\
                            id_category = %s \
                            WHERE id_sound = %s", (id_category, id_sound,))

                con.commit()
                file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
                remove(path.join(app.config['UPLOAD_FOLDER'], old_filename))

                session['operation_success'] = True
                session['alert_messages'] = messages['update_success']

            except Exception as e:
                con.rollback()
                session['alert_messages'] = messages['update_failed']
            
            finally:
                con.close()

            return redirect(url_for('index'))

    session['alert_messages'] = messages['update_failed']

    return redirect(url_for('index'))


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        new_category = request.form['new-category']

        try:
            con = mysql.connection
            con.autocommit = False
            cur = con.cursor()

            cur.execute("INSERT INTO `categories` (name) VALUES (%s)", (new_category,))

            con.commit()

            session['operation_success'] = True
            session['alert_messages'] = messages['add_category_success']

        except:
            con.rollback()
            session['alert_messages'] = messages['add_category_failed']

        finally:
            con.close()

    return redirect(url_for('index'))


def delete_non_default_sound():
    for cat in sound_dict:
        for data in sound_dict[cat]:
            if data[0] >= 5:
                remove(path.join(app.config['UPLOAD_FOLDER'], data[3]))

@app.route('/default-db')
def generate_default_db():
    categories = [
        (1, 'Nature'),
        (2, 'Travel'),
        (3, 'Interiors'),
        (4, 'Noise'),
        (5, 'Custom')
    ]

    sound_data = [
        #   0           1            2            3             4
        # (s.title, s.audio_path, sl.author, sl.license, sd.id_category)
        ('Birds', 'birds.wav', 'kvgarlic', 'CC0', 1),
        ('Crickets', 'night-crickets.wav', 'Lisa Redfern', 'Public Domain', 1),
        ('Rain', 'rain-ambience.wav', 'alex36917', 'CC BY', 1),
        ('Storm', 'infinite-storm.wav', 'Digifish music', 'CC BY', 1),
        ('Stream', 'stream.wav', 'gluckose', 'CC0', 1),
        ('Waves', 'ocean-waves.wav', 'Luftrum', 'CC BY', 1),
        ('Wind', 'wind.wav', 'Stilgar', 'Public Domain', 1),
        ('Boat', 'boat.wav', 'Falcet', 'CC0', 2),
        ('City', 'city.wav', 'gezortenplotz', 'CC BY', 2),
        ('Coffee Shop', 'coffee-shop.wav', 'stephan', 'Public Domain', 3),
        ('Fireplace', 'fireplace.wav', 'ezwa', 'Public Domain', 3),
        ('Pink noise', 'pink-noise.ogg', 'Omegatron', 'CC BY-SA', 4),
        ('White noise', 'white-noise.ogg', 'Jorge Stolfi', 'CC BY-SA', 4)
    ]

    try:
        con = mysql.connection
        con.autocommit = False
        cur = con.cursor()

        cur.execute("TRUNCATE `categories`")
        cur.execute("TRUNCATE `sounds`")
        cur.execute("TRUNCATE `sound_legals`")
        cur.execute("TRUNCATE `sound_details`")

        for cat in categories:
            cur.execute("INSERT INTO `categories`\
                        VALUES (%s, %s)", (cat[0], cat[1],))
    
        for data in sound_data:
            cur.execute("INSERT INTO `sounds` (title, audio_path)\
                        VALUES (%s, %s)", (data[0], data[1],))

            id_sound_latest = get_latest_id_sound()

            cur.execute("INSERT INTO `sound_legals` (author, license, id_sound)\
                VALUES (%s, %s, %s)", (data[2], data[3], id_sound_latest,))

            cur.execute("INSERT INTO `sound_details`\
                VALUES (%s, %s)", (id_sound_latest, data[4],))
            
        con.commit()
        delete_non_default_sound()

        session['operation_success'] = True
        session['alert_messages'] = messages['reset_success']

    except Exception as e:
        con.rollback()
        session['alert_messages'] = messages['reset_failed']

    finally:
        con.close()

    return redirect(url_for('index'))
