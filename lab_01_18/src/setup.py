
def read_manual() -> str:
    file = open("./src/app_messages/manual.txt", "r", encoding='utf-8')
    manual = file.read()
    file.close()
    return manual

def read_task() -> str:
    file = open("./src/app_messages/task.txt", "r", encoding='utf-8')
    task = file.read()
    file.close()
    return task

