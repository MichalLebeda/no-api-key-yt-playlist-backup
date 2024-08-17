import json
import pathlib
import os
import datetime
from typing import List

import yt_dlp

from src import db

script_dir = pathlib.Path(__file__).parent.parent
os.chdir(script_dir)

PLAYLISTS_FILENAME = "playlists.txt"


def main():
    scraped_video_ids = set()

    con = db.get_connection()
    db.init_schema(con)
    scrape_id = db.insert_new_scrape(con)

    playlists = read_playlists(PLAYLISTS_FILENAME)

    for playlist in playlists:
        scrape_playlist(con, playlist, scrape_id, scraped_video_ids)


def read_playlists(playlists_file: str) -> List[str]:
    if not os.path.exists(playlists_file):
        raise Exception(f"Playlists file {playlists_file} does not exist!")

    with open(playlists_file, "r") as f:
        playlists = [url.split("#")[0].strip() for url in f.readlines()]
        return playlists


def scrape_playlist(con, playlist, scrape_id, scraped_video_ids):
    playlist_id = db.insert_or_get_playlist(con, playlist)

    print(50 * "-")
    print("playlist: ", playlist)
    with yt_dlp.YoutubeDL({"ignoreerrors": True, "quiet": True}) as ydl:
        try:
            playlist_dict = ydl.extract_info(playlist, download=False, process=False)
        except Exception as e:
            print(f"LOGGING ERROR:e {e}")
            db.insert_error(con, scrape_id, playlist_id, None, "extract_info(playlist failed: " + str(e))

        for video in playlist_dict["entries"]:
            scrape_video(con, playlist_id, scrape_id, scraped_video_ids, video)


def scrape_video(con, playlist_id, scrape_id, scraped_video_ids, video):
    id = video.get("id")
    title = video.get("title")
    duration = video.get("duration")

    print("\t", 50 * "-")
    print("\t", "title:", title)
    print("\t", "id:", id)
    print("\t", "duration:", duration)

    if id not in scraped_video_ids:
        db.ensure_video(con, id)
        db.insert_scraped_video(
            con,
            scrape_id,
            id,
            title,
            duration
        )
    db.insert_scraped_playlist_video(
        con,
        scrape_id,
        playlist_id,
        id
    )
    scraped_video_ids.add(id)


if __name__ == '__main__':
    main()
