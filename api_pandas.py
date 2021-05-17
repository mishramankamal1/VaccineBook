import numpy as np
import pandas as pd
import requests
import json
import param
import notification
from datetime import datetime, timedelta
import time

url_dist_code = '64'
actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(param.num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
#actual_dates = ['18-05-2021']
vaccine_center = []


def run_vaccine():
    counter = 0
    for pinCode in param.pinCodes:
        for given_date in actual_dates:
            url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={}&date={}'.format(
                url_dist_code, given_date)
            print(given_date)
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
            result = requests.get(url, headers=header)

            if result.ok:
                response_json = result.json()
                print("Vaccine Available")
                for centers in response_json['centers']:
                    for session in centers['sessions']:
                        vaccine_center.append(
                            [centers["name"], centers['address'], centers['block_name'], session['vaccine'],
                             session['date'], session['min_age_limit'], session["available_capacity"]])
                        counter = counter + 1

    if counter > 0:
        print(vaccine_center)
        return True
    else:
        return False


while True:
    flag = run_vaccine()
    if flag:
        print("inside if in while")
        column_name = ['Center_Name', 'Address', 'Block', 'Vaccine_Name', 'Date', 'Age', 'Capacity']
        vaccine_df = pd.DataFrame(vaccine_center, columns=column_name)
        mask = ((vaccine_df.Age == param.age) & (vaccine_df.Capacity > 0))
        # vaccine_df = vaccine_df[(vaccine_df['Age'] == param.age) & (vaccine_df['Capacity'] > 0)]
        vaccine_df = vaccine_df.loc[mask, :]
        whatsapp_center = ', '.join(str(e) for e in vaccine_df['Center_Name'])
        if len(vaccine_df) > 0:
            print("notifications")
            notification.mail_send(vaccine_df)
            # notification.send_whatsapp_message(whatsapp_center, vaccine_df.Date.unique())
    else:
        print("No Vaccine found")

    dt = datetime.now() + timedelta(minutes=1)

    while datetime.now() < dt:
        time.sleep(1)
