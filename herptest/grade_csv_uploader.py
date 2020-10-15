__author__ = "Boris Ermakov-Spektor, Adapted by: Tyler Maiello"

import os
import requests
import csv
import json
from dotenv import load_dotenv
import sys


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, r: requests.Request):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


class Rubric:
    def __init__(self):
        self.criteria: list[Criterion] = []
        self.id = ""

    class Criterion:
        def __init__(self):
            self.ratings: list[Rating] = []
            self.id = ""

        class Rating:
            def __init__(self):
                self.points = 0
                self.id = ""


class Student:
    def __init__(self):
        self.last_name = ""
        self.first_name = ""
        self.grade = 0
        self.rubric: list[(float, str)] = []

    def __str__(self):
        print(f"Last Name: {self.last_name}")
        print(f"First Name: {self.last_name}")
        print(f"Grade: {self.last_name}")
        print(f"Rubric: {self.rubric}")


class CanvasUtil:
    def __init__(self):
        self.canvas_api_url = "https://ufl.beta.instructure.com/api/v1"
        load_dotenv()  # load token from .env file
        self.token = os.getenv("TOKEN")

    def get_courses_this_semester(self) -> dict:
        """
        Get dictionary (name -> id) of courses in this semester
        """
        response = requests.get(f"{self.canvas_api_url}/courses?enrollment_type=ta", auth=BearerAuth(self.token))
        content = response.json()
        enrollment_term_id = content[0]["enrollment_term_id"]
        for course in content:  # Find the current enrollment term
            enrollment_term_id = max(enrollment_term_id, int(course["enrollment_term_id"]))
        # Filter for courses in the current term
        result = {}
        for course in content:
            if course["enrollment_term_id"] == enrollment_term_id:
                result[course["name"]] = int(course["id"])

        return result

    def get_section_ids(self, course_id: str) -> list:
        """
        Get a list of all section IDs in a specific course
        """
        response = requests.get(f"{self.canvas_api_url}/courses/{course_id}/sections", auth=BearerAuth(self.token))
        content = response.json()
        section_ids = []
        for section in content:
            section_ids.append(section["id"])
        return section_ids

    def get_assignment_id_by_name(self, course_id: str, assignment_name: str) -> str:
        """
        Get the id of the first assignment with a name that matches the input
        """
        response = requests.get(f"{self.canvas_api_url}/courses/{course_id}/assignments", auth=BearerAuth(self.token))
        content = response.json()
        for assignment in content:

            if str(assignment["name"]).lower().count(assignment_name.lower()):
                print(f"Found assignment: {assignment['name']}")
                return str(assignment["id"])

        raise Exception("ERROR: No matching assignment found!")

    def get_student_ids_by_section(self, course_id: str, section_id: str, results: dict):
        """
        Get list of students from a particular section (by Canvas supplied Section ID) and store them in the dictionary
        """
        response = requests.get(f"{self.canvas_api_url}/courses/{course_id}/sections/{section_id}?include[]=students",
                                auth=BearerAuth(self.token))
        content = response.json()
        student_ids = []
        if content["students"] is not None:
            for student in content["students"]:
                results[str(student["name"]).lower()] = student["id"]

    def get_rubric_id(self, course_id: str, assignment_id: str) -> str:
        response = requests.get(f"{self.canvas_api_url}/courses/{course_id}/assignments/{assignment_id}",
                                auth=BearerAuth(self.token))
        content = response.json()
        return content["rubric_settings"]["id"]

    def generate_rubric(self, course_id: str, rubric_id: str) -> Rubric:
        result_rubric = Rubric()
        result_rubric.id = rubric_id

        response = requests.get(f"{self.canvas_api_url}/courses/{course_id}/rubrics/{rubric_id}",
                                auth=BearerAuth(self.token))
        content = response.json()

        criteria_data = content["data"]

        for criterion in criteria_data:
            temp_criterion = Rubric.Criterion()
            temp_criterion.id = criterion["id"]
            rating_data = criterion["ratings"]

            for rating in rating_data:
                temp_rating = Rubric.Criterion.Rating()
                temp_rating.id = rating["id"]
                temp_rating.points = float(rating["points"])
                temp_criterion.ratings.append(temp_rating)

            result_rubric.criteria.append(temp_criterion)

        return result_rubric

    def populate_students_from_csv(self, csv_path: str) -> list:
        students = []
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            column_end_index = -1
            for i, row in enumerate(csv_reader):
                if i == 0:
                    for j, val in enumerate(row):
                        if val == "Total Left":
                            column_end_index = j
                            break
                else:
                    student = Student()
                    name = str(row[0]).split(',')
                    student.last_name = name[0].strip()
                    student.first_name = name[1].strip()
                    for i in range(2, column_end_index, 2):
                        try:
                            grade = float(row[i])
                        except:
                            grade = 0
                        student.rubric.append((grade, row[i + 1]))
                    students.append(student)

        return students

    def upload_grades(self, course_id: str, user_ids: dict, assignment_id: str, students_from_file: list,
                      rubric: Rubric):
        counter = 0

        for student in students_from_file:
            student_name = f"{student.first_name} {student.last_name}".lower()

            if student_name in user_ids:
                gradeURI = f"{self.canvas_api_url}/courses/{course_id}/assignments/{assignment_id}/submissions/{user_ids[student_name]}"

                response = requests.get(gradeURI, auth=BearerAuth(self.token))
                content = response.json()

                # PROMPT WHEN OVERWRITING GRADES
                if content["grade"] is not None:
                    print(f"{student_name}: grade not null!")
                    print("Confirm grade replacement with 'Y'.")
                    if input().lower() != 'y':
                        sys.exit(0)

                payload = {}

                if len(student.rubric) != len(rubric.criteria):
                    raise Exception("Criteria length mismatch!")

                for i, criterion in enumerate(rubric.criteria):
                    payload[f"rubric_assessment[{criterion.id}][points]"] = student.rubric[i][0]
                    payload[f"rubric_assessment[{criterion.id}][comments]"] = str(student.rubric[i][1])
                    rating_id_chosen = ""
                    for j, rating in enumerate(criterion.ratings):
                        if criterion.ratings[j].points <= student.rubric[i][0]:
                            rating_id_chosen = criterion.ratings[j].id
                            break
                    payload[f"rubric_assessment[{criterion.id}][rating_id]"] = rating_id_chosen

                response = requests.put(gradeURI, params=payload, auth=BearerAuth(self.token))

                counter = counter + 1
                print(f"{counter} student(s) graded.")


