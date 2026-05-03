from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView

from .models import Post, Project, Task
from .utils import get_user_role


class LandingView(TemplateView):
    template_name = 'core/landing.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role = get_user_role(user)

        if role == 'Administrator':
            projects = Project.objects.all()
        elif role == 'Professor':
            projects = Project.objects.filter(Q(lead_professor=user) | Q(members=user)).distinct()
        else:
            projects = Project.objects.filter(members=user)

        context.update(
            {
                'role': role,
                'projects': projects.select_related('lead_professor')[:5],
                'project_count': projects.count(),
                'task_count': Task.objects.filter(project__in=projects).count(),
                'post_count': Post.objects.filter(project__in=projects).count(),
            }
        )
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)
        queryset = Project.objects.select_related('lead_professor').prefetch_related('members')

        if role == 'Administrator':
            return queryset
        if role == 'Professor':
            return queryset.filter(Q(lead_professor=user) | Q(members=user)).distinct()
        return queryset.filter(members=user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'core/project_detail.html'

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)
        queryset = Project.objects.select_related('lead_professor').prefetch_related(
            'members',
            'tasks__assignee',
            'posts__author',
        )

        if role == 'Administrator':
            return queryset
        if role == 'Professor':
            return queryset.filter(Q(lead_professor=user) | Q(members=user)).distinct()
        return queryset.filter(members=user)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        project_ids = set(user.joined_projects.values_list('id', flat=True)) | set(user.led_projects.values_list('id', flat=True))
        context['role'] = get_user_role(user)
        context['project_count'] = len(project_ids)
        context['task_count'] = user.assigned_tasks.count()
        return context