from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import sqlite3
import os
import time


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "secure_file_transfer.db"
)

WATCH_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)


def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


class SecureFileMonitor(FileSystemEventHandler):

    def on_moved(self, event):

        if event.is_directory:
            return

        print("=" * 50)

        print("RENAMED / MOVED DETECTED")

        print("FROM :", event.src_path)

        print("TO   :", event.dest_path)

        old_path = event.src_path

        new_path = event.dest_path

        old_name = os.path.basename(old_path)

        new_name = os.path.basename(new_path)

        conn = get_connection()

        cursor = conn.execute(
            """
            UPDATE files
            SET
                filename = ?,
                filepath = ?,
                status = ?,
                integrity = ?,
                risk_level = ?
            WHERE filepath = ?
            """,
            (
                new_name,
                new_path,
                "Threat",
                "Failed",
                "HIGH",
                old_path
            )
        )

        conn.commit()

        print(
            "Rows Updated :",
            cursor.rowcount
        )

        conn.execute(
            """
            INSERT INTO file_events
            (
                event_type,
                file_name,
                file_path,
                source_path,
                destination_path,
                risk_level,
                authorization,
                username,
                event_time
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'))
            """,
            (
                "RENAMED",
                new_name,
                new_path,
                old_path,
                new_path,
                "HIGH",
                "AUTHORIZED",
                "shravya"
            )
        )

        conn.commit()

        conn.close()

        print("DATABASE UPDATED")

        print("=" * 50)


if __name__ == "__main__":

    observer = Observer()

    observer.schedule(
        SecureFileMonitor(),
        WATCH_FOLDER,
        recursive=False
    )

    observer.start()

    print("Watching:", WATCH_FOLDER)

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()
