from flask import request
from flask_restful import Resource, reqparse

from marshmallow import ValidationError

from sqlalchemy import func

from src.models import Student, Course, Group
from src import api, db
from src.schemas import StudentSchema, GroupSchema, CourseSchema


parser = reqparse.RequestParser()
parser.add_argument('students')  # count of students
parser.add_argument('courses') # list of students in course


class Smoke(Resource):
    def get(self):
        return {"message": "OK"}, 200


class StudentsView(Resource):

    student_schema = StudentSchema()

    def get(self, id=None):

        args = parser.parse_args(strict=True)

        if id:
            student = Student.query.get_or_404(id)
            return self.student_schema.dump(student), 200
        elif raw_course := args['courses']:
            course_id = Course.query.filter(
                    Course.course_name == raw_course
                    ).first()
            students = db.session.query(Student).filter(
                    Student.courses.contains(course_id)
                    ).all()
        else:
            students = Student.query.all()
        return self.student_schema.dump(students, many=True), 200

    def post(self):
        try:
            student = self.student_schema.load(request.json, session=db.session)
        except ValidationError as v_error:
            return {"message": str(v_error)}, 400
        db.session.add(student)
        db.session.commit()
        return self.student_schema.dump(student), 201

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
        args = parser.parse_args(strict=True)
        if students_count := args['students']:
            print(students_count.isdigit())
            print(int(students_count) > 0)
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


api.add_resource(Smoke, "/smoke/")
api.add_resource(StudentsView, '/students/', '/students/<int:id>/',
                 strict_slashes=False)
api.add_resource(GroupsView, "/groups/", strict_slashes=False)
api.add_resource(CourseViews, "/courses/",  strict_slashes=False)
