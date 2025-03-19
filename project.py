import sys
import os
import csv
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        user='test',
        password='password',
        database='cs122a'
    )


def import_data(folderName):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        drop_statements = [
            "DROP TABLE IF EXISTS Reviews",
            "DROP TABLE IF EXISTS Sessions",
            "DROP TABLE IF EXISTS Videos",
            "DROP TABLE IF EXISTS Series",
            "DROP TABLE IF EXISTS Movies",
            "DROP TABLE IF EXISTS Releases",
            "DROP TABLE IF EXISTS Viewers",
            "DROP TABLE IF EXISTS Producers",
            "DROP TABLE IF EXISTS Users"
        ]
        for drop_sql in drop_statements:
            cursor.execute(drop_sql)
        conn.commit()

        create_statements = [
            """
            CREATE TABLE Users (
              uid INTEGER,
              nickname VARCHAR(20),
              email VARCHAR(125),
              street VARCHAR(50),
              city VARCHAR(50),
              state VARCHAR(50),
              zip VARCHAR(50),
              genres TEXT NOT NULL,
              joined_date DATE,
              PRIMARY KEY (uid)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Producers (
              uid INTEGER,
              company VARCHAR(125),
              bio VARCHAR(255),
              PRIMARY KEY (uid),
              FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Viewers (
              uid INTEGER,
              first_name VARCHAR(20),
              last_name VARCHAR(20),
              subscription ENUM('free', 'monthly', 'yearly'),
              PRIMARY KEY (uid),
              FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Releases (
              rid INTEGER,
              producer_uid INTEGER NOT NULL,
              title VARCHAR(20),
              genre VARCHAR(20),
              release_date DATE,
              PRIMARY KEY (rid),
              FOREIGN KEY (producer_uid) REFERENCES Producers(uid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Movies (
              rid INTEGER,
              website_url VARCHAR(255),
              PRIMARY KEY (rid),
              FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Series (
              rid INTEGER,
              introduction TEXT,
              PRIMARY KEY (rid),
              FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Videos (
              ep_num INTEGER NOT NULL,
              rid INTEGER NOT NULL,
              title VARCHAR(20),
              length REAL,
              PRIMARY KEY (ep_num, rid),
              FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Sessions (
              sid INTEGER,
              quality ENUM('480p', '720p', '1080p'),
              device ENUM('mobile', 'desktop'),
              ep_num INTEGER NOT NULL,
              rid INTEGER NOT NULL,
              uid INTEGER NOT NULL,
              initiate_at DATETIME,
              leave_at DATETIME,
              PRIMARY KEY (sid),
              FOREIGN KEY (uid) REFERENCES Viewers(uid) ON DELETE CASCADE,
              FOREIGN KEY (ep_num, rid) REFERENCES Videos(ep_num, rid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """
            CREATE TABLE Reviews (
              rvid INTEGER,
              rating INTEGER,
              body VARCHAR(125),
              uid INTEGER NOT NULL,
              posted_at DATETIME,
              rid INTEGER NOT NULL,
              PRIMARY KEY (rvid),
              FOREIGN KEY (uid) REFERENCES Viewers(uid) ON DELETE CASCADE,
              FOREIGN KEY (rid) REFERENCES Releases(rid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
        ]

        for create_sql in create_statements:
            cursor.execute(create_sql)
        conn.commit()

        mapping = {
            "Users": (
                "users.csv",
                "INSERT INTO Users (uid, email, joined_date, nickname, street, city, state, zip, genres) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            ),
            "Producers": (
                "producers.csv",
                "INSERT INTO Producers (uid, bio, company) VALUES (%s, %s, %s)"
            ),
            "Viewers": (
                "viewers.csv",
                "INSERT INTO Viewers (uid, subscription, first_name, last_name) VALUES (%s, %s, %s, %s)"
            ),
            "Releases": (
                "releases.csv",
                "INSERT INTO Releases (rid, producer_uid, title, genre, release_date) VALUES (%s, %s, %s, %s, %s)"
            ),
            "Movies": (
                "movies.csv",
                "INSERT INTO Movies (rid, website_url) VALUES (%s, %s)"
            ),
            "Series": (
                "series.csv",
                "INSERT INTO Series (rid, introduction) VALUES (%s, %s)"
            ),
            "Videos": (
                "videos.csv",
                "INSERT INTO Videos (rid, ep_num, title, length) VALUES (%s, %s, %s, %s)"
            ),
            "Sessions": (
                "sessions.csv",
                "INSERT INTO Sessions (sid, uid, rid, ep_num, initiate_at, leave_at, quality, device) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            ),
            "Reviews": (
                "reviews.csv",
                "INSERT INTO Reviews (rvid, uid, rid, rating, body, posted_at) VALUES (%s, %s, %s, %s, %s, %s)"
            )
        }

        for table, (csv_file, insert_query) in mapping.items():
            file_path = os.path.join(folderName, csv_file)

            if not os.path.exists(file_path):
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                rows = [tuple(row) for row in reader]

                if rows:
                    cursor.executemany(insert_query, rows)
                    conn.commit()

        print("Success")
    except Exception as e:
        print("Fail")
    finally:
        cursor.close()
        conn.close()


def insertViewer(uid, email, nickname, street, city, state, zip_code, genres, joined_date, first, last, subscription):
    # pass
    # 还没测试

    conn = connect_db()
    cursor = conn.cursor()

    try:
        # insert Users table
        cursor.execute("""
            INSERT INTO Users (uid, email, joined_date, nickname, street, city, state, zip, genres)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (uid, email, joined_date, nickname, street, city, state, zip_code, genres))

        # insert Viewers table
        cursor.execute("""
            INSERT INTO Viewers (uid, subscription, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """, (uid, subscription, first, last))

        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        # print("Fail", err)
        print("Fail")

    finally:
        cursor.close()
        conn.close()


def addGenre(uid, new_genre):
    # pass
    # 还没测试

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT genres FROM Users WHERE uid = %s", (uid,))
        result = cursor.fetchone()

        if result:
            current_genres = result[0]

            # None值处理
            if current_genres is None:
                current_genres_list = []
            else:
                # 分割现有genres并转换为小写
                current_genres_list = [g.strip().lower() for g in current_genres.split(';')]

            # 统一new_genre格式
            new_genre_lower = new_genre.strip().lower()

            # 检查是否已存在
            if new_genre_lower in current_genres_list:
                print("Fail")
                return

            # 添加新genre
            updated_genres = ";".join(current_genres_list + [new_genre_lower])
            cursor.execute("UPDATE Users SET genres = %s WHERE uid = %s", (updated_genres, uid))
            conn.commit()
            print("Success")
        else:
            # print("Fail: User not found")
            print("Fail")

    except mysql.connector.Error as err:
        # print("Fail", err)
        print("Fail")

    finally:
        cursor.close()
        conn.close()


def deleteViewer(uid):
    # pass
    # 还没测试
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # 检查uid是否存在于Users
        cursor.execute("SELECT uid FROM Users WHERE uid = %s", (uid,))
        if not cursor.fetchone():
            # print("Fail: User not found")
            print("Fail")
            return

        cursor.execute("DELETE FROM Users WHERE uid = %s", (uid,))
        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        # print("Fail", err)
        print("Fail")

    finally:
        cursor.close()
        conn.close()


def insertMovie(rid, website_url):
    # pass
    # 还没测试
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # 检查外键rid是否存在于Releases
        cursor.execute("SELECT rid FROM Releases WHERE rid = %s", (rid,))
        if not cursor.fetchone():
            # print("Fail: Release ID does not exist")
            print("Fail")
            return

        cursor.execute("INSERT INTO Movies (rid, website_url) VALUES (%s, %s)", (rid, website_url))
        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        # print("Fail", err)
        print("Fail")

    finally:
        cursor.close()
        conn.close()


def insertSession(sid, uid, rid, ep_num, initiate_at, leave_at, quality, device):
    # pass
    # 还没测试
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # 检查uid是否存在于Viewers
        cursor.execute("SELECT uid FROM Viewers WHERE uid = %s", (uid,))
        if not cursor.fetchone():
            # print("Fail: Viewer ID does not exist")
            print("Fail")
            return

        # 检查rid, ep_num是否存在于Videos中
        cursor.execute("SELECT rid FROM Videos WHERE rid = %s AND ep_num = %s", (rid, ep_num))
        if not cursor.fetchone():
            # print("Fail: Video episode does not exist")
            print("Fail")
            return

        # 检查时间戳是否有效
        if initiate_at >= leave_at:
            # print("Fail: initiate_at must be earlier than leave_at")
            print("Fail")
            return

        # 检查quality是否有效
        valid_qualities = {"480p", "720p", "1080p"}
        if quality not in valid_qualities:
            # print("Fail: Invalid quality. Must be one of", valid_qualities)
            print("Fail")
            return

        # 检查device是否为有效
        valid_devices = {"mobile", "desktop"}
        if device not in valid_devices:
            # print("Fail: Invalid device. Must be one of", valid_devices)
            print("Fail")
            return

        cursor.execute("""
            INSERT INTO Sessions (sid, uid, rid, ep_num, initiate_at, leave_at, quality, device)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (sid, uid, rid, ep_num, initiate_at, leave_at, quality, device))

        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        # print("Fail", err)
        print("Fail")

    finally:
        cursor.close()
        conn.close()


def updateRelease(rid, title):
    # pass
    # 还没测试
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # 检查rid是否存在
        cursor.execute("SELECT rid FROM Releases WHERE rid = %s", (rid,))
        if not cursor.fetchone():
            # print("Fail: Release ID does not exist")
            print("Fail")
            return

        cursor.execute("UPDATE Releases SET title = %s WHERE rid = %s", (title, rid))
        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        # print("Fail", err)
        print("Fail")

    finally:
        cursor.close()
        conn.close()


def listReleases(uid):
    # pass
    # 还没测试
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # 查询uid用户评价过的release
        cursor.execute("""
            SELECT DISTINCT r.rid, r.genre, r.title
            FROM Reviews rv
            JOIN Releases r ON rv.rid = r.rid
            WHERE rv.uid = %s
            ORDER BY r.title ASC
        """, (uid,))

        results = cursor.fetchall()

        if results:
            for row in results:
                print(",".join(map(str, row)))
        else:
            # print("Fail: No reviewed releases found")
            print("Fail")

    except mysql.connector.Error as err:
        # print("Fail", err)
        print("Fail")

    finally:
        cursor.close()
        conn.close()


def popularRelease(N):
    pass


def releaseTitle(sid):
    pass


def activeViewer(N, start_date, end_date):
    pass


def videosViewed(rid):
    pass


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 project.py <function name> [params...]")
        return

    func = sys.argv[1]
    args = sys.argv[2:]

    if func == "import":
        if len(args) != 1:
            print("Usage: python3 project.py import <folderName>")
            return
        import_data(args[0])
    elif func == "insertViewer":
        if len(args) != 12:
            print(
                "Usage: python3 project.py insertViewer <uid> <email> <nickname> <street> <city> <state> <zip> <genres> <joined_date> <first> <last> <subscription>")
            return
        insertViewer(*args)
    elif func == "addGenre":
        if len(args) != 2:
            print("Usage: python3 project.py addGenre <uid> <genre>")
            return
        addGenre(*args)
    elif func == "deleteViewer":
        if len(args) != 1:
            print("Usage: python3 project.py deleteViewer <uid>")
            return
        deleteViewer(*args)
    elif func == "insertMovie":
        if len(args) != 2:
            print("Usage: python3 project.py insertMovie <rid> <website_url>")
            return
        insertMovie(*args)
    elif func == "insertSession":
        if len(args) != 8:
            print(
                "Usage: python3 project.py insertSession <sid> <uid> <rid> <ep_num> <initiate_at> <leave_at> <quality> <device>")
            return
        insertSession(*args)
    elif func == "updateRelease":
        if len(args) != 2:
            print("Usage: python3 project.py updateRelease <rid> <title>")
            return
        updateRelease(*args)
    elif func == "listReleases":
        if len(args) != 1:
            print("Usage: python3 project.py listReleases <uid>")
            return
        listReleases(*args)
    elif func == "popularRelease":
        if len(args) != 1:
            print("Usage: python3 project.py popularRelease <N>")
            return
        popularRelease(*args)
    elif func == "releaseTitle":
        if len(args) != 1:
            print("Usage: python3 project.py releaseTitle <sid>")
            return
        releaseTitle(*args)
    elif func == "activeViewer":
        if len(args) != 3:
            print("Usage: python3 project.py activeViewer <N> <start_date> <end_date>")
            return
        activeViewer(*args)
    elif func == "videosViewed":
        if len(args) != 1:
            print("Usage: python3 project.py videosViewed <rid>")
            return
        videosViewed(*args)
    else:
        print("Unknown function")


if __name__ == "__main__":
    main()