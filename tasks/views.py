from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def home(request):
    if request.method=="POST":
        title=request.POST.get("title")
        Task.objects.create(title=title)
        return redirect("home")
    
    tasks=Task.objects.all()

    context={
        "tasks":tasks
    }

    return render(request, "tasks/home.html", context)

def delete_task(request, id):
    task=get_object_or_404(Task,id=id)
    task.delete()
    return redirect('home')

def complete_task(request, id):
    task=get_object_or_404(Task,id=id)
    task.completed=True
    task.save()
    return redirect('home')

def edit_task(request, id):
    task=get_object_or_404(Task,id=id)

    if request.method=="POST":
        task.title=request.POST.get("title")
        task.save()
        return redirect('home')
    return render(request,"tasks/edit.html",{"task":task})