from canvasapi import Canvas
from csv import reader

with open("API_URL.txt", 'r') as url:
    API_URL = url.readline().rstrip('\n')

with open("API_Key.txt", 'r') as key:
    API_Key = key.readline().rstrip('\n')

with open("Course.txt", 'r') as code:
    code = int(code.readline().rstrip('\n'))
    
with open("Assignment.txt", 'r') as ass:
    ass_name = ass.readline().rstrip('\n')

with open("Results.txt", 'r') as result:
    summary = result.readline().rstrip('\n')

canvas = Canvas(API_URL, API_Key)
course = canvas.get_course(code)
students = []

for student in course.get_users(enrollment_type='student'):
    students.append(student.name.split(' ') + [student.id])

results = []
with open(summary, 'r') as _summary:
    csv_reader = reader(_summary)
    header = next(csv_reader)
    if header != None:
        for row in csv_reader:
            results.append(row)

for res in results:
    res[1] = res[1].split('_', 1)[0]

for assignment in course.get_assignments():
    if(ass_name == assignment.name):
        for sub in assignment.get_submissions():
            for res in results:
                if(str(sub.user_id) == res[1]):
                    print("Score of " + res[0] + ", ID: " + res[1] + " changed from " + str(sub.score) + " to " + str(float(res[2])) + ".")
                    sub.edit(
                        submission = {
                            'posted_grade' : float(res[2])
                        }
                    )
