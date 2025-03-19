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
                print(f"File not found: {file_path}")
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 跳过表头
                rows = [tuple(row) for row in reader]

                if rows:
                    cursor.executemany(insert_query, rows)
                    conn.commit()
                    print(f"Inserted {len(rows)} rows into {table}")
                else:
                    print(f"No data in {csv_file}")

        print("Success")
    except Exception as e:
        print("Fail", e)
        raise
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
        print("Fail", err)

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
            updated_genres = current_genres + ";" + new_genre if current_genres else new_genre
            cursor.execute("UPDATE Users SET genres = %s WHERE uid = %s", (updated_genres, uid))
            conn.commit()
            print("Success")
        else:
            print("Fail: User not found")

    except mysql.connector.Error as err:
        print("Fail", err)
    
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
            print("Fail: User not found")
            return
        
        cursor.execute("DELETE FROM Users WHERE uid = %s", (uid,))
        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        print("Fail", err)
    
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
            print("Fail: Release ID does not exist")
            return
        
        cursor.execute("INSERT INTO Movies (rid, website_url) VALUES (%s, %s)", (rid, website_url))
        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        print("Fail", err)

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
            print("Fail: Viewer ID does not exist")
            return
        
        # 检查rid, ep_num是否存在于Videos中
        cursor.execute("SELECT rid FROM Videos WHERE rid = %s AND ep_num = %s", (rid, ep_num))
        if not cursor.fetchone():
            print("Fail: Video episode does not exist")
            return
        
        # 检查时间戳是否有效
        if initiate_at >= leave_at:
            print("Fail: initiate_at must be earlier than leave_at")
            return
        
        # 检查quality是否有效
        valid_qualities = {"480p", "720p", "1080p"}
        if quality not in valid_qualities:
            print("Fail: Invalid quality. Must be one of", valid_qualities)
            return
        
        # 检查device是否为有效
        valid_devices = {"mobile", "desktop"}
        if device not in valid_devices:
            print("Fail: Invalid device. Must be one of", valid_devices)
            return
        
        cursor.execute("""
            INSERT INTO Sessions (sid, uid, rid, ep_num, initiate_at, leave_at, quality, device)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (sid, uid, rid, ep_num, initiate_at, leave_at, quality, device))

        conn.commit()
        print("Success")

    except mysql.connector.Error as err:
        print("Fail", err)

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
            print("Fail: Release ID does not exist")
            return
        
        cursor.execute("UPDATE Releases SET title = %s WHERE rid = %s", (title, rid))
        conn.commit()
        print("Success")
    
    except mysql.connector.Error as err:
        print("Fail", err)

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
            print("Fail: No reviewed releases found")

    except mysql.connector.Error as err:
        print("Fail", err)

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
            print("Usage: python3 project.py insertViewer <uid> <email> <nickname> <street> <city> <state> <zip> <genres> <joined_date> <first> <last> <subscription>")
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
            print("Usage: python3 project.py insertSession <sid> <uid> <rid> <ep_num> <initiate_at> <leave_at> <quality> <device>")
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