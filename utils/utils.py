import importlib


def import_method_from_string(file, method_name):
    """
    Add the posibility to import method dynamically using a string like "intents.daily.date_and_time.intent" as file and
    "what_time_is_it" as method_name
    """
    mod = importlib.import_module(file)
    met = getattr(mod, method_name)

    return met
