import os
import json
import sqlite3

settings_file_path = './settings.json'
database_folder_path = './database'

def load_settings_file() -> dict:
    if not os.path.exists(settings_file_path):
        settings_dict = {"monitor_folders":[]}
        with open(mode="w", file=settings_file_path) as f:
            json.dump(settings_dict, f)
        return settings_dict
    with open(mode="r", file=settings_file_path) as f:
        return json.load(f)

def init_database(db_path):
    if not os.path.exists(database_folder_path):
        os.mkdir(database_folder_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = '''
        create table if not exists monitor (
            id int primary
        )
    '''

    cur.execute(sql)
    conn.commit()

    return (conn, cur)

if __name__ == "__main__":
    load_settings_file()
    for folder in load_settings_file()['monitor']:
        conn, cur = init_database(folder)
