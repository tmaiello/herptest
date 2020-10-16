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

for assignment in course.get_assignments():
    if assignment.name == ass_name:
        print(assignment.name)