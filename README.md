# Blanket Web

This project inspired by [blanket](https://github.com/rafaelmardojai/blanket/).

---

## How to Use

### First Run

1. Create database by running `CREATE DATABASE db_blanket_web;`.
2. Switch to the database with `USE db_blanket_web;`.
3. Create tables by running the following queries:

    ```
    CREATE TABLE `categories` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(30) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
    ```

    ```
    CREATE TABLE `sounds` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `title` varchar(100) NOT NULL,
      `audio_path` varchar(100) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
    ```

    ```
    CREATE TABLE `sound_legals` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `author` varchar(50) DEFAULT NULL,
      `license` varchar(50) DEFAULT NULL,
      `id_sound` int(11) NOT NULL,
      PRIMARY KEY (`id`,`id_sound`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
    ```

    ```
    CREATE TABLE `sound_details` (
      `id_sound` int(11) NOT NULL,
      `id_category` int(11) NOT NULL DEFAULT 5,
      PRIMARY KEY (`id_category`,`id_sound`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    ```

4. Create virtual environment.

5. Activate the virtual environment. It depends on your OS and shell emulator, please refer to [this page](https://flask.palletsprojects.com/en/2.0.x/cli/) for better information.

6. Install all requirements by running `pip install -r requirements.txt`.

7. Run the application by using this following commands:

    ```
    set FLASK_APP run.py
    flask run
    ```

8. It should be make a connection in `127.0.0.1:5000`. Open the URL on your browser.

9. Click the "Reset to Default" Navbar to setup the application sounds data.

---

### Non-First Run

1. Activate the virtual environment. It depends on your OS and shell emulator, please refer to [this page](https://flask.palletsprojects.com/en/2.0.x/cli/) for better information.

2. Run the application by using this following commands:

    ```
    set FLASK_APP run.py
    flask run
    ```
