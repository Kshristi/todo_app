from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date

def home(request):
    if request.method=="POST":
        title=request.POST.get("title")
        due_date=request.POST.get("due_date")
        Task.objects.create(title=title, due_date=due_date)
        return redirect("home")
    
    tasks=Task.objects.all()
    today=date.today()
    for task in tasks:
        if task.due_date:
            task.is_overdue= task.due_date < today
            task.is_today= task.due_date == today
        else:
            task.is_overdue= False
            task.is_today= False

    context={
        "tasks":tasks,
        "today": date.today(),
    }

    return render(request, "tasks/home.html", context)

def delete_task(request, id):
    task=get_object_or_404(Task,id=id)
    task.delete()
    return redirect('home')

def complete_task(request, id):
    task=get_object_or_404(Task,id=id)
    task.completed= not task.completed
    task.save()
    return redirect('home')

def edit_task(request, id):
    task=get_object_or_404(Task,id=id)

    if request.method=="POST":
        task.title=request.POST.get("title")
        task.save()
        return redirect('home')
    return render(request,"tasks/edit.html",{"task":task})