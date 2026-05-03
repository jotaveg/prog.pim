from django.contrib import admin

from .models import Post, Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'lead_professor', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('members',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'status', 'due_date')
    list_filter = ('status', 'project')
    search_fields = ('title', 'description')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('project', 'author', 'created_at')
    search_fields = ('body',)