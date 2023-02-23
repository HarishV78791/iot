from django.shortcuts import render, redirect, reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.views import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.views import (PasswordChangeView, 
                                        PasswordResetView, 
                                        PasswordResetConfirmView)
from django.contrib.messages.views import SuccessMessageMixin
from iot.settings import EMAIL_HOST_USER
from django.http import JsonResponse
from django.utils.timezone import utc
import pytz
from .models import  FromMicroController, ProjectModel
from .forms import FromMcForm, UserRegistrationForm, ProjectCreationForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def usercreation(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('node:login')
    else:
        form = UserCreationForm()

    content = {'form':form}
    return render(request, 'registeration.html', content)


def register(request):
    if request.user.is_authenticated:
        name = str(request.user.is_authenticated)
        messages.success(
                request, f'{name} is already logged in. Logout to create a new user.')
        return redirect('node:login') 
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.email = email
            user.save()
            messages.success(
                request, f'Your registration for {email} is successfully created.')
            return redirect('node:login')
    else:
        form = UserRegistrationForm()

    content = {'form':form}
    return render(request, 'registeration.html', content)


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    success_url = reverse_lazy('node:project')
    template_name="password_change.html"
    success_message = "Password has been changed successfully"


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    success_url = reverse_lazy('node:login')
    template_name='password_reset_form.html'
    email_template_name = 'password_reset_email.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            em = form.cleaned_data.get('email')
            if User.objects.filter(email= em).exists():
                messages.success(request, f'A link to reset your account password has been sent to {em}.')
                return self.form_valid(form)
            else:
                messages.warning(request, f'Entered email id:- {em} is not registered. Please check with the mail id or register your account.')
                return self.form_invalid(form)

        else:
            return self.form_invalid(form)


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('node:login')
    template_name = 'password_reset_confirm.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, f'Your password reset successful')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def project_list(request):
    projects = ProjectModel.objects.filter(user=request.user).order_by('-id')
    content = {'projects':projects}
    return render(request, 'projects.html', content)


@login_required
def createProject(request):
    if request.method == "POST":
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            user = request.user
            project.user = user
            project.save()
            messages.success(
                request, f'Project is successfully created.')
            return redirect('node:project')
    else:
        form = ProjectCreationForm()

    content = {'form':form}
    return render(request, 'create_project.html', content)


@login_required
def updateProject(request, pk):
    try:
        project = ProjectModel.objects.get(pk=pk)
        user = project.user
        login_user = request.user
        if user!=login_user:
            return redirect('node:project')
    except:
        return redirect('node:project')
    if request.method == "POST":
        form = ProjectCreationForm(request.POST, instance=ProjectModel.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Project is successfully updated.')
            return redirect('node:project')
    else:
        form = ProjectCreationForm(instance=ProjectModel.objects.get(pk=pk))

    content = {'form':form}
    return render(request, 'update_project.html', content)



@login_required
def viewProject(request, pk):
    try:
        project = ProjectModel.objects.get(pk=pk)
        user = project.user
        login_user = request.user
        if user!=login_user:
            return redirect('node:project')
    except:
        return redirect('node:project')
    content={'project':project}
    return render(request,'view_project.html',content )


@login_required
def deleteConfirmProject(request, pk):
    try:
        project = ProjectModel.objects.get(pk=pk)
        user = project.user
        login_user = request.user
        if user!=login_user:
            return redirect('node:project')
    except:
        return redirect('node:project')
    content={'project':project}
    return render(request,'delete_confirm.html',content )


@login_required
def deleteProject(request, pk):
    try:
        project = ProjectModel.objects.get(pk=pk)
        user = project.user
        login_user = request.user
        if user!=login_user:
            messages.warning(request,f'You are not authorised to delete the project')
            return redirect('node:project')
    except:
        messages.warning(request,f'You are not authorised to delete the project')
        return redirect('node:project')
    project.delete()
    messages.warning(request,f'{project.name} has been deleted sucessfully')
    return redirect('node:project')


def project_api_write(request):
    api = request.GET.get('API', '')
    project_id = request.GET.get('id', '')
    if project_id=='':
        data = {'info':'Error in the data received'}
        return JsonResponse(data)
    else:
        try:
            project = ProjectModel.objects.get(id=project_id)
            API = project.write_api
            email_id = project.email
        except:
            data = {'info':'Error in the data received'}
            return JsonResponse(data)
    if api != API:
        recipient_list = [email_id,]
        message = f'Alert! Please Check your security for {project.name}'
        subject = f'Alert! Please Check your security for {project.name} message'
        from_email = EMAIL_HOST_USER
        context = {'name':project.user.first_name,
                    'projectName':project.name,
                    }
        html_content = render_to_string('alert_email.html',context)
        mail = EmailMultiAlternatives(subject,message,from_email,recipient_list, reply_to=['test@iot.in'])
        mail.attach_alternative(html_content,"text/html")
        try:
            mail.send()
        except:
            pass
            # messages.warning(request, f'Sorry, Unable to send mail. Try aftersome time.')
        data = {'status_code':406,
                'info':'You are not authorised'}
        return JsonResponse(data)

    form = FromMcForm(request.GET)
    if form.is_valid():
        frommc = form.save(commit=False)
        frommc.project = project
        frommc.save()
        data = {'info':'Data Stored on Data Base'}
        return JsonResponse(data)
    else:
        data = {'info':'Error in the data received'}
        return JsonResponse(data)


@login_required
def plot_graph(request, pk):
    try:
        project = ProjectModel.objects.get(pk=pk)
        user = project.user
        login_user = request.user
        if user!=login_user:
            messages.warning(request,f'You are not authorised to view the project')
            return redirect('node:project')
    except:
        pass
    datas = FromMicroController.objects.filter(project_id=pk).values('data','date').order_by('-id')[:40]
    tz = pytz.timezone('Asia/Kolkata')
    field_data=[]
    date =[]
    for mc in datas:
        field_data.append(mc['data'])
        date.append(mc['date'].replace(tzinfo=tz).strftime('%d-%m-%Y %H:%M:%S'))
    field_data.reverse()
    date.reverse()
    data={'field_data':field_data,
            'date':date}
    
    return JsonResponse(data)


