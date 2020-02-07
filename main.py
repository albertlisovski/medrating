import sys
from application import Application


if __name__ == "__main__":

    app = Application()
    app.get_data_from_url('https://json.medrating.org/todos', 'https://json.medrating.org/users')
    # app.get_data_from_file('./data/default_tasks.json', './data/default_users.json')

    if (app.tasks == {}) or (app.users == {}):
        print("Data collecting failed. Program aborted.")
        sys.exit()

    app.generate_reports('./tasks/')
