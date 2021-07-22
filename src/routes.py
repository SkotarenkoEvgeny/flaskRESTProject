from flask import request
from flask_restful import Resource

from marshmallow import ValidationError

from src.models import Student, Course, Group
from src import api, db
from src.schemas import StudentSchema, GroupSchema, CourseSchema


class Smoke(Resource):
    def get(self):
        return {"message": "OK"}, 200


class StudentsView(Resource):

    student_schema = StudentSchema()

    def get(self, id=None):
        if id:
            student = Student.query.get_or_404(id)
            return self.student_schema.dump(student), 200
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
        groups = Group.query.all()
        return self.group_schema.dump(groups, many=True)


class CourseViews(Resource):

    course_schema = CourseSchema


api.add_resource(Smoke, "/smoke/")
api.add_resource(StudentsView, '/students/', '/students/<int:id>/',
                 strict_slashes=False)
api.add_resource(GroupsView, "/groups/", strict_slashes=False)
