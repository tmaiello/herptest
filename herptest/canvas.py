from canvasapi import Canvas

with open("API_URL.txt", 'r') as url:
    API_URL = url.readline().rstrip('\n')

with open("API_Key.txt", 'r') as key:
    API_Key = key.readline().rstrip('\n')

with open("Course.txt", 'r') as code:
    code = int(code.readline().rstrip('\n'))
    
with open("Assignment.txt", 'r') as ass:
    ass_name = ass.readline().rstrip('\n')

canvas = Canvas(API_URL, API_Key)
course = canvas.get_course(code)
students = []

for student in course.get_users(enrollment_type='student'):
    students.append(student.name.split(' ') + [student.id])

for assignment in course.get_assignments():
    if(ass_name == assignment.name):
        for sub in assignment.get_submissions():
            if(sub.user_id == students[0][2]):
                print(sub.score)
                score = input("Change Blanchard's score to: ")
                sub.edit(
                    submission = {
                        'posted_grade' : score
                    }
                )
                print(sub.score)
