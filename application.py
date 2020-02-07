import requests
import json
import os
from requests.exceptions import HTTPError
from report import Report


def get_data(url):
    try:
        response = requests.get(url)
        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
        return {}
    return response.json()


class Application:
    def __init__(self):
        self.tasks = []
        self.users = []

    def get_data_from_url(self, task_url, user_url):
        self.tasks = get_data(task_url)
        self.users = get_data(user_url)

    def get_data_from_file(self, task_file, user_file):
        try:
            with open(task_file, "r") as read_file:
                self.tasks = json.load(read_file)
            with open(user_file, "r") as read_file:
                self.users = json.load(read_file)
        except FileNotFoundError as err:
            print(err)

    def generate_reports(self, task_dir='./', no_file=False):
        for user in self.users:
            report = Report(str(f'{task_dir}{user["username"]}.txt.tmp'))
            # готовим содержимое файла в виде списка.
            if not report.prepare_content(user, self.tasks):
                continue
            # если отключен дебажный флаг
            if not no_file:
                if not os.path.exists(task_dir):
                    try:
                        os.makedirs(task_dir)
                    except Exception as err:
                        print(f'{err} Report cannot be saved.')
                        break
                # сохраняем временный файл
                if not report.write_temp_file(report.file_name):
                    break
                # валидируем временный файл
                if report.validate_output_file(report.file_name):
                    # сохраняем изменения, переименовывая старый отчет
                    report.commit()
                else:
                    print("Report validation error. Changes will not accepted.")
                    # удаляем временный файл
                    report.rollback()
