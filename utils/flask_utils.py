import json


def get_data_in_request(request):
    data_str = str(request.data.decode('utf8')).replace('"', '\"').replace("\'", "'")

    # if no data return an empty json to avoid error with json.loads below
    if not data_str:
        return {}

    data_json = json.loads(data_str)

    if not isinstance(data_json, dict):
        data_json = json.loads(data_json)

    return data_json
