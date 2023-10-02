import csv
import random

# Set the number of students and preferences
num_students = 500
num_prefs = 4
topic_range = range(1, 100)

# Create a list of student IDs
student_ids = [1000 + i for i in range(num_students)]

# Create a list of preferences for each student
student_prefs = [[random.sample(topic_range, num_prefs)] for _ in range(num_students)]

# Write the data to a CSV file
with open('student-data500.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Studentno'] + [f'Pref{i}' for i in range(1, num_prefs+1)])
    for i, student_id in enumerate(student_ids):
        writer.writerow([student_id] + student_prefs[i][0])