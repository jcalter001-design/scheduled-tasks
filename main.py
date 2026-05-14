##################### Hard Starting Project ######################

# 1. Update the birthdays.csv with your friends & family's details. 
# HINT: Make sure one of the entries matches today's date for testing purposes. 

# 2. Check if today matches a birthday in the birthdays.csv
# HINT 1: Only the month and day matter. 
# HINT 2: You could create a dictionary from birthdays.csv that looks like this:
# birthdays_dict = {
#     (month, day): data_row
# }
#HINT 3: Then you could compare and see if today's month/day matches one of the keys in birthday_dict like this:
# if (today_month, today_day) in birthdays_dict:

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# HINT: https://www.w3schools.com/python/ref_string_replace.asp

# 4. Send the letter generated in step 3 to that person's email address.
# HINT: Gmail(smtp.gmail.com), Yahoo(smtp.mail.yahoo.com), Hotmail(smtp.live.com), Outlook(smtp-mail.outlook.com)

import os
import pandas
import datetime as dt
import random
import smtplib

#constant for readability, used to replace the generic name with the dynamically chosen name for the letter
TEMPLATE_NAME = "[NAME]"
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


#Saves the day and month to a set of variables to be used for checking birthdays going forward
today = dt.datetime.now()
month = today.month
day = today.day
#This function will choose a random letter
def choose_letter():
    letter_choices = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]
    return random.choice(letter_choices)

#This function will actually send the email
def send_email(name, email):
    with open(file=choose_letter(), mode="r") as file:
        letter_template = file.read()
    final_letter = letter_template.replace(TEMPLATE_NAME, name)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=email,
                            msg=f"Subject: Happy Birthday!\n\n{final_letter}".encode("utf8"))

#This gets the data in the csv, iterates over it, and saves the names/emails for anyone whose birthday it is
is_birthday = {"names": [], "emails": []}
index = 0
df = pandas.read_csv("birthdays.csv")
birthday_dict = df.to_dict(orient="records")
print(birthday_dict)
for rows in birthday_dict:
    if rows["month"] == month and rows["day"] == day:
        is_birthday["names"].append(rows["name"])
        is_birthday["emails"].append(rows["email"])
        send_email(name=is_birthday["names"][index], email=is_birthday["emails"][index])
        index += 1
#todo If it in fact IS someone's birthday, pick a random letter and replace the name in the letter with the person
# whose birthday it is

#todo Finally sent the letter to that person's email address


