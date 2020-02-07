import requests
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

    def get_data_from_url(self):
        self.tasks = get_data('https://json.medrating.org/todos')
        self.users = get_data('https://json.medrating.org/users')

    def get_data_from_file(self):
        pass

    def generate_reports(self):
        for user in self.users:
            report = Report(str(f'./tasks/{user["username"]}.txt.tmp'))
            # готовим содержимое файла в виде списка. Если задач нет, то переходим к следующему пользователю.
            if not report.prepare_content(user, self.tasks):
                continue
            # сохраняем временный файл
            report.write_temp_file(report.file_name)
            # валидируем временный файл
            if report.validate_output_file(report.file_name):
                # сохраняем изменения, переименовывая старый отчет
                report.commit()
            else:
                print("Report validation error. Changes will not accepted.")
                # удаляем временный файл
                report.rollback()
