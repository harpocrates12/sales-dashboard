import json

from urllib.request import urlopen
from secret import Secret, Agents

cache = {}
api_timestamp = 0

def get_values(current_time, day):

    global cache, api_timestamp

    if cache and (current_time - api_timestamp) < 60:
        print(current_time - api_timestamp)
        print("cache filled")
        deals = cache
    else:
        try:
            response, deals, start_x = [], None, 0
            full_response = False

            while full_response == False:
                print ("API request...")
                f = urlopen("https://api.pipedrive.com/v1/deals:(user_id,value,won_time)?filter_id=579&status=all_not_deleted&start=%s&api_token=%s" % (start_x, Secret))
                print ("...successful")

                api_timestamp = current_time

                s = f.read().decode('utf-8')
                response.append(s)

                check_temp = json.loads(s)

                if check_temp['additional_data']['pagination']['more_items_in_collection'] == False:
                    full_response = True
                else:
                    start_x += 100

            for item in response:

                if deals:
                    temp_item = json.loads(item)
                    for i in temp_item['data']:
                        deals['data'].append(i)

                else:
                    deals = json.loads(item)

            print ("filling cache ...")
            cache = deals

        except Exception as e:
            print ("API request failed: ", e)
            return False

    # initialising dict {user_id: [name, current_month_won, month_target, current_day_won]}
    values_temp = json.loads(Agents)
    values = {}
    # convert Keys to integer values so api comparison can match the values
    for val in values_temp:
        # values[int(val)] = [values_temp[val][0],float(values_temp[val][1]),float(values_temp[val][2]),float(values_temp[val][3])]
        values[int(val)] = values_temp[val] + [0]

    # print(values)

    # adding values from API response to current_month_won and current_day_won
    if deals['data']:
        for entry in deals['data']:

            if entry['user_id']['value'] in values:

                values[entry['user_id']['value']][0] = entry['user_id']['name']
                values[entry['user_id']['value']][1] += (entry['value'])
                values[entry['user_id']['value']][-1] += 1

                if entry['won_time']:

                    if entry['won_time'][8:10] == day:
                        values[entry['user_id']['value']][3] += (entry['value'])
            else:
                pass

    # print(values)

    return values