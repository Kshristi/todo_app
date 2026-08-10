from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date

def home(request):
    if request.method=="POST":
        title=request.POST.get("title")
        due_date=request.POST.get("due_date")
        priority=request.POST.get("priority")
        Task.objects.create(title=title, due_date=due_date,priority=priority)
        return redirect("home")
    
        
    tasks=Task.objects.all()
    search_query=request.GET.get("search")
    if search_query:
        tasks=Task.objects.filter(title__icontains=search_query)
    else:
        tasks=Task.objects.all()
        
    total_tasks=tasks.count()
    completed_tasks=tasks.filter(completed=True).count()
    pending_tasks=tasks.filter(completed=False).count()

    today=date.today()
    for task in tasks:
        if task.due_date:
            task.is_overdue= task.due_date < today
            task.is_today= task.due_date == today
        else:
            task.is_overdue= False
            task.is_today= False
    overdue_tasks=tasks.filter(due_date__lt=today, completed=False).count()

    context={
        "tasks":tasks,
        "today": date.today(),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "search_query": search_query
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
        task.due_date=request.POST.get("due_date")
        task.priority=request.POST.get("priority")
        task.save()
        return redirect('home')
    return render(request,"tasks/edit.html",{"task":task})