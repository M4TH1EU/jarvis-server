import threading
from time import time, sleep

from lingua_franca.parse import extract_duration

from jarvis.skills import Skill, SkillRegistering, background_tasks
from jarvis.skills.decorators import intent_file_handler
from jarvis.utils import languages_utils


class TimerSkill(Skill, metaclass=SkillRegistering):
    def __init__(self, data=dict):
        super().__init__("TimerSkill", data)

    def register(self):
        super(TimerSkill, self).register()

    @intent_file_handler("start_timer.intent", "StartTimerIntent")
    def handle_start_timer(self, data):
        print(data)

        timestamp_in_seconds = int(time())

        if 'duration' in data:
            duration = extract_duration(data['duration'], languages_utils.get_language())[0]
            duration_in_seconds = int(duration.total_seconds())

            if 'name' in data:
                print("Start timer for {} named {}".format(data['duration'], data['name']))
                pass
            else:
                print("Start timer for {} without name".format(data['duration']))
                # TODO : ask for name

                timer_thread_key = "timer_" + str(timestamp_in_seconds) + "_" + str(
                    timestamp_in_seconds + duration_in_seconds)
                background_tasks.add_task(
                    timer_thread_key,
                    threading.Thread(target=timer_thread, args=[duration_in_seconds, timer_thread_key]))
        else:
            print("No amount and/or time_unit")
        pass

    @intent_file_handler("stop_timer.intent", "StopTimerIntent")
    def handle_stop_timer(self, data):

        if len(get_all_timers()) <= 1:
            background_tasks.remove_task(get_all_timers()[0])

        print("stop")


def create_skill(data):
    return TimerSkill(data)


def timer_thread(seconds, key):
    print("Starting timer in thread for " + str(seconds) + "s")

    while seconds > 0 and key in background_tasks.running_tasks.keys():
        print(str(seconds))
        seconds = seconds - 1
        sleep(1)

    if key not in background_tasks.running_tasks.keys():
        print("Timer (" + key + ") killed!")
    else:
        print("End of timer!! BIP BIP BOUP BIP")


def get_all_timers():
    return background_tasks.get_tasks_starting_with_in_name("timer")