def main():
    canvas_util = CanvasUtil()

    courses = canvas_util.get_courses_this_semester()
    course_names = list(courses.keys())
    print("***Which course are you choosing? (enter number, 0 indexed)")
    temp_count = 0
    for name in course_names:
        print(f"{temp_count}. {name}")
        temp_count = temp_count + 1
    index_choice = input()
    course_id = courses[course_names[int(index_choice)]]

    section_ids = canvas_util.get_section_ids(course_id)
    print(f"{len(section_ids)} section(s) found")

    print("***Type some part of the title of your assignment - if it's \"Python Pitches\", type \"Pitches\"")
    assignment_name = input()

    assignment_id = canvas_util.get_assignment_id_by_name(course_id, assignment_name)
    print(f"Found assignment ID: {assignment_id}")

    user_ids = {}
    for section in section_ids:
        canvas_util.get_student_ids_by_section(course_id, section, user_ids)

    print("***Please input path of CSV file:")
    csv_path = input()
    students_from_file = canvas_util.populate_students_from_csv(csv_path)

    rubric_id = canvas_util.get_rubric_id(course_id, assignment_id)
    rubric_format = canvas_util.generate_rubric(course_id, rubric_id)

    canvas_util.upload_grades(course_id, user_ids, assignment_id, students_from_file, rubric_format)


if __name__ == "__main__":
    main()