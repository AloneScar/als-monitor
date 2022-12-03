import os
import json
import sqlite3

settings_file_path = './settings.json'
database_folder_path = './.database'

def load_settings_file() -> dict:
    if not os.path.exists(settings_file_path):
        settings_dict = {"monitor_folders":[]}
        with open(mode="w", file=settings_file_path) as f:
            json.dump(settings_dict, f)
        return settings_dict
    with open(mode="r", file=settings_file_path) as f:
        return json.load(f)

def init_database(db_name):
    if not os.path.exists(database_folder_path):
        os.mkdir(database_folder_path)

    conn = sqlite3.connect(os.path.join(database_folder_path, db_name + ".db"))
    cur = conn.cursor()

    sql = '''
        create table if not exists files_info (
            id integer primary key autoincrement,
            path text,
            timestamp text
        )
    '''

    cur.execute(sql)
    conn.commit()

    return (conn, cur)

def get_files_info(folder_name):
    files_info = []
    for curDir, _,  files in os.walk(folder_name):
        for file in files:
            file_path = os.path.join(curDir, file)
            files_info.append((
                file_path,
                os.stat(file_path).st_mtime,
            ))
    return files_info

def comparison_files_info(current_files_info, cur):
    updated_files_info = []

    cur.execute("select path, timestamp from files_info")
    pervious_files_info = cur.fetchall()

    pervious_paths = set([path[0] for path in pervious_files_info])
    current_paths = set([path[0] for path in current_files_info])

    intersection_paths = pervious_paths & current_paths

    added_path = list(current_paths - intersection_paths)
    added_files_info = list(filter(lambda file: file[0] in added_path, current_files_info))
    deleted_paths = list(pervious_paths - intersection_paths)

    pervious_timestamps = [timestamp[1] for timestamp in pervious_files_info]

    for file_info in current_files_info:
        if file_info[0] in current_paths or file_info[0] in pervious_paths:
            continue
        pervious_index = pervious_paths.index(file_info[0])
        if file_info[0] != pervious_timestamps[pervious_index]:
            updated_files_info.append(pervious_files_info[pervious_index])
    
    updated_files_info(added_files_info, deleted_paths, updated_files_info)
    
    return (added_files_info, deleted_paths, updated_files_info)

def updated_database(added_files_info, deleted_paths, cur, conn):
    cur.executemany('insert into files_info (path, timestamp) values (?, ?)', added_files_info)
    cur.executemany('delete from files_info where path=?', deleted_paths)
    conn.commit()

def main():
    for folder_path in load_settings_file()['monitor_folders']:
        # _, folder_name = os.path.split(folder_path)
        conn, cur = init_database(folder_path.replace('\\', "-").replace('/', "-").replace(':', '-'))
        current_files_info = get_files_info(folder_path)
        added_files_info, deleted_paths, updated_files_info = comparison_files_info(current_files_info, cur)


if __name__ == "__main__":
    main()