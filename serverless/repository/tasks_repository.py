from utils.task_status_enum import TaskStatus
import datetime

def get_task_id_by_filepath(db_connection, filepath):
    cursor = db_connection.cursor()
    cursor.execute("SELECT id from imagefunctions.tasks WHERE filepath = '%s'" % (filepath))
    return cursor.fetchone()[0]

def update_task_status(db_connection, status: TaskStatus, task_id):
    cursor = db_connection.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE imagefunctions.tasks SET Status='%s', LastModifiedDate='%s' WHERE Id = '%s'" % (status.value, timestamp, task_id))
    db_connection.commit()
