from src import db

student_course_association = db.Table(
    'student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('courses_id', db.Integer, db.ForeignKey('courses.id'))
    )


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    group = db.relationship('Group', back_populates="students")
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    courses = db.relationship(
        "Course",
        secondary=student_course_association,
        back_populates="students"
        )

    def __repr__(self):
        return f"{self.id}-{self.first_name}-{self.last_name}"


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String, nullable=False)
    students = db.relationship('Student', back_populates="group")

    def __repr__(self):
        return f"{self.id}-{self.group_name}"


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String, nullable=False)
    students = db.relationship(
        "Student",
        secondary=student_course_association,
        back_populates="courses"
        )

    def __repr__(self):
        return f"{self.id}-{self.course_name}"
