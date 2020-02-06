import requests
from requests.exceptions import HTTPError
import os
from time import localtime, strftime


def get_data(url):
    try:
        response = requests.get(url)
        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return response.json()


class User:
    def __init__(self, completed_tasks, uncompleted_tasks):
        self.completed_tasks = completed_tasks
        self.uncompleted_tasks = uncompleted_tasks


class Report:
    def __init__(self, f_name):
        self.file_name = f_name

    def prepare_content(self, user):
        self.content = [f'{user["name"]} <{user["email"]}> {strftime("%Y-%m-%d %H:%M", localtime())}\n']
        self.content.append(f'{user["company"]["name"]}\n')
        self.content.append('\n')
        self.content.append('Завершенные задачи:' + '\n')

        completed_tasks = []
        uncompleted_tasks = []

        for task in tasks:
            if task["userId"] == user["id"]:
                if len(task["title"]) < 50:
                    task_title = task["title"] + '\n'
                else:
                    task_title = task["title"][:50] + '...' + '\n'
                if task["completed"]:
                    completed_tasks.append(task_title)
                else:
                    uncompleted_tasks.append(task_title)

        self.content.extend(completed_tasks)
        self.content.append('\n')
        self.content.append('Оставшиеся задачи:' + '\n')
        self.content.extend(uncompleted_tasks)

    def write_temp_file(self, file_name):
        with open(file_name, "w") as file:
            file.writelines(self.content)

    def validate_output_file(self, file_name):
        try:
            f = open(file_name)
            file_content = []
            for line in f:
                file_content.append(line)
            f.close()
            return self.content == file_content
        except FileNotFoundError:
            print(f'File {file_name} not found!')
            return False

    def commit(self):
        self.file_name = self.file_name[:-4]
        # если файл уже существует, то его нужно переименовать по правилу
        if os.path.exists(self.file_name):
            file_time_stamp = strftime("%Y-%m-%dT%H:%M", localtime(os.path.getctime(self.file_name)))
            os.rename(self.file_name, str(f'{self.file_name[:-4]}_{file_time_stamp}.txt'))
        os.rename(self.file_name + '.tmp', self.file_name)


tasks = get_data('https://json.medrating.org/todos')
users = get_data('https://json.medrating.org/users')

if not os.path.exists('tasks'):
    os.makedirs('tasks')

for user in users:
    report = Report(str(f'./tasks/{user["username"]}.txt.tmp'))
    # готовим содержимое файла в виде списка
    report.prepare_content(user)
    # сохраняем временный файл
    report.write_temp_file(report.file_name)
    # валидируем временный файл
    if report.validate_output_file(report.file_name):
        report.commit()
    else:
        print("Report validation error. Changes will not accepted.")

