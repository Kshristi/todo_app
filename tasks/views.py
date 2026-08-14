from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date, datetime

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
    current_hour= datetime.now().hour
    if current_hour < 12:
        greeting= "Good Morning"
    elif current_hour < 17:
        greeting= "Good Afternoon"
    else:
        greeting= "Good Evening"
    search_query=request.GET.get("search")
    filter_type=request.GET.get("filter","all")  
    sort_by=request.GET.get("sort","due_date") 
    category=request.GET.get("category","all")
    tasks=Task.objects.filter(user=request.user).order_by("completed", "due_date")
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
    if total_tasks>0:
        completion_percentage= int((completed_tasks / total_tasks)*100)
    else:
        completion_percentage=0

    pending_tasks=tasks.filter(completed=False).count()

    if sort_by=="due_date":
        tasks=tasks.order_by("completed","due_date")
    elif sort_by == "priority":
        tasks=tasks.order_by("completed","priority")
    elif sort_by == "newest":
        tasks=tasks.order_by("-id")
    elif sort_by == "alphabet":
        tasks=tasks.order_by("title")

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
        "completion_percentage": completion_percentage,
        "sort_by": sort_by,
        "greeting": greeting,
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