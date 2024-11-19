from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Главная страница с задачами
def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

# Добавление задачи
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача добавлена!')
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'edit.html', {'form': form})

# Редактирование задачи
def edit_task(request, task_id):
    if task_id:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = None
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача обновлена!')
            return redirect('index')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit.html', {'form': form})

# Удаление задачи
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.error(request, 'Задача удалена!')
    return redirect('index')

# Переключение статуса задачи
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_done = not task.is_done
    task.save()
    return redirect('index')
