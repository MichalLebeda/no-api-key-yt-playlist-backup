import sqlite3
from typing import Optional

DATABASE_FILE = "data/database.db"


def get_connection():
    import sqlite3
    con = sqlite3.connect(DATABASE_FILE)

    return con


def init_schema(con: sqlite3.Connection):
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS scrape (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utc_timestamp TIMESTAMP NOT NULL
        )
        """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS playlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL
        )
        """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS video (
            id TEXT PRIMARY KEY
        )
        """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS scraped_video (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scrape_id INTEGER,
            video_id TEXT,
            title TEXT,
            duration TEXT,
            FOREIGN KEY(scrape_id) REFERENCES scrape(id),
            FOREIGN KEY(video_id) REFERENCES video(id)
        )
        """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS scraped_playlist_video (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scrape_id INTEGER,
            playlist_id INTEGER,
            video_id INTEGER,
            FOREIGN KEY(scrape_id) REFERENCES scrape(id),
            FOREIGN KEY(playlist_id) REFERENCES playlist(id)
            FOREIGN KEY(video_id) REFERENCES video(id)
        )
        """
    )

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS error (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scrape_id INTEGER,
            playlist_id INTEGER NULL,
            video_id INTEGER NULL,
            text TEXT,
            FOREIGN KEY(scrape_id) REFERENCES scrape(id),
            FOREIGN KEY(playlist_id) REFERENCES playlist(id)
            FOREIGN KEY(video_id) REFERENCES video(id)
        )
        """
    )


def insert_new_scrape(con: sqlite3.Connection) -> int:
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO scrape (utc_timestamp)
        VALUES (CURRENT_TIMESTAMP)
        """
    )
    con.commit()

    return cur.lastrowid


def insert_or_get_playlist(con: sqlite3.Connection, playlist_url) -> int:
    cur = con.cursor()

    cur.execute(
        """
        SELECT id 
        FROM  playlist 
        WHERE url=?
        """,
        (playlist_url,),
    )
    maybe_playlist = cur.fetchone()
    if maybe_playlist is not None:
        return maybe_playlist[0]

    cur.execute(
        """
        INSERT INTO playlist (url)
        VALUES (?)
        """,
        (playlist_url,),
    )
    con.commit()

    return cur.lastrowid


def ensure_video(
        con: sqlite3.Connection,
        id: str,
):
    cur = con.cursor()

    cur.execute(
        """
        SELECT id 
        FROM  video 
        WHERE id=?
        """,
        (id,),
    )
    maybe_video = cur.fetchone()
    if maybe_video is not None:
        return

    cur.execute(
        """
        INSERT INTO video (id)
        VALUES (?)
        """,
        (id,),
    )
    con.commit()


def insert_scraped_video(
        con: sqlite3.Connection,
        scrape_id: int,
        video_id: int,
        title: Optional[str],
        duration: Optional[int]
) -> int:
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO scraped_video (scrape_id, video_id, title, duration)
        VALUES (?,?,?,?)
        """,
        (scrape_id, video_id, title, duration)
    )
    con.commit()

    return cur.lastrowid


def insert_scraped_playlist_video(
        con: sqlite3.Connection,
        scrape_id: int,
        playlist_id: int,
        video_id: int,
) -> int:
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO scraped_playlist_video (scrape_id, playlist_id, video_id)
        VALUES (?,?,?)
        """,
        (scrape_id, playlist_id, video_id)
    )
    con.commit()

    return cur.lastrowid


def insert_error(
        con: sqlite3.Connection,
        scrape_id: int,
        playlist_id: Optional[int],
        video_id: Optional[int],
        text: str
) -> int:
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO error (scrape_id, playlist_id, video_id, text)
        VALUES (?,?,?, ?)
        """,
        (scrape_id, playlist_id, video_id, text)
    )
    con.commit()

    return cur.lastrowid
