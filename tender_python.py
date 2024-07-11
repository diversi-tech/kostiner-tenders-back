import csv
import json
import os
import random
from datetime import datetime, timedelta
from bson import ObjectId

# פונקציה ליצירת שם אקראי
def random_name():
    return ''.join(random.choices(names))


# פונקציה ליצירת תאריך אקראי בטווח נתון
def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# פונקציה ליצירת סכום אקראי
def random_amount():
    return random.randint(1000, 10000)

# יצירת נתונים מגוונים
num_records = 10
data = []

# עדכון הקטגוריות להכללת יותר אפשרויות
categories = ["home", "office", "garden", "technology", "health", "education", "sports", "entertainment"]
reasons = ["late submission", "incomplete documents", "not meeting criteria", "invalid bid"]
tender_names = ["furniture", "stationery", "tools", "electronics", "software", "medical equipment", "sports gear", "entertainment system"]
committee_members = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Eve White", "Michael Green", "Emma Black"]
names = ["John Doe", "Jane Smith", "alice_smith", "bob_johnson", "carol_davis", "eve_martin", "frank_wright", "grace_adams", "henry_brown", "isabella_taylor", "jack_evans", "karen_wilson", "nathan_hall", "olivia_scott", "peter_robinson", "queen_smith", "robert_adams", "samantha_brown"]



for i in range(num_records):
    tender_id = ObjectId()
    category = random.choice(categories)
    tender_name = random.choice(tender_names)
    date = random_date(datetime(2023, 1, 1), datetime(2024, 12, 31)).strftime('%Y-%m-%d')
    participants = []
    for item in range(3):
        participants.append({
            "name": random_name(),
            "amount": random_amount(),
            "isWinner": random.choice([True, False])
        })
    disqualified_participants = []
    for item in range(3):
     disqualified_participants.append({
            "name": random_name(),
            "reason": random.choice(reasons)
        })
    committee_member = random.choice(committee_members)

    data.append({
        "tender_id": tender_id,
        "category": category,
        "tender_name": tender_name,
        "date": date,
        "details": {
            "participants": participants,
            "disqualified_participants": disqualified_participants,
            "committee_member": committee_member
        }
    })

# הגדרת כותרות העמודות
csv_columns = [
    "tender_id", "category", "tender_name", "date",
    "details__participants",
    "details__disqualified_participants",
    "details__committee_member"
]

# כתיבת הנתונים לקובץ CSV
csv_file = "tender.csv"
try:

    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        if os.path.getsize(csv_file) == 0:
            writer.writeheader()

        for item in data:
            # מנרמל את מבנה הנתונים
            normalized_item = {
                "tender_id": item["tender_id"],
                "category": item["category"],
                "tender_name": item["tender_name"],
                "date": item["date"],
                "details__participants": json.dumps(item['details']['participants']),
                "details__disqualified_participants": json.dumps(item['details']['disqualified_participants']),
                # "details__participants__name": item["details"]["participants"][0]["name"] if item["details"][
                #     "participants"] else "",
                # "details__participants__amount": item["details"]["participants"][0]["amount"] if item["details"][
                #     "participants"] else "",
                # "details__participants__isWinner": item["details"]["participants"][0]["isWinner"] if item["details"][
                #     "participants"] else "",
                # "details__disqualified_participants__name": item["details"]["disqualified_participants"][0]["name"] if
                # item["details"]["disqualified_participants"] else "",
                # "details__disqualified_participants__reason": item["details"]["disqualified_participants"][0][
                #     "reason"] if item["details"]["disqualified_participants"] else "",
                "details__committee_member": item["details"]["committee_member"],
            }
            writer.writerow(normalized_item)
except IOError:
    print("I/O error")