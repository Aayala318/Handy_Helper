from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        messages.success(request,'Successful Registration!')
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/jobs')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_jobs': Job.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id']),
        }
        return render(request,'jobs.html',context)

def new_job(request):
    context = {
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,"new.html",context)

def create_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else:
        user = User.objects.get(id=request.session["user_id"])
        job = Job.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            location = request.POST['location'],
            creator = user
        )
        return redirect(f'/jobs')

def show_one(request, job_id):
    context = {
        'job': Job.objects.get(id=job_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,"view.html",context)

def edit(request,job_id):
    context = {
        'job': Job.objects.get(id=job_id)
    }
    return render(request,'edit.html',context)

def update(request, job_id):
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/jobs/{job_id}/edit')
    else:
        job = Job.objects.get(id=job_id)
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.location = request.POST['location']
        job.save()
    return redirect(f'/jobs')

def delete(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()
    return redirect(f'/jobs')

def logout(request):
    request.session.flush()
    return redirect('/')