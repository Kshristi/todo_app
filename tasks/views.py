from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date

@login_required
def home(request):
    if request.method=="POST":
        title=request.POST.get("title")
        due_date=request.POST.get("due_date")
        priority=request.POST.get("priority")
        category=request.POST.get("category")
        Task.objects.create(user=request.user, title=title, due_date=due_date,priority=priority,category=category)
        return redirect("home")

    today=date.today()
    search_query=request.GET.get("search")
    filter_type=request.GET.get("filter","all")  
    category=request.GET.get("category","all")
    tasks=Task.objects.filter(user=request.user)
    if search_query:
        tasks=tasks.filter(title__icontains=search_query)
    if filter_type=="pending":
        tasks=tasks.filter(completed=False)
    elif filter_type=="completed":
        tasks=tasks.filter(completed=True)
    elif filter_type=="overdue":
        tasks=tasks.filter(due_date__lt=today, completed=False)

    if category!= "all":
        tasks=tasks.filter(category=category)

    total_tasks=tasks.count()
    completed_tasks=tasks.filter(completed=True).count()
    pending_tasks=tasks.filter(completed=False).count()
            
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
        "search_query": search_query,
        "filter_type": filter_type,
        "category": category,
    }

    return render(request, "tasks/home.html", context)

def delete_task(request, id):
    task=get_object_or_404(Task,id=id, user= request.user)
    task.delete()
    return redirect('home')

def complete_task(request, id):
    task=get_object_or_404(Task,id=id, user=request.user)
    task.completed= not task.completed
    task.save()
    return redirect('home')

def edit_task(request, id):
    task=get_object_or_404(Task,id=id, user=request.user)

    if request.method=="POST":
        task.title=request.POST.get("title")
        task.due_date=request.POST.get("due_date")
        task.priority=request.POST.get("priority")
        task.category=request.POST.get("category")
        task.save()
        return redirect('home')
    return render(request,"tasks/edit.html",{"task":task})