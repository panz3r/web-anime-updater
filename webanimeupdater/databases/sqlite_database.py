import sqlite3 as sqlite

from webanimeupdater.commons import logger as log


class SQLiteDb:
    DB_NAME = 'test.db'

    def __init__(self, database_file):
        log.debug("Will use DB at %s" % (database_file,))
        self.DB_NAME = database_file
        with sqlite.connect(self.DB_NAME) as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Users("
                        "id INTEGER PRIMARY KEY, "
                        "username TEXT, "
                        "password TEXT, "
                        "UNIQUE(username)"
                        ")")

            cur.execute("CREATE TABLE IF NOT EXISTS Anime("
                        "id INTEGER PRIMARY KEY, "
                        "title TEXT, "
                        "url TEXT, "
                        "poster_url TEXT, "
                        "UNIQUE(url)"
                        ")")

            cur.execute("CREATE TABLE IF NOT EXISTS User_Anime("
                        "user_id INTEGER, "
                        "series_id INTEGER, "
                        "UNIQUE(user_id, series_id), "
                        "FOREIGN KEY(user_id) REFERENCES Users(id), "
                        "FOREIGN KEY(series_id) REFERENCES Anime(id)"
                        ")")

            cur.execute("CREATE TABLE IF NOT EXISTS Episode("
                        "id INTEGER PRIMARY KEY, "
                        "series_id INTEGER, "
                        "episode_num INTEGER, "
                        "title TEXT, "
                        "provider TEXT, "
                        "url TEXT, "
                        "UNIQUE(series_id, episode_num), "
                        "FOREIGN KEY(series_id) REFERENCES Anime(id)"
                        ")")

            cur.execute("CREATE TABLE IF NOT EXISTS User_Settings("
                        "user_id INTEGER, "
                        "service_name TEXT, "
                        "settings_id INTEGER, "
                        "UNIQUE(user_id, service_name), "
                        "FOREIGN KEY(user_id) REFERENCES Users(id) "
                        ")")

            cur.execute("CREATE TABLE IF NOT EXISTS Telegram_Settings("
                        "settings_id INTEGER PRIMARY KEY, "
                        "api_key TEXT, "
                        "chat_id TEXT "
                        ")")

    def find_user(self, username):
        with sqlite.connect(self.DB_NAME) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Users WHERE username = ?", (username,))

            data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(data) > 0:
                return data[0]

    def find(self):
        data = None
        with sqlite.connect(self.DB_NAME) as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Anime ORDER BY title')

            data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

            for d in data:
                cur.execute('SELECT MAX(episode_num) FROM Episode WHERE series_id=?', (d['id'],))
                d['last_episode'] = cur.fetchone()[0] or 0

            log.debug("Data: %s" % str(data))
        return data

    def find_by_id(self, entry_id):
        data = None
        with sqlite.connect(self.DB_NAME) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Anime WHERE id=?", (entry_id,))

            data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
            log.debug("Data: %s" % str(data[0]))
        return data[0]

    def find_subentries(self, entry_id):
        data = None
        with sqlite.connect(self.DB_NAME) as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Episode WHERE series_id=?', (entry_id,))

            data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
            log.debug("Data: %s" % str(data))
        return data

    def insert_anime(self, data, username):
        log.debug('Data to insert: ' + str(data))
        with sqlite.connect(self.DB_NAME) as con:
            c = con.cursor()
            c.execute("SELECT * FROM Anime WHERE title=? AND url=?", (data['title'], data['page_url']))
            anime = c.fetchone()
            log.debug("Anime found: (%s)" % (anime,))

            if anime is None:
                c.execute("INSERT INTO Anime(title, url) VALUES(?, ?)", (data['title'], data['page_url']))
                lid = c.lastrowid
            else:
                lid = anime[0]

            log.debug("The last Id of the inserted row is %s" % lid)

            # Look for user and add Anime to his catalog
            user = self.find_user(username)
            if user is not None:
                c.execute("INSERT INTO User_Anime(user_id, series_id) VALUES(?, ?)", (user['id'], lid))

        return lid

    def insert_episode(self, episode):
        log.info('Adding new episode...')
        log.debug('Episode to add: ' + str(episode))
        with sqlite.connect(self.DB_NAME) as con:
            c = con.cursor()

            c.execute("SELECT id FROM Anime WHERE title LIKE ?", (episode.series,))
            series_id = c.fetchone()[0]

            log.debug("SeriesId for '%s' is: %s" % (episode.series, series_id))

            if series_id is not None:
                c.execute("INSERT OR IGNORE INTO Episode(series_id, episode_num, provider, url) VALUES(?, ?, ?, ?)",
                          (series_id, episode.title, episode.provider, episode.link))
                lid = c.lastrowid
                log.debug("The last episode Id of the inserted row is %s" % lid)
                if lid > 0:
                    log.info("New episode found for series '%s'" % episode.series)
                    return True
            else:
                log.warn("Anime '%s' not found" % episode.series)

        log.info("Episode isn't new. Skipping add")
        return False
