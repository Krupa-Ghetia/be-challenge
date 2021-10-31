from django.shortcuts import get_object_or_404
from datetime import datetime

from subjects.models import Subjects


class SubjectsRepository:

    @staticmethod
    def create_subject(user, data):
        subject = Subjects.objects.create(name=data['name'], created_by_id=user.id)
        return subject

    @staticmethod
    def get_or_create_subject(user, name):
        subject = Subjects.objects.get_or_create(created_by_id=user.id, name=name)
        return subject

    @staticmethod
    def subject_already_exists(data):
        if Subjects.objects.filter(name=data['name']).exists():
            return True
        return False

    @staticmethod
    def get_subject_by_id(subject_id):
        return get_object_or_404(Subjects, id=subject_id)

    @staticmethod
    def get_all_subjects():
        return Subjects.objects.all()

    @staticmethod
    def update_subject(subject, data):
        subject.name = data['name']
        subject.row_last_updated = datetime.now()
        subject.save()

        return subject
