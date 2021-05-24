# How to Use

---

## First Run

1. Create database by running `CREATE DATABASE db_blanket_web`
2. Create tables by running the following queries.

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

3. Install all requirements by running `pip install -r requirements.txt`

4. Activate the virtual environment. Depends on your OS and terminal, if you using GNU/Linux and FISH, simply run `source env/bin/activate.fish`

5. Run the application by using this following commands

    ```
    set FLASK_APP run.py
    flask run
    ```

6. It should be make a connection in `127.0.0.1:5000`. Open the URL on your browser.

7. Click the "Reset to Default" Navbar to setup the application sounds data.

---

## Non-First Run

Simply **skip the 1st, 2nd, and 7th step** on First Run section.
