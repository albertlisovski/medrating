from report import Report

def validate_output_file(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print(f'File {file_name} not found!')
        return False
    finally:
        file.close()
    return
