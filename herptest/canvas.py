import os
from canvasapi import Canvas
from csv import reader
from canvasapi import assignment
from dotenv import load_dotenv
import requests
from . import grade_csv_uploader

class CanvasWrapper:
    def __init__(self, API_URL, env_path):
        self.canv_url = API_URL
        load_dotenv(env_path)
        self.canv_token = os.getenv("TOKEN")
        self.canv = Canvas(API_URL, self.canv_token)

    def get_courses(self):
        return self.canv.get_courses(enrollment_type='teacher')
    
    def get_assignments(self, course):
        return self.canv.get_course(course).get_assignments()

    def get_students(self, course):
        students = []
        for student in self.canv.get_course(course).get_users(enrollment_type='student'):
            students.append(student.name.split(' ') + [student.id])
        return students

    def get_results(self, path):
        results = []
        with open(path, 'r') as _summary:
            csv_reader = reader(_summary)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    results.append(row)
        return results

    def download_submissions(self, _course, assignment, path):
        for assn in self.get_assignments(list(course.id for course in self.get_courses() if course.name == _course)[0]):
            if(assignment == assn.name):
                print(assn.submissions_download_url)
                r = requests.get(assn.submissions_download_url, auth=grade_csv_uploader.BearerAuth(self.canv_token))
                open(path, 'wb').write(r.content)


    def push_grades(self, _course, assignment, path):
        for assn in self.get_assignments(list(course.id for course in self.get_courses() if course.name == _course)[0]):
            if(assignment == assn.name):
                for sub in assn.get_submissions():
                    for res in self.get_results(path):
                        if(str(sub.user_id) == res[1]):
                            print("Score of " + res[0] + ", ID: " + res[1] + " changed from " + str(sub.score) + " to " + str(float(res[2])) + ".")
                            sub.edit(
                                submission = {
                                    'posted_grade' : float(res[2])
                                }
                            )

def main():
    url = "https://ufl.instructure.com" #input("Enter canvas URL here: ")
    path = "canvas.env" #input("Enter env path: ")

    canvas = CanvasWrapper(url, path)

    #print([course for course in canvas.get_courses()])
    canvas.download_submissions("Sandbox: Blanchard", "PengTest", 'submissions.zip')
    #canvas.push_grades("Sandbox: Blanchard", "PengTest", "../../Test Suite/Results")

if __name__ == "__main__":
    main()
