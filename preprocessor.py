import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[APap][Mm]\s?-\s'

    messages = re.split(pattern, data)[1:]
    messages

    dates = re.findall(pattern,data)
    dates

    df = pd.DataFrame({"user_message":messages, "message_date": dates})

# clean \u202df

    df["message_date"] = df["message_date"].str.replace('\u202f',' ',regex=True)

# convert message_date type

    df["message_date"] = pd.to_datetime(df["message_date"], format="%m/%d/%y, %I:%M %p - ", errors="coerce" )

    df.rename(columns={"message_date": "date"}, inplace = True)

    

    users = []
    messages_clean = []

    for message in df["user_message"]:
        entry = re.split(r'([^:]+): (.+)', message)
        if len(entry) >= 3:
           users.append(entry[1].strip())
           messages_clean.append(entry[2].strip())
        else:
            users.append("group_notification")
            messages_clean.append(message.strip())

    df["user"] = users
    df["message"] = messages_clean
    df.drop(columns=["user_message"], inplace=True)


    df["only_date"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []

    for hour in df[["day_name","hour"]]["hour"]:
        if hour == 23:
          period.append(str(hour) + "-" + str("00"))

        elif hour == 0:
          period.append(str("00") + "-" + str(hour+1))

        else:
          period.append(str(hour)+ "-" + str(hour+1))    

    df["period"] = period    

    return df