import os
import sys
from application import Application


class User:
    def __init__(self, completed_tasks, uncompleted_tasks):
        self.completed_tasks = completed_tasks
        self.uncompleted_tasks = uncompleted_tasks


if __name__ == "__main__":

    app = Application()
    app.get_data_from_url()

    if (app.tasks == {}) or (app.users == {}):
        print("Data collecting failed. Program aborted.")
        sys.exit()

    if not os.path.exists('tasks'):
        os.makedirs('tasks')

    app.generate_reports()

