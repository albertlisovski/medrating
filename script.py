import requests
from requests.exceptions import HTTPError
# import json
import os
# import datetime
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


def prepare_content(user):
    content = [f'{user["name"]} <{user["email"]}> {strftime("%Y-%m-%d %H:%M", localtime())}\n']
    content.append(f'{user["company"]["name"]}\n\n')
    content.append('Завершенные задачи:' + '\n')

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

    content.extend(completed_tasks)
    content.append('\n' + 'Оставшиеся задачи:' + '\n')
    content.extend(uncompleted_tasks)

    return content


tasks = get_data('https://json.medrating.org/todos')
users = get_data('https://json.medrating.org/users')

if not os.path.exists('tasks'):
    os.makedirs('tasks')

for user in users:
    file_name = str(f'./tasks/{user["username"]}.txt')

    # если файл уже существует, то его нужно переименовать по правилу
    if os.path.exists(file_name):
        file_time_stamp = strftime("%Y-%m-%dT%H:%M", localtime(os.path.getctime(file_name)))
        os.rename(file_name, str(f'{file_name[:-4]}_{file_time_stamp}.txt'))

    # готовим содержимое файла в виде списка
    file_content = prepare_content(user)

    # открываем файл для записи
    file = open(file_name, "w")
    # пишем содержимое
    file.writelines(file_content)
    file.close()
