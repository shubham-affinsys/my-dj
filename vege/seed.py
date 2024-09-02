from faker import Faker
import random
from .models import *
from .serializer import *
fake = Faker()


def create_subject_marks():
    try:
        student_objs = Student.objects.all()
        subjects = Subject.objects.all()
        print(student_objs.count(), subjects.count())

        for student in student_objs:
            for subject in subjects:
                print(subject)
                print(student)
                print("inserted")
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(0, 100)
                )
    except Exception as e:
        print(e)


def seed_db(n=10) -> None:
    try:
        for _ in range(n):
            department_objs = Department.objects.all()
            random_idx = random.randint(0, len(department_objs) - 1)
            department = department_objs[random_idx]

            student_id = f'STU-0{random.randint(100, 999)}'
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(18, 30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)
            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address
            )
    except Exception as e:
        print(e)
def insert_todo():
    for i in range (10):
        todo_title = random.randint(0,1000)
        todo_d = fake.sentence()
        data = {'user': 'shubham', 'todo_title': f'taks {todo_title}', 'todo_description': todo_d}
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

