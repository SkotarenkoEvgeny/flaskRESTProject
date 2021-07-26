from flask import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from sqlalchemy import func

from src import api, db
from src.models import Course, Group, Student
from src.schemas import CourseSchema, GroupSchema, StudentSchema

parser = reqparse.RequestParser()
parser.add_argument('students')  # count of students
parser.add_argument('courses')  # list of students in course
parser.add_argument('del_course')  # delete course for student
parser.add_argument('add_course') # add course for student


class StudentsView(Resource):
    student_schema = StudentSchema()

    def get(self, id=None):
        args = parser.parse_args(strict=True)
        if not id:
            if raw_course := args['courses']:
                if course_id := Course.query.get(raw_course):
                    students = db.session.query(Student).filter(
                        Student.courses.contains(course_id)
                        ).all()
                else:
                    return {
                           'message': f"id course-{raw_course} not exist"
                        }, 400
            else:
                students = Student.query.all()
            return self.student_schema.dump(students, many=True), 200
        else:
            student = Student.query.get_or_404(id)
            return self.student_schema.dump(student), 200

    def post(self):
        try:
            student = self.student_schema.load(
                request.json, session=db.session
                )

        except ValidationError as v_error:
            return {"message": str(v_error)}, 400
        db.session.add(student)
        db.session.commit()
        return self.student_schema.dump(student), 201

    def put(self, id):
        args = parser.parse_args(strict=True)
        student = Student.query.get_or_404(id)

        if del_course := args['del_course']:
            if del_course.isdigit():
                if course := db.session.query(Course).get(del_course):
                    if course in student.courses:
                        student.courses.remove(course)
                        db.session.commit()
                        return {
                                   'message': f'successfully course {del_course} form st'
                                              f'udent id-{id} deleted'
                                   }, 200
                    else:
                        return {
                                   'message': f"'student id-{id} haven't course "
                                              f"{del_course}"
                                }, 400
            else:
                return {
                            'message': f"{del_course} not exist"
                        }, 400

        if add_course := args['add_course']:
            if add_course.isdigit():
                if course := db.session.query(Course).get(add_course):
                    if course not in student.courses:
                        student.courses.append(course)
                        db.session.commit()
                        return {
                                   'message': f'successfully added course'
                                              f' {add_course} form student id-{id}'
                                   }, 200
                    else:
                        return {'message': f'student id-{id} already signed up '
                                           f'for {add_course} '
                                   }, 400
            else:
                return {
                            'message': f"{add_course} not exist"
                        }, 400
        return {'message': 'bad request'}, 400




    def delete(self, id):
        if student := Student.query.get_or_404(id):
            db.session.delete(student)
            db.session.commit()
            return {'message': f'successfully id: {id} deleted'}, 200
        else:
            return {'message': f'id: {id} not exist'}, 404


class GroupsView(Resource):
    group_schema = GroupSchema()

    def get(self):
        print(1)
        args = parser.parse_args(strict=True)
        if students_count := args['students']:
            if students_count.isdigit() and int(students_count) > 0:
                groups = db.session.query(Group).join(Student).group_by(
                    Student.group_id
                    ).having(
                    func.count(Student.group_id) <= int(students_count)
                    ).all()
            else:
                return {'message': f'bad argument {students_count}'}, 400
        else:
            groups = Group.query.all()
        return self.group_schema.dump(groups, many=True), 200


class CourseViews(Resource):
    course_schema = CourseSchema()

    def get(self):
        courses = Course.query.all()
        return self.course_schema.dump(courses, many=True), 200


api.add_resource(
    StudentsView, '/students/', '/students/<int:id>/',
    strict_slashes=False
    )
api.add_resource(GroupsView, "/groups/", strict_slashes=False)
api.add_resource(CourseViews, "/courses/", strict_slashes=False)
