import json
import os
import unittest

from src import app, db
from src.config import BASE_DIR
from src.models import Course, Group, Student


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            BASE_DIR, 'test.db'
            )
        self.app = app.test_client()
        db.create_all()
        for item in ('AA-11', 'AA-22'):
            db.session.add(Group(group_name=item))
        for item in ('math', 'biology'):
            db.session.add(Course(course_name=item))
        student_1 = Student(
            first_name='first_name_1', last_name='last_name_1',
            group_id=1
            )
        student_2 = Student(
            first_name='first_name_2', last_name='last_name_2',
            group_id=1
            )
        for item in Course.query.all():
            student_1.courses.append(item)
            if item.id == 1:
                student_2.courses.append(item)
        db.session.add(student_1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Group(self):
        response = self.app.get('/groups/')
        resp = response.json
        self.assertEqual(resp[0]['group_name'], 'AA-11')

    def test_Course(self):
        response = self.app.get('/courses/')
        resp = response.json
        self.assertEqual(resp[0]['course_name'], 'math')

    def test_Student(self):
        response = self.app.get('/students/1')
        resp = response.json
        self.assertEqual(resp['first_name'], 'first_name_1')

    def test_Student_list(self):
        response = self.app.get('/students/')
        resp = response.json
        self.assertEqual(resp[0]['first_name'], 'first_name_1')

    def test_2_Students_in_Course(self):
        response = self.app.get('/students/?courses=1')
        resp = response.json
        resp.sort(key=lambda j: j['id'])
        self.assertEqual(resp[0]['first_name'], 'first_name_1')
        self.assertEqual(resp[1]['first_name'], 'first_name_2')

    def test_1_Student_dell_Course(self):
        self.app.put('/students/2?del_course=1')
        response = self.app.get('/students/?courses=1')
        resp = response.json
        self.assertEqual(resp[0]['first_name'], 'first_name_1')
        self.assertEqual(len(resp), 1)

    def test_Add_Student(self):
        student = {
            "last_name": "Jenning", "group_id": 2,
            "first_name": "Kadin"
            }
        response = self.app.post(
            '/students/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(student)
            )
        resp = response.json
        self.assertEqual(resp['first_name'], 'Kadin')


if __name__ == '__main__':
    unittest.main()
