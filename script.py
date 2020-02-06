import requests
from requests.exceptions import HTTPError
import json
import os
#import datetime
from time import gmtime, strftime

try:
    todos = requests.get('https://json.medrating.org/todos')
    # если ответ успешен, исключения задействованы не будут
    todos.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

try:
    users = requests.get('https://json.medrating.org/users')
    # если ответ успешен, исключения задействованы не будут
    users.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

if not os.path.exists('tasks'):
    os.makedirs('tasks')

for user in users.json():
    file_name = str(f'./tasks/{user["username"]}.txt')
    # если файл уже существует, то его нужно переименовать по правилу
    if os.path.exists(file_name):
        file_time_stamp = strftime("%Y-%m-%dT%H:%M", gmtime(os.path.getctime(file_name)))
        os.rename(file_name, str(f'{file_name[:-4]}_{file_time_stamp}.txt'))
    # готовим содержимое файла в виде списка
    file_content = []
    file_content = [f'{user["name"]} <{user["email"]}> {strftime("%Y-%m-%d %H:%M", gmtime())}\n']
    file_content.append(f'{user["company"]["name"]}\n\n')
    file_content.append('Завершенные задачи:' + '\n')
    completed_tasks = []
    uncompleted_tasks = []
    for task in todos.json():
        if task["userId"] == user["id"]:
            if len(task["title"]) < 50:
                task_title = task["title"] + '\n'
            else:
                task_title = task["title"][:50] + '...' + '\n'
            if task["completed"]:
                completed_tasks.append(task_title)
            else:
                uncompleted_tasks.append(task_title)
    file_content.extend(completed_tasks)
    file_content.append('\n' + 'Оставшиеся задачи:' + '\n')
    file_content.extend(uncompleted_tasks)
    # открываем файл для записи
    file = open(file_name, "w")
    # пишем содержимое
    file.writelines(file_content)
    file.close()



    #with open(f'./tasks/{user["username"]}.txt', "w") as write_file:
    #    json.dump(user, write_file)
