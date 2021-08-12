from threading import Thread

running_tasks = dict()


def add_task(key, thread: Thread):
    running_tasks[key] = thread
    running_tasks[key].start()


def remove_task(key):
    del running_tasks[key]


def contains_task(key):
    if key in running_tasks.keys():
        return True
    return False


def get_tasks_starting_with_in_name(starts_with):
    matching = []

    for key in running_tasks.keys():
        if str(key).startswith(starts_with):
            matching.append(key)

    return matching
