# YouTube Playlist Backup

YouTube videos get deleted/hidden all the time.  
Sadly, it's not even possible to get the title which would be useful for music playlists etc.  
This tool saves all the videos into a database making it possible to obtain titles of deleted videos.

## Features

- Obtain video/playlist metadata by scraping playlist URLs defined in `playlists.txt` file
- Store metadata from each execution in SQLite database making tracking video availability changes possible.
- **No API key needed** (only **public/unlisted** playlists supported)

## Usage

Put non-private (public/unlisted) playlist URLs to `playlists.txt`.  
One URL per line, like so:

```
https://www.youtube.com/playlist?list=PLAYLIST_ID_01 # Some comment/name
https://www.youtube.com/playlist?list=PLAYLIST_ID_02
https://www.youtube.com/playlist?list=PLAYLIST_ID_03
```

Setup venv

```bash
./setup.sh
```

Run

```bash
./run.sh
```

Check the execution logs or inspect the `data/database.db` file using tool such as [DB Browser for Sqlite](https://sqlitebrowser.org/).

**TIP: Configure a Cron job for periodical checks**

## Todo

- Optionally backup video files, not just metadata
- Use ORM with migrates  
- Use Python package