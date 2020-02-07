import os
from time import localtime, strftime
from shutil import copy


class Report:
    def __init__(self, f_name):
        self.file_name = f_name
        self.content = []
        self.completed_tasks = []
        self.uncompleted_tasks = []

    def prepare_content(self, user, tasks):

        for task in tasks:
            if task["userId"] == user["id"]:
                if len(task["title"]) < 50:
                    task_title = task["title"] + '\n'
                else:
                    task_title = task["title"][:50] + '...' + '\n'
                if task["completed"]:
                    self.completed_tasks.append(task_title)
                else:
                    self.uncompleted_tasks.append(task_title)
        # Если задач нет, то переходим к следующему пользователю.
        if (self.completed_tasks == []) and (self.uncompleted_tasks == []):
            print(f'There are no tasks for user {user["id"]}. Nothing to save.')
            return False

        self.content = [f'{user["name"]} <{user["email"]}> {strftime("%Y-%m-%d %H:%M", localtime())}\n']
        self.content.append(f'{user["company"]["name"]}\n')
        self.content.append('\n')
        self.content.append('Завершенные задачи:' + '\n')

        self.content.extend(self.completed_tasks)
        self.content.append('\n')
        self.content.append('Оставшиеся задачи:' + '\n')
        self.content.extend(self.uncompleted_tasks)
        return True

    def write_temp_file(self, file_name):
        try:
            with open(file_name, "w") as file:
                file.writelines(self.content)
                return True
        except Exception as err:
            print(f'{err} Report cannot be saved.')
            return False

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
            copy(self.file_name, str(f'{self.file_name[:-4]}_{file_time_stamp}.txt'))
        os.rename(self.file_name + '.tmp', self.file_name)

    def rollback(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)