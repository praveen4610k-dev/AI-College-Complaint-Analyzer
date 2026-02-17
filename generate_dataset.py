import pandas as pd
import random

categories = {
    "Hostel": [
        "Water problem in hostel",
        "Food quality is poor",
        "Fan not working in room",
        "Room cleaning not done",
        "Wifi not working",
        "Electricity issue in hostel",
        "Bed damaged",
        "Washroom not clean"
    ],
    "Academic": [
        "Faculty not explaining properly",
        "Syllabus not completed",
        "Internal marks not updated",
        "Exam timetable delay",
        "Lab sessions insufficient",
        "Notes not provided",
        "Assignment deadline issue",
        "Online class quality poor"
    ],
    "Transport": [
        "Bus not arriving on time",
        "Bus overcrowded",
        "Driver driving rashly",
        "Bus route changed",
        "Bus breakdown issue",
        "No evening bus",
        "Bus seats damaged",
        "Transport fee issue"
    ],
    "Infrastructure": [
        "Projector not working",
        "Classroom fan not working",
        "Bench broken",
        "Power failure in lab",
        "Internet slow",
        "Lift not working",
        "AC not working",
        "Parking light issue"
    ],
    "Administration": [
        "Scholarship not credited",
        "ID card not issued",
        "Fee receipt not available",
        "Office staff rude",
        "Certificate delay",
        "Document verification delay",
        "Transfer certificate slow",
        "Notice not informed"
    ]
}

data = []

for category, complaints in categories.items():
    for _ in range(160):  # 160 × 5 categories = 800 complaints
        complaint = random.choice(complaints)
        data.append([complaint, category])

df = pd.DataFrame(data, columns=["Complaint", "Category"])
df.to_csv("complaints_dataset.csv", index=False)

print("800 complaints dataset generated successfully!")