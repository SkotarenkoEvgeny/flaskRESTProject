import string
from random import choice, randint, sample

from src import db
from src.models import Course, Group, Student

courses = ('math', 'biology', 'physics',
           'chemistry', 'statistics',
           'computer science', 'draw',
           'data bases', 'python', 'python advanced')

with open('names.txt', 'r') as file_names:
    names = [name[:-2].split(' ') for name in file_names.readlines()]

first_names = [i[0] for i in names]
last_names = [i[1] for i in names]

# course generation
for item in courses:
    if not Course.query.filter_by(course_name=item).first():
        db.session.add(Course(course_name=item))

# group generation
# create empty group for students, who not in any group
empty_group = Group(group_name="empty")
db.session.add(empty_group)
# create groups
for _ in range(20):
    group_number = f"{choice(string.ascii_uppercase)}" \
                   f"{choice(string.ascii_uppercase)}-" \
                   f"{choice(string.digits)}" \
                   f"{choice(string.digits)}"
    if not Group.query.filter_by(group_name=group_number).first():
        db.session.add(Group(group_name=group_number))

student_count = 200
group_count = 40  # set 20 at the last

while student_count != 0:
    first_name = choice(first_names)
    last_name = choice(last_names)
    student_query = Student.query.filter(
        db.and_(
            Student.first_name == first_name,
            Student.last_name == last_name
            )
        ).first()
    if not student_query:
        ch = choice([True, True, True, True, False])
        # randomly add curses to student
        student_course = sample(courses, randint(0, len(courses) - 1))
        print(student_course)
        if ch:
            group = choice(Group.query.all())
            student = Student(
                first_name=first_name,
                last_name=last_name,
                group_id=group.id
                )
        else:
            student = Student(
                first_name=first_name, last_name=last_name,
                group_id=empty_group.id
                )
        db.session.add(student)
        print(student)
        for item in student_course:
            student.courses.append(
                Course.query.filter_by(course_name=item).first()
                )

    # randomly add curses to student
    student_count -= 1

db.session.commit()
