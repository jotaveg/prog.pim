import os
import sys
from datetime import timedelta

if __name__ == '__main__' and 'DJANGO_SETTINGS_MODULE' not in os.environ:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pim.settings')

import django

django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import Post, Project, Task


User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with demo users, projects, tasks, and posts.'

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='Administrator')
        professor_group, _ = Group.objects.get_or_create(name='Professor')
        student_group, _ = Group.objects.get_or_create(name='Student')

        admin_user, created = User.objects.get_or_create(
            username='admin_demo',
            defaults={'email': 'admin@example.com', 'first_name': 'Admin', 'last_name': 'Demo'},
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        admin_user.groups.add(admin_group)

        professor_one, created = User.objects.get_or_create(
            username='professor_ana',
            defaults={'email': 'ana@example.com', 'first_name': 'Ana', 'last_name': 'Silva'},
        )
        if created:
            professor_one.set_password('prof123')
            professor_one.save()
        professor_one.groups.add(professor_group)

        professor_two, created = User.objects.get_or_create(
            username='professor_carlos',
            defaults={'email': 'carlos@example.com', 'first_name': 'Carlos', 'last_name': 'Mendes'},
        )
        if created:
            professor_two.set_password('prof123')
            professor_two.save()
        professor_two.groups.add(professor_group)

        students = []
        for username, first_name in [
            ('student_luiza', 'Luiza'),
            ('student_joao', 'João'),
            ('student_maria', 'Maria'),
            ('student_pedro', 'Pedro'),
        ]:
            student, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com', 'first_name': first_name, 'last_name': 'Aluno'},
            )
            if created:
                student.set_password('student123')
                student.save()
            student.groups.add(student_group)
            students.append(student)

        projects = [
            {
                'title': 'Pesquisa em IA Educacional',
                'description': 'Projeto colaborativo sobre aplicações de IA no ensino básico.',
                'lead': professor_one,
                'members': students[:3],
            },
            {
                'title': 'Laboratório de Desenvolvimento Web',
                'description': 'Espaço para documentar sprints, tarefas e entregas da turma.',
                'lead': professor_two,
                'members': students[1:],
            },
        ]

        for project_data in projects:
            project, _ = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    'description': project_data['description'],
                    'lead_professor': project_data['lead'],
                },
            )
            project.description = project_data['description']
            project.lead_professor = project_data['lead']
            project.save()
            project.members.set(project_data['members'])

            Task.objects.get_or_create(
                project=project,
                title='Definir escopo inicial',
                defaults={
                    'description': 'Organizar objetivos, cronograma e entregáveis do projeto.',
                    'assignee': project_data['members'][0],
                    'created_by': project_data['lead'],
                    'status': Task.Status.DOING,
                    'due_date': timezone.now().date() + timedelta(days=7),
                },
            )
            Task.objects.get_or_create(
                project=project,
                title='Criar protótipo visual',
                defaults={
                    'description': 'Montar o layout principal com navegação superior.',
                    'assignee': project_data['members'][1],
                    'created_by': project_data['lead'],
                    'status': Task.Status.TODO,
                    'due_date': timezone.now().date() + timedelta(days=10),
                },
            )

            Post.objects.get_or_create(
                project=project,
                author=project_data['lead'],
                body='Bem-vindos ao projeto. Vamos organizar as primeiras atividades nesta semana.',
            )
            Post.objects.get_or_create(
                project=project,
                author=project_data['members'][0],
                body='Já revisei a documentação e posso ajudar na estrutura do dashboard.',
            )

        self.stdout.write(self.style.SUCCESS('Demo data created successfully.'))