from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task



def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})


def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'todo_app/add_task.html')


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()
        return redirect('task_list')
    return render(request, 'todo_app/edit_task.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')
