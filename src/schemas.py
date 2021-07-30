from marshmallow_sqlalchemy import SQLAlchemySchema

from src.models import Course, Group, Student


class StudentSchema(SQLAlchemySchema):
    class Meta:
        model = Student
        load_instance = True
        fields = ['id', 'first_name', 'last_name', 'group_id']


class CourseSchema(SQLAlchemySchema):
    class Meta:
        model = Course
        load_instance = True
        fields = ['id', 'course_name']


class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True
        fields = ['id', 'group_name']
