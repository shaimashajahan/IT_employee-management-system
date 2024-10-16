import random
import string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from calendar import monthrange
from .models import Usermember,CustomUser,project,module,project_TL,module_dev,teamlead,P_progress,m_progress
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import date,datetime,timedelta
import re
from tkinter import *
from tkinter import messagebox
from django.db.models.functions import Coalesce
import pandas as pd
from django.db.models import Q
from django.db.models import F
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime , timedelta


def print_dates(start_date, end_date):
    while start_date <= end_date:
        print(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)
def add_project(request):
    if request.method == 'POST':
        topic=request.POST['topic']
        desc=request.POST['desc']
        requr=request.POST['requi']
        modul=request.POST['modul']
        guidelines=request.FILES.get('file')
        sdate = request.POST['sdate']
        edate = request.POST['edate']
        c_name=request.POST['c_name']
        c_addr=request.POST['c_addr']
        c_contact=request.POST['c_contact']
        c_email=request.POST['c_email'] 
        if not sdate or not edate:
            messages.error(request, 'Start and end dates are required')
            return redirect('assign_project')
        try:
            # Attempt to parse dates
            startdate = datetime.strptime(sdate, "%Y-%m-%d")
            enddate = datetime.strptime(edate, "%Y-%m-%d")
        except ValueError:
            # Handle invalid date format
            messages.error(request, 'Invalid date format. Use YYYY-MM-DD')
            return redirect('assign_project')
        else:
            projectassign=project(topic=topic,desc=desc,requirement=requr,modules=modul,cl_name=c_name,cl_address=c_addr,cl_contact=c_contact,cl_email=c_email,file=guidelines,start_date=startdate,end_date=enddate)
            projectassign.save()
            messages.info(request,'Project Added')
        return redirect('assign_project')
def add_modulefun(request):
    if request.method == 'POST':
        uid=request.user.id
        project_name =request.POST['sel_pr']
        pr_name=project_TL.objects.get(id=project_name)
        module_name=request.POST['module_name']
        requirement=request.POST['requir']
        attachment=request.FILES.get('file')
        sdate=request.POST['sdate']
        edate=request.POST['edate']    
        currentdate = datetime.today()
        dateend = edate
        team=CustomUser.objects.get(id=uid)
      
        if not sdate or not edate:
            messages.error(request, 'Start and end dates are required')
            return redirect('add_module')
        try:
            # Attempt to parse dates
            startdate = datetime.strptime(sdate, "%Y-%m-%d")
            enddate = datetime.strptime(edate, "%Y-%m-%d")
        except ValueError:
            # Handle invalid date format
            messages.error(request, 'Invalid date format. Use YYYY-MM-DD')
            return redirect('add_module')
        else:
            moduleassign=module(module_name=module_name,requirement=requirement,file=attachment,start_date=startdate,end_date=enddate,pro=pr_name,team=team)
            moduleassign.save()
            messages.info(request,'Module Assigned')    
        return redirect('add_module')
        
def calendar(request, id, tlid):
    try:
        print('admin id',id)
        print('admin tlid',tlid)
        prtl = project_TL.objects.get(team_lead_id=tlid, project_name_id=id)
        print('admin prtl',prtl)
        TL = Usermember.objects.all()
        co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
        cou = co.count()
        
        if prtl:
            project_start = prtl.project_name.start_date
            project_end = prtl.project_name.end_date
           
            dates = []
            current_date = project_start
            while current_date <= project_end:
                dates.append({
                    'date': current_date.strftime("%Y-%m-%d"),
                    'datep':current_date,
                    'day': current_date.strftime("%A"),
                    'year': current_date.year,
                    'month': current_date.strftime("%B"),
                    'is_new_month': current_date.day == 1,
                    'is_last_date': False
                })
                current_date += timedelta(days=1)
            
            for i, date in enumerate(dates):
                if i == len(dates) - 1 or dates[i+1]['is_new_month']:
                    date['is_last_date'] = True
            year1 = project_start.year
            month1 = project_start.strftime("%B")

            prog=P_progress.objects.filter(p_tl__project_name__id =id,p_tl__team_lead__id = tlid)
            print('prog',prog)
            return render(request, 'calendar.html', {
                'id': id,
                'tlid': tlid,
                'project_dates': dates,
                'y':year1,
                'm':month1,
                'cou':cou,
                'prtl':prtl,
                'prog':prog,

                            
            })
    
    except project_TL.DoesNotExist:
        print("Project team lead not found")
        return render(request, 'error.html', {'error_message': 'Project team lead not found'})
def tl_ppworkprogress(request,id):
    try:
        uid=request.user.id
        prtl = project_TL.objects.get(team_lead__user__id=uid, project_name__id=id)
        t= Usermember.objects.get(user=uid)
        pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()

        if prtl:
            project_start = prtl.project_name.start_date
            project_end = prtl.project_name.end_date
            
            dates = []
            current_date = project_start
            while current_date <= project_end:
                dates.append({
                    'date': current_date.strftime("%Y-%m-%d"),
                    'datep':current_date,
                    'day': current_date.strftime("%A"),
                    'year': current_date.year,
                    'month': current_date.strftime("%B"),
                    'is_new_month': current_date.day == 1,
                    'is_last_date': False
                })
                current_date += timedelta(days=1)
            
            for i, date in enumerate(dates):
                if i == len(dates) - 1 or dates[i+1]['is_new_month']:
                    date['is_last_date'] = True
            year1 = project_start.year
            month1 = project_start.strftime("%B")
            prog=P_progress.objects.filter(p_tl__project_name__id =  id, p_tl__team_lead__user__id = uid)
            print('prog',prog)
            return render(request, 'tl_ppworkprogress.html', {
                'uid':uid,
                'id': id,
                'project_dates': dates,
                'y':year1,
                'm':month1,
                't':t,
                'pcount':pcount,
                'prtl':prtl,
                'prog':prog,
            })
    
    except project_TL.DoesNotExist:
        print("Project team lead not found")
        return render(request, 'error.html', {'error_message': 'Project team lead not found'})
    
def dev_viewprogress(request,id):
    try:
        uid=request.user.id
        print('mprogress id',id)
        print('mprogress uid',uid)
        md = module_dev.objects.get(dev__user__id = uid, modu__id=id)
        print('mprogress md',md)
        mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
        dev= request.user.username
        print('mprogress dev',dev)
        dev_user= Usermember.objects.filter(user = uid)
        current__datetime = datetime.now()
        print('datenow',current__datetime)
        nowdate=current__datetime.date()
        print('nowdate',nowdate)





        if md:
            project_start = md.modu.start_date
            project_end = md.modu.end_date          
            dates = []
            current_date = project_start
            while current_date <= project_end:
                dates.append({
                    'date': current_date.strftime("%Y-%m-%d"),
                    'datep':current_date,
                    'day': current_date.strftime("%A"),
                    'year': current_date.year,
                    'month': current_date.strftime("%B"),
                    'is_new_month': current_date.day == 1,
                    'is_last_date': False
                })
                current_date += timedelta(days=1)
            
            for i, date in enumerate(dates):
                if i == len(dates) - 1 or dates[i+1]['is_new_month']:
                    date['is_last_date'] = True
            year1 = project_start.year
            month1 = project_start.strftime("%B")
            mg=m_progress.objects.filter(m_dev__modu__id =  id, m_dev__dev__user__id = uid)
            print('mprogress',mg)
            return render(request, 'dev_viewprogress.html', {
                'uid':uid,
                'id': id,
                'project_dates': dates,
                'mcount':mcount,
                'y':year1,
                'm':month1,
                'dev':dev,
                'md':md,
                'mg':mg,
                'udev':dev_user,
                'nowdate':nowdate
            })
    
    except module_dev.DoesNotExist:
        print("developer not found")
        return render(request, 'error.html', {'error_message': 'not found'})


def admin_mprogress(request,id):
    try:
        print('admin mprogress id',id)
        md = module_dev.objects.get(id=id)
        print('admin  md',md)    
        co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
        cou = co.count()
         
        if md:
            project_start = md.modu.start_date
            project_end = md.modu.end_date          
            dates = []
            current_date = project_start
            while current_date <= project_end:
                dates.append({
                    'date': current_date.strftime("%Y-%m-%d"),
                    'datep':current_date,
                    'day': current_date.strftime("%A"),
                    'year': current_date.year,
                    'month': current_date.strftime("%B"),
                    'is_new_month': current_date.day == 1,
                    'is_last_date': False
                })
                current_date += timedelta(days=1)
            
            for i, date in enumerate(dates):
                if i == len(dates) - 1 or dates[i+1]['is_new_month']:
                    date['is_last_date'] = True
            year1 = project_start.year
            month1 = project_start.strftime("%B")
            mg=m_progress.objects.filter(m_dev__id =  id)
            print('mprogress',mg)
            return render(request, 'admin_mprogress.html', {
                'id': id,
                'project_dates': dates,
                'y':year1,
                'm':month1,
                'md':md,
                'mg':mg,
                'cou':cou
                
            })
    
    except module_dev.DoesNotExist:
        print("developer not found")
        return render(request, 'error.html', {'error_message': 'not found'})

def tl_devpro(request,id):
    try:
        uid=request.user.id
        print('tl_dev progress id',id)
        print('tl_dev progress uid',uid)
        t= Usermember.objects.get(user=uid)
        pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
        md = module_dev.objects.get(id=id)
        print('mprogress md',md)
       
        if md:
            project_start = md.modu.start_date
            print('tl_dev progress startdate',project_start)
  
            project_end = md.modu.end_date          
            print('tl_dev progress end date',project_end)
            dates = []
            current_date = project_start
            while current_date <= project_end:
                dates.append({
                    'date': current_date.strftime("%Y-%m-%d"),
                    'datep':current_date,
                    'day': current_date.strftime("%A"),
                    'year': current_date.year,
                    'month': current_date.strftime("%B"),
                    'is_new_month': current_date.day == 1,
                    'is_last_date': False
                })
                current_date += timedelta(days=1)
            
            for i, date in enumerate(dates):
                if i == len(dates) - 1 or dates[i+1]['is_new_month']:
                    date['is_last_date'] = True
            year1 = project_start.year
            month1 = project_start.strftime("%B")
            mg=m_progress.objects.filter(m_dev__id =  id)
            print('mprogress',mg)
            return render(request, 'tl_devpro.html', {
                'uid':uid,
                'id': id,
                'project_dates': dates,
                'pcount':pcount,
                'y':year1,
                'm':month1,
                't':t,
                'md':md,
                'mg':mg,
            })
    
    except module_dev.DoesNotExist:
        print("developer not found")
        return render(request, 'error.html', {'error_message': 'not found'})

    
 

def custom_password_change_view(request):
    error_message = None
    uid = request.user.id
    t= Usermember.objects.get(user=uid)
    if request.method == 'POST':
        old_password = request.POST.get('Mpwd')
        new_password1 = request.POST.get('Npwd')
        new_password2 = request.POST.get('Cpwd')

        if not request.user.check_password(old_password):
            error_message = "Your old password was entered incorrectly. Please enter it again."
        elif new_password1 != new_password2:
            error_message = "The two new password fields didn’t match."
        elif not new_password1:
            error_message = "The new password cannot be empty."
        elif len(new_password1) < 6:
            error_message = "Password must be 6 characters long."
        elif not re.search(r"[A-Z]",new_password1):
            error_message = "Password must contain at least one uppercase letter."
        elif not re.search(r"\d", new_password1):
            error_message = "Password must contain at least one digit."
        elif not re.search(r"\W", new_password1):
            error_message = "Password must contain at least one special character."
    
        else:
            # Update the user's passwordn
            request.user.set_password(new_password1)
            request.user.Epwd = new_password1
            request.user.save()

            # Keep the user logged in after changing the password
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Your password was successfully updated!')
            return redirect('TL_change_pwd')

    return render(request, 'TL_change_pwd.html', {'error_message':error_message,'t':t})

def dev_password_change_view(request):
    uid=request.user.id
    error_message = None
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    if request.method == 'POST':
        old_password = request.POST.get('Mpwd')
        new_password1 = request.POST.get('Npwd')
        new_password2 = request.POST.get('Cpwd')

        if not request.user.check_password(old_password):
            error_message = "Your old password was entered incorrectly. Please enter it again."
        elif new_password1 != new_password2:
            error_message = "The two new password fields didn’t match."
        elif not new_password1:
            error_message = "The new password cannot be empty."
        elif len(new_password1) < 6:
            error_message = "Password must be 6 characters long."
        elif not re.search(r"[A-Z]",new_password1):
            error_message = "Password must contain at least one uppercase letter."
        elif not re.search(r"\d",new_password1):
            error_message = "Password must contain at least one digit."
        elif not re.search(r"[!@#$%^&*()_+\-=\]{};':\\|,.<>/?]",new_password1):
            error_message = "Password must contain at least one special character."
        else:
            # Update the user's passwordn
            request.user.set_password(new_password1)
            request.user.Epwd = new_password1
            request.user.save()

            # Keep the user logged in after changing the password
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Your password was successfully updated!')
            return redirect('dev_change_pwd')

    return render(request, 'dev_change_pwd.html', {'error_message':error_message,'uid':uid,'mcount':mcount,'dev':dev,'udev':dev_user})

# Create your views here.
def open_certificate(request,id):
    uid= request.user.id
    certificate=Usermember.objects.get(id=id)
    file_path=certificate.file.path
    with open(file_path,'rb') as f:
        response = HttpResponse(f.read(),content_type='application/docx')
        response['Content-Disposition']='inline;filename="' + certificate.file.name + ' " '
        return response
def open_Pprogress(request,id):
    progress=P_progress.objects.get(id=id)
    file_path=progress.file.path
    with open(file_path,'rb') as f:
        response = HttpResponse(f.read(),content_type='application/docx')
        response['Content-Disposition']='inline;filename="' + progress.file.name + ' " '
        return response
def open_mprogress(request,id):
    progress=m_progress.objects.get(id=id)
    file_path=progress.file.path
    with open(file_path,'rb') as f:
        response = HttpResponse(f.read(),content_type='application/docx')
        response['Content-Disposition']='inline;filename="' + progress.file.name + ' " '
        return response
def open_project(request,id):
    guidelines=project.objects.get(id=id)
    file_path=guidelines.file.path
    with open(file_path,'rb') as f:
        response = HttpResponse(f.read(),content_type='application/docx')
        response['Content-Disposition']='inline;filename="' + guidelines.file.name + ' " '
        return response   
def open_attachment(request,id):
    attachment=module.objects.get(id=id)
    file_path=attachment.file.path
    with open(file_path,'rb') as f:
        response = HttpResponse(f.read(),content_type='application/docx')
        response['Content-Disposition']='inline;filename="' + attachment.file.name + ' " '
        return response          
def home(request):
    return render(request,'home.html')
def waiting(request):
    return render(request,'waiting.html')
def reg_developer(request):
    return render(request,'reg_developer.html')
def reg_TL(request):
    return render(request,'reg_TL.html')
def loginhome(request):
    return render(request,'loginhome.html')

@login_required(login_url='ulogin')
def adminhome(request):
    current_date=datetime.today()
    print(current_date)
    enddt = project.objects.all()
    c=project.objects.filter(crossed_date = '1').count()
    print(c)    
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'adminhome.html',{'cou':cou,'c':c})

@login_required(login_url='ulogin')
def TL_home(request): 
    uid=request.user.id
    print('TL home uid',uid)
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    print('TL home pcount',pcount)
    return render(request,'TL_home.html',{'t':t,'pcount':pcount})
@login_required(login_url='ulogin')
def dev_home(request):
    uid=request.user.id
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    print('mcount',mcount)
    return render(request,'dev_home.html',{'dev':dev,'mcount':mcount,'udev':dev_user})
    
@login_required(login_url='ulogin')
def view_tl(request):
    tl=Usermember.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'view_TL.html',{'teamlead':tl,'cou':cou})
@login_required(login_url='ulogin')
def view_project(request):      
    uid=request.user.id
    t= Usermember.objects.get(user=uid)
    print('view project uid',uid)
    proj=project.objects.all()
    p_tl=project_TL.objects.all()
    print('project-teamlead',p_tl)
    pmembers = project_TL.objects.filter(team_lead__user__id = uid)
    pmembers.update(newcount = '1')   
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'view_project.html',{'proj':proj,'uid':uid,'cou':cou,'p_tl':p_tl,'t':t,'pcount':pcount})
def tl_pworkprogress(request):      
    uid=request.user.id
    print(uid)
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    print('view project uid',uid)
    proj=project.objects.all()
    p_tl=project_TL.objects.filter(team_lead__user__id = uid)
    print('projects',p_tl)
    return render(request,'tl_pworkprogress.html',{'proj':proj,'uid':uid,'p_tl':p_tl,'t':t,'pcount':pcount})
def dev_modules(request):
    uid=request.user.id
    print('dev uid',uid)
    d=Usermember.objects.get(user=uid)
    mod=module.objects.all()
    md=module_dev.objects.filter(dev__user__id = uid)
    print('modu_dev',md)
    dev_user= Usermember.objects.filter(user = uid)
    dev=request.user.username
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    return render(request,'dev_modules.html',{'mod':mod,'uid':uid,'md':md,'d':d,'mcount':mcount,'udev':dev_user,'dev':dev})
def admin_module(request,id):
    d=Usermember.objects.get(user=id)
    print('admin module',d)
    mod=module.objects.all()
    md=module_dev.objects.filter(dev__user__id = id)
    print('admin md :',md)
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'admin_module.html',{'md':md,'cou':cou})

@login_required(login_url='ulogin')
def new_member(request):
    member=Usermember.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'new_member.html',{'member':member,'cou':cou})

@login_required(login_url='ulogin')
def view_developer(request):
    developer=Usermember.objects.all()
    h=Usermember.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'view_developer.html',{'developer':developer,'h':h,'cou':cou})
@login_required(login_url='ulogin')
def viewdeveloper_TL(request):
    uid=request.user.id
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    developer = Usermember.objects.filter(user__user_type = '3', user__status = '3')
    uid=request.user.id
    team_user = Usermember.objects.filter(team = uid)
    t_l=teamlead.objects.exclude(tl=uid)
    print('team_user',team_user)
    return render(request, 'viewdeveloper_TL.html', {'uid':uid,'developer':developer,'team_user':team_user,'t_l':t_l,'t':t,'pcount':pcount})

@login_required(login_url='ulogin')
def assign_module(request):
    developer = Usermember.objects.filter(user__user_type = '3', user__status = '3')
    uname=request.user.username
    return render(request, 'assign_modules.html', {'uname':uname,'developer':developer})

@login_required(login_url='ulogin')
def add_module(request):
    uid=request.user.id
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()

    developer = Usermember.objects.filter(user__user_type = '3', user__status = '3')
    proj=project.objects.all()
    p_tl=project_TL.objects.all()
    uname=request.user.username
    return render(request, 'add_module.html', {'uname':uname,'developer':developer,'p_tl':p_tl,'uid':uid,'t':t,'pcount':pcount})

@login_required(login_url='ulogin')
def assign_project(request):
    tl=Usermember.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'assign_project.html',{'teamlead':tl,'cou':cou})
@login_required(login_url='ulogin')
def assign_TL(request,id):
    TL=Usermember.objects.all()
    dev=Usermember.objects.get(id = id)
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'assign_TL.html',{'dev':dev,'tl':TL,'cou':cou})
@login_required(login_url='ulogin')
def admin_viewproject(request):
    pro=project.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    prtl = project_TL.objects.all()
    print('prtl',prtl)
    return render(request,'admin_viewproject.html',{'pro':pro,'cou':cou,'prtl':prtl})
@login_required(login_url='ulogin')
def adminworkprogress(request):
    pro=project.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
   
    TL=Usermember.objects.filter(user__user_type = '2', user__status = '2')
    prtl=project_TL.objects.all()
    prp=P_progress.objects.all()
    return render(request,'adminworkprogress.html',{'pro':pro,'cou':cou,'prtl':prtl,'prp':prp,'TL':TL})
def progress(request,id):
    print('id',id)
    pro=project.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    TL=Usermember.objects.get(id=id)
    prtl=project_TL.objects.filter(team_lead__id = id)
    print('prtl',prtl)
    prp=P_progress.objects.filter(p_tl__team_lead__id = id)
    print('prp',prp)
    values = prp.values_list('p_tl', flat=True)
    print('values:',values)
    return render(request,'progress.html',{'pro':pro,'cou':cou,'prtl':prtl,'prp':prp,'tl':TL,'values':values})
    
def progresspro(request,id):
    print('id',id)
    pro=project.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    TL=Usermember.objects.get(id=id)
    prtl=project_TL.objects.filter(team_lead__id = id)
    print('prtl',prtl)
    prp=P_progress.objects.filter(p_tl__team_lead__id = id)
    print('prp',prp)
    values = prp.values_list('p_tl', flat=True)
    print('values:',values)
    return render(request,'progresspro.html',{'pro':pro,'cou':cou,'prtl':prtl,'prp':prp,'tl':TL,'values':values,'tlid':id})
def progresspr(request,id):
    if request.method == 'POST':
        name=request.POST.get('name')
    print('id',id)
    pro=project.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    TL=Usermember.objects.get(id=id)
    prtl=project_TL.objects.filter(team_lead__id = id)
    print('prtl',prtl)
    prp=P_progress.objects.filter(p_tl__team_lead__id = id)
    print('prp',prp)
    values = prp.values_list('p_tl', flat=True)
    print('values:',values)
    return render(request,'progresspro.html',{'pro':pro,'cou':cou,'prtl':prtl,'prp':prp,'tl':TL,'values':values})
def pemployee(request):
    TL=Usermember.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    
    cou = co.count()
    return render(request,'pemployee.html',{'tl':TL,'cou':cou})
@login_required(login_url='ulogin')
def TLworkprogress(request):
    uid=request.user.id
    developer = Usermember.objects.filter(user__user_type = '3', user__status = '3')
    team_user = Usermember.objects.filter(team = uid)
    t_l=teamlead.objects.exclude(tl=uid)
    t= Usermember.objects.get(user=uid)
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    print('tl work',uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    return render(request, 'TLworkprogress.html', {'t':t,'uid':uid,'team_user':team_user,'t_l':t_l,'developer':developer,'pcount':pcount})
def tl_progressmod(request,id):
    print("progressmod id",id)
    uid=request.user.id
    print("progressmod uid", uid)
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    tl_mod=module_dev.objects.filter(dev__id = id)
    print('progressmod tl_mod',tl_mod)
    return render(request, 'tl_progressmod.html', {'t':t,'uid':uid,'pcount':pcount,'tl_mod':tl_mod})



@login_required(login_url='ulogin')
def TL_viewmodules(request):
    uid=request.user.id
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    mod=module_dev.objects.all()
    print('mod',mod)
    print('tl work',uid)
    mo=module.objects.all()
    return render(request, 'TL_viewmodules.html', {'uid':uid,'mo':mo,'t':t,'pcount':pcount,'mod':mod})
 
@login_required(login_url='ulogin')
def change_member(request,pk,upk):
    print('pk',pk)
    print('upk',upk)
    member=CustomUser.objects.get(id=pk)
    mem=Usermember.objects.get(user=pk)
    print('ch_member',mem)
    memassign = CustomUser.objects.all()
    mem.assign= ''
    mem.save()
    if  member.user_type == '2':
        member.user_type = '3'
        member.status = '3'  
        member.save()
        dev_tl=Usermember.objects.filter(team = pk)
        print('ch_tl',dev_tl)
        dev_tl.update(team = None)
        pr_user=project_TL.objects.filter(team_lead = upk)
        print('pr_user',pr_user)
        pr_user.update(team_lead = None)   
        # print('pr_id',pr_id)
        # pr_custom = pr_user.team_lead()
        # print('pr_user',pr_user)       
    return redirect('view_tl')   
@login_required(login_url='ulogin')
def change_developer(request,pk):
    member=CustomUser.objects.get(id=pk)
    mem=Usermember.objects.get(user=pk)
    mem.assign= ''
    mem.save()
    if member.user_type == '3':
        member.user_type = '2'
        member.status = '2'
        member.save()
    return redirect('view_developer')      
def register_dev(req):
    if req.method == 'POST':
        fname = req.POST['fname']
        lname = req.POST['lname']
        addr = req.POST['addr']
        uname = req.POST['uname']
        email = req.POST['email']
        number = req.POST['number']
        course = req.POST['course']
        certificate=req.FILES.get('file')
        dept = req.POST['dept']
        utype = req.POST['utype']
        ustatus = req.POST['ustatus']
        uassign = req.POST['assign']
        Epwd = req.POST['Epwd']
        regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        match=re.match(regex,email)
        def generate_random_string():
            length=6
            characters=string.ascii_letters + string.digits
            random_string=''.join(random.choice(characters) for i in range(length))
            return random_string
        password=generate_random_string()
        Epwd = password
        print(password)

        if fname == "":
            messages.info(req,"First Name Field is required !!")
            return render(req,'reg_developer.html')
        elif lname == "":
            messages.info(req,"Last Name Field is required !!")
            return render(req,'reg_developer.html')
        elif addr == "":
            messages.info(req,"Address  Field is required !!")
            return render(req,'reg_developer.html')
        elif uname == "":
            messages.info(req,"User Name Field is required !!")
            return render(req,'reg_developer.html')
        elif dept == "":
            messages.info(req,"Department Field is required !!")
            return render(req,'reg_developer.html')
        elif certificate == "":
            messages.info(req,"Certification Field is required !!")
            return render(req,'reg_developer.html')
        elif course == "":
            messages.info(req,"Course Field is required !!")
            return render(req,'reg_developer.html')       
        elif email == "":
            messages.info(req,"Contact Number Field is required !!")
            return render(req,'reg_developer.html')
        elif match == False :
            messages.info(req,"Invalid Email !!")
            return render(req,'reg_developer.html')
        elif not email.lower().endswith('.com'):
            messages.info(req,"Invalid Email..Must include .com")
            return render(req,'reg_developer.html')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(req,"Email already exist !!")
            return render(req,'reg_developer.html')
        elif number == "":
            messages.info(req,"Contact Number Field is required !!")
            return render(req,'reg_developer.html')
        elif len(number) != 10 :         
            messages.info(req,"Mobile number must be 10 digits long !!")
            return render(req,'reg_developer.html')
        elif CustomUser.objects.filter(username=uname).exists():
            messages.info(req,"User Name already exist !!")
            return render(req,'reg_developer.html')
        else:
            user = CustomUser.objects.create_user(first_name=fname,last_name = lname,username=uname,email=email,user_type=utype,password=password,status=ustatus,Epwd=Epwd)
            user.save()
            member = Usermember(address=addr,number=number,course=course,file=certificate,department=dept,user=user,assign=uassign)
            member.save()
         
            subject="Registration successfull"
            message="username: {0} and password : {1}".format(uname,password)
            recipient=req.POST['email']
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            messages.info(req,"Registration successfull, Please wait for Approval")
            return render(req,'reg_developer.html')  
def register_TL(req):
    if req.method == 'POST':
        fname = req.POST['fname']
        lname = req.POST['lname']
        addr = req.POST['addr']
        uname = req.POST['uname']
        email = req.POST['email']
        number = req.POST['number']
        course = req.POST['course']
        certificate=req.FILES.get('file')
        dept = req.POST['dept']
        utype = req.POST['utype']
        ustatus = req.POST['ustatus']
        uassign = req.POST['assign']
        Epwd = req.POST['Epwd']
        status = 0
        regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-zA-Z0-9-.]+$'
        match=re.match(regex,email)
        def generate_random_string():
            length=6
            characters=string.ascii_letters + string.digits
            random_string=''.join(random.choice(characters) for i in range(length))
            return random_string
        password=generate_random_string()
        Epwd = password  
        print(password)
        if fname == "":
            messages.info(req,"First Name Field is required !!")
            return render(req,'reg_TL.html')
        elif lname == "":
            messages.info(req,"Last Name Field is required !!")
            return render(req,'reg_TL.html')
        elif addr == "":
            messages.info(req,"Address  Field is required !!")
            return render(req,'reg_TL.html')
        elif uname == "":
            messages.info(req,"User Name Field is required !!")
            return render(req,'reg_TL.html')
        elif dept == "":
            messages.info(req,"Department Field is required !!")
            return render(req,'reg_TL.html')
        elif certificate == "":
            messages.info(req,"Certification Field is required !!")
            return render(req,'reg_TL.html')
        elif course == "":
            messages.info(req,"Course Field is required !!")
            return render(req,'reg_TL.html')
        elif email == "":
            messages.info(req,"Email Field is required !!")
            return render(req,'reg_TL.html')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(req,"Email already exist !!")
            return render(req,'reg_TL.html')
        elif match == False :
            messages.info(req,"Invalid Email !!")
            return render(req,'reg_TL.html')
        elif not email.lower().endswith('.com'):
            messages.info(req,"Invalid Email..   include .com")
            return render(req,'reg_TL.html')
        elif number == "":
            messages.info(req,"Contact Number Field is required !!")
            return render(req,'reg_TL.html')
        elif len(number) != 10 :         
            messages.info(req,"Mobile number must be 10 digits long !!")
            return render(req,'reg_TL.html')   
        elif CustomUser.objects.filter(username=uname).exists():
            messages.info(req,"User Name already exist !!")
            return render(req,'reg_TL.html')
        else:
            user = CustomUser.objects.create_user(first_name=fname,last_name = lname,username=uname,email=email,user_type=utype,status=ustatus,password=password,Epwd=Epwd)
            user.save()
            member = Usermember(address=addr,number=number,course=course,file=certificate,department=dept,user=user,assign=uassign)
            member.save()
                        
            subject="Registration successfull"
            message="username: {0} and password : {1}".format(uname,password)
            recipient=req.POST['email']
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            messages.info(req,"Registration successfull, Please wait for Approval")
            return render(req,'reg_TL.html') 
    return redirect('home')


def ulogin(req):
    if req.method == 'POST':
        uname = req.POST['username']
        passw = req.POST['password']
        users = authenticate(username =uname,password=passw)
        
        
        if users is not None:
            if users.user_type == '1':
                login(req,users)
                return redirect('adminhome')
            elif users.status == '0':
                auth.login(req,users)
                messages.info(req,f'welcome {uname}, Please wait for approval')
                return redirect('waiting')
            elif users.user_type == '2':
                auth.login(req,users)
                messages.info(req,f'welcome {uname}, You have been logged In')
                return redirect('TL_home')
            else:
                auth.login(req,users)
                messages.info(req,f'welcome {uname}, You have been logged In')
                return redirect('dev_home')  
        return redirect('ulogin')
    return render(req,'loginhome.html')
def reject(request,id):
    member1=Usermember.objects.get(id=id)
    member2=member1.user
    print('member1',member1)
    print('member2',member2)
    recipient=member1.user.email
    print(recipient)
    subject="rejected"
    message="Your application is Rejectded ...!!"
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
    member1.delete()
    member2.delete()
    messages.info(request,'Application Rejected')
    return redirect('new_member')
def approve(request,id):
    approve=CustomUser.objects.get(id=id)
    if approve.user_type == '2':
        approve.status = '2'
    else:
        approve.status = '3'
    approve.save()
    recipient=approve.email
    subject="Approved"
    message="Your application is Approved.username: {0} and password : {1}".format(approve.username,approve.Epwd)
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])

    messages.info(request,'Application Approved') 
    return redirect('new_member')
@login_required(login_url='ulogin')
def TL_updateworkprogress(request,id):
    uid=request.user.id
    print('TL home uid',uid)
    t= Usermember.objects.get(user=uid)
    print('id',id)
    print('uid',uid)
    proj=project.objects.all()
    protl=project_TL.objects.filter(team_lead = id)
    progress = P_progress.objects.filter(p_tl__team_lead = id)
    print('progress',progress)
    now=datetime.now()
    c_date=now.strftime("%Y-%m-%d")
    print(c_date)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    return render(request,'TL_updateworkprogress.html',{'t':t,'proj':proj,'uid':uid,'protl':protl,'progress':progress,'c_date':c_date,'pcount':pcount})
def update_dev(request,id):
    uid=request.user.id
    modul = module_dev.objects.get(id = id)
    u=Usermember.objects.all()
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    return render(request,'update_dev.html',{'mo':modul,'u':u,'uid':uid,'dev':dev,'udev':dev_user,'mcount':mcount})
@login_required(login_url='ulogin')
def updatework(request,id):
    uid=request.user.id
    print('TL home uid',uid)
    t= Usermember.objects.get(user=uid)
    proj=project.objects.all()
    prtl=project_TL.objects.get(id=id)
    protl=project_TL.objects.filter(team_lead = id)
    progress = P_progress.objects.filter(p_tl__team_lead = id)
    now=datetime.now()
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
    c_date=now.strftime("%Y-%m-%d")
    u=Usermember.objects.all()
    return render(request,'updatework.html',{'u':u,'prtl':prtl,'t':t,'pcount':pcount,'proj':proj,'uid':uid,'protl':protl,'progress':progress,'c_date':c_date})   


@login_required(login_url='ulogin')
def editworkfun(request,id):
    if request.method=='POST':
        uid=request.user.id
        print('uid',uid)
        print('editwork id',id)
        pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()
        t= Usermember.objects.get(user=uid)
        proj=project.objects.all()
        protl=project_TL.objects.filter(team_lead = id) 
        now=datetime.now()
        c_date=now.strftime("%Y-%m-%d")
        work=project_TL.objects.get(id = id)
        print('work',work)
        progress_instance = P_progress.objects.filter(p_tl=work, date=c_date).first()
        progress = request.FILES.get('file')
        print('progress',progress)
        if progress_instance:
            progress_instance.file = progress
            progress_instance.save()
        else:
            up_tl = P_progress(p_tl=work, date=c_date, file=progress)
            up_tl.save()
            print('up_tl-pprogress',up_tl)
        messages.info(request,'Work Progress Updated')
        return redirect('TL_home')
    return redirect('TL_home')
@login_required(login_url='ulogin')
def editfun_dev(request, id):
    if request.method == 'POST':
        # Get current user ID and username
        uid = request.user.id
        dev = request.user.username

        # Get module development object
        work = module_dev.objects.get(id=id)

        # Get progress file from request
        progress_file = request.FILES.get('file')
        print('progress', progress_file)

        if progress_file:
            # Delete existing progress for the same date
            m_progress.objects.filter(m_dev=work, date=timezone.now()).delete()

            # Create and save new progress update
            m_progress.objects.create(
                m_dev=work,
                date=timezone.now(),
                file=progress_file
            )

            # Count modules with zero progress
            mcount = module_dev.objects.filter(dev__user__id=uid, mod_count=0).count()

            messages.info(request, 'Work Progress Updated')
        else:
            messages.error(request, 'No file uploaded')

        return redirect('dev_home')

 
    
@login_required(login_url='ulogin')
def TL_change_pwd(request):
    uid = request.user.id
    mem = CustomUser.objects.get(id = uid)
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()

    return render(request,'TL_change_pwd.html',{'m':mem,'uid':uid,'t':t,'pcount':pcount})
@login_required(login_url='ulogin')
def dev_change_pwd(request):
    uid = request.user.id
    mem = CustomUser.objects.get(id = uid)
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    return render(request,'dev_change_pwd.html',{'m':mem,'uid':uid,'dev':dev,'udev':dev_user,'mcount':mcount})
@login_required(login_url='ulogin')
def TL_pwdfun(request,id):
    if request.method == 'POST':
        uid = request.user.id
        pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()

        t= Usermember.objects.get(user=uid)
        membr = CustomUser.objects.get(id = id)
        pwd = membr.Epwd
        print('pwd :',pwd)
        Mpwd = request.POST['Mpwd']
        Npwd = request.POST['Npwd']
        Cpwd = request.POST['Cpwd']
        if pwd == Mpwd and Npwd == Cpwd :
            membr.Epwd = Npwd
            membr.password = Npwd 
            membr.save()
            messages.info(request,"Password Updated")
            return render(request,'TL_home.html')
        else :
            messages.info(request,"Password doesn't match...!!!")
            return render(request,'TL_change_pwd.html',{'t':t,'pcount':pcount})
    return redirect('TL_home')


@login_required(login_url='ulogin')
def dev_viewmodule(request):
    uid=request.user.id
    print('dev id',uid)
    modul = module_dev.objects.filter(dev__user__id = uid)
    print('modul',modul)
    modul.update(mod_count='1')
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    return render(request,'dev_viewmodule.html',{'modu':modul,'uid':uid,'dev':dev,'mcount':mcount,'udev':dev_user})

@login_required(login_url='ulogin')
def dev_updatework(request):
    uid=request.user.id
    now=datetime.now()
    c_date=now.strftime("%Y-%m-%d")
    print('cdate',c_date)
    modul = module_dev.objects.filter(dev__user__id = uid)
    progress = m_progress.objects.filter(m_dev__dev__user__id = uid)
    print('dev_updatework progress',progress)
    print('uid',uid)
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    return render(request,'dev_updatework.html',{'mo':modul,'uid':uid,'progress':progress,'dev':dev,'mcount':mcount,'udev':dev_user,'c_date':c_date})

@login_required(login_url='ulogin')
def admin_logout(request):
    return render(request,'home.html')
@login_required(login_url='ulogin')
def TL_logout(request):
    return render(request,'home.html')
@login_required(login_url='ulogin')
def dev_logout(request):
    return render(request,'home.html')    
@login_required(login_url='ulogin')
def TL_profile(request):
    uid=request.user.id
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()

    member=Usermember.objects.get(user=uid)
    return render(request,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
def dev_profile(request):
    uid=request.user.id
    member=Usermember.objects.get(user=uid)
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    return render(request,'dev_profile.html',{'m':member,'dev':dev,'mcount':mcount,'udev':dev_user})


def assign_teamleader(request):
    uid=request.user.id
    print('uid',uid)
    TL=Usermember.objects.filter(user__user_type = '2', user__status = '2')
    memtl=teamlead.objects.all()
    member2=Usermember.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    return render(request,'assign_teamleader.html',{'memtl':memtl,'mem2':member2,'tl':TL,'cou':cou})
@login_required(login_url='ulogin')
def assignfun(request,id):
    if request.method=='POST':
        teaml =teamlead.objects.all()
        print('usermember id: ',id)
        dev=Usermember.objects.get(id=id)
        print('dev',dev)
        sel = request.POST['sel']
        print('sel',sel)
        t_l = CustomUser.objects.get(id = sel)
        tl_id = t_l.id
        print('tl_id',tl_id)
        teaml =teamlead(id=tl_id,tl=t_l)
        print('teaml',teaml)
        teaml.save()
        uteam = teamlead.objects.get(id=tl_id)
        dev.team = uteam
        dev.save()
        print('uteam',uteam)
        messages.info(request,"Teamlead Assigned.")
        return redirect('assign_teamleader')     
def proj_assignfun(request):
    if request.method == 'POST':
        pr_topic = request.POST['sel1']
        prj_topic = project.objects.get(id=pr_topic)
        pr_tl = request.POST['sel2']
        prj_tl = Usermember.objects.get(user=pr_tl)
        pid = (prj_tl.id)
        print('pid', pid)

        # Check if project is already assigned to team lead
        if project_TL.objects.filter(project_name=prj_topic, team_lead=prj_tl).exists():
            messages.info(request, "Already assigned...!!!")
            return render(request, 'tl_assign.html')

        # Count projects assigned to team lead
        pcount = project_TL.objects.filter(team_lead__id=pid).count()
        print('pcount', pcount)

        # Assign project to team lead
        pr_assign = project_TL(project_name=prj_topic, team_lead=prj_tl, newcount=pcount)
        pr_assign.save()

        # Get project timeline
        ptl = project_TL.objects.get(project_name=prj_topic, team_lead=prj_tl)
        startdate = ptl.project_name.start_date
        print('sdate:', startdate)
        enddate = ptl.project_name.end_date
        print('edate:', enddate)
        progress_list = list(P_progress.objects.all())
        print(progress_list)

        # Create progress entries for each day
        current_date = startdate
        while current_date <= enddate:
            P_progress.objects.create(date=current_date, p_tl=ptl)
            current_date += timedelta(days=1)

        messages.info(request, "Project Assigned.")
        return redirect('tl_assign')
    else:
        return render(request, 'tl_assign.html')

 
def mod_assignfun(request):
    if request.method == 'POST':
        uid = request.user.id
        t = Usermember.objects.get(user=uid)
        mod_name = request.POST['sel1']
        print('sel1', mod_name)
        modu_name = module.objects.get(id=mod_name)
        mdev = request.POST['sel2']
        print('sel2', mdev)
        m_dev = Usermember.objects.get(user=mdev)
        
        # Check if module is already assigned
        if module_dev.objects.filter(modu=modu_name, dev=m_dev).exists():
            messages.info(request, "Already assigned...!!!")
            return redirect('TL_assignmodule')
        
        # Create and save new module assignment
        mod_assign = module_dev(modu=modu_name, dev=m_dev, mod_count=0)
        mod_assign.save()
       
        md = module_dev.objects.get(modu=modu_name, dev=m_dev)
        startdate = md.modu.start_date
        print('sdate:', startdate)
        enddate = md.modu.end_date
        print('edate:', enddate)
        progress_list = list(m_progress.objects.all())
        print(progress_list)

        # Create progress entries for each day
        current_date = startdate
        while current_date <= enddate:
            m_progress.objects.create(date=current_date,m_dev=md)
            current_date += timedelta(days=1)
       
        messages.info(request, "Module Assigned.")
        return redirect('TL_assignmodule')

def tl_assign(request):
    uid=request.user.id
    print('uid',uid)
    proj = project.objects.all()
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    TL = Usermember.objects.filter(user__user_type = '2', user__status = '2')
    return render(request,'tl_assign.html',{'proj':proj,'tl':TL,'cou':cou})
def TL_assignmodule(request):
    uid = request.user.id
    uname = request.user.username
    print('uid',uid)
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()

    modu = module.objects.all()
    developer = Usermember.objects.filter(user__user_type = '3', user__status = '3')
    team_user = Usermember.objects.filter(team = uid)
    return render(request,'TL_assignmodule.html',{'t':t,'pcount':pcount,'modu':modu,'developer':developer,'uid':uid,'uname':uname,'team_user':team_user})
def tldev_assign(request,id):
    uid=request.user.id
    print('uid',uid)
    print('tldiv id',id)
    co=CustomUser.objects.filter(status = '0').exclude(user_type = '1')
    cou = co.count()
    tl = Usermember.objects.filter(user__user_type = '2', user__status = '2')
    member2=Usermember.objects.get(id=id)
    return render(request,'tldev_assign.html',{'mem2':member2,'tl':tl,'cou':cou})
def deletetl(request,id):
    uid = Usermember.objects.get(id=id)
    print('uid',uid)
    uname = uid.user.username
    print('uname',uname)
    tl_c =CustomUser.objects.filter(TL = uname)
    print('filter columns with del username',tl_c)
    tl_c.update(TL='0')
    membr = Usermember.objects.get(id = id)
    print('member',membr)
    membr.delete()
    membr.user.delete()
    return redirect('view_tl')
def deletedev(request,id):
    uid = request.user.id
    print('uid',uid)
    print('id',id)
    membr = Usermember.objects.get(id = id)
    print('member',membr)
    membr.delete()
    membr.user.delete()
    return redirect('view_developer')
def TLprofile_edit(request,id):
    uid=request.user.id
    print('edit uid',uid)
    member=Usermember.objects.get(user=uid)
    print('edit member',member)
    return render(request,'TLprofile_edit.html',{'m':member})
def devprofile_edit(request,id):
    uid=request.user.id
    print('edit uid',uid)
    member=Usermember.objects.get(id=id)
    print('edit member',member)
    dev=request.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()
    return render(request,'devprofile_edit.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
def edit_tl(req,id):
    uid=req.user.id
    uemail = req.user.email
    cert = Usermember.objects.get(id = id)
    cer =cert.file
    member=Usermember.objects.get(user=uid)
    print('edit uid',uid)
    print('id',id)
    print('uemail',uemail)
    print('cert',cer)
    uid=req.user.id
    t= Usermember.objects.get(user=uid)
    pcount = project_TL.objects.filter(team_lead__user__id = uid,newcount= '0').count()

    users = CustomUser.objects.exclude(email = uemail)
    print('users',users)
    if req.method == 'POST':
        email = req.POST['email']
        print('email_to_check',email)
        regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-zA-Z0-9-.]+$'
        match=re.match(regex,email)
        number = req.POST['number']
        f = req.FILES.get('file')
        print('file',f)

        if users.filter(email = email).exists():
            messages.info(req,"Email already exist !!")
            return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
        elif email == "":
            messages.info(req,"Email Field is required !!")
            return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
        elif match == False :
            messages.info(req,"Invalid Email !!")
            return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
        elif not email.lower().endswith('.com'):
            messages.info(req,"Invalid Email..   include .com")
            return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
        elif number == "":
            messages.info(req,"Contact Number Field is required !!")
            return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
        elif len(number) != 10 :         
            messages.info(req,"Mobile number must be 10 digits long !!")
            return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})  
        else :
            member.user.first_name = req.POST['fname']
            member.user.last_name = req.POST['lname']
            member.address = req.POST['addr']
            member.user.email = req.POST['email']
            member.number = req.POST['number']
            member.course = req.POST['course']
            if f == None:
                member.file = cer
            else:
                member.file = req.FILES.get('file')
            member.department = req.POST['dept']
            member.save()
            member.user.save()
            messages.info(req,"Profile updated")
            return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
    return render(req,'TL_profile.html',{'m':member,'t':t,'pcount':pcount})
def edit_dev(req,id):
    uid=req.user.id
    uemail = req.user.email
    cert = Usermember.objects.get(id = id)
    cer =cert.file
    member=Usermember.objects.get(user=uid)
    users = CustomUser.objects.exclude(email = uemail)
    print('edit uid',uid)
    print('id',id) 
    dev=req.user.username
    print('dev',dev)
    dev_user= Usermember.objects.filter(user = uid)
    print('dev_user',dev_user)
    mcount=module_dev.objects.filter(dev__user__id = uid,mod_count = '0').count()    
    if req.method == 'POST':
        email = req.POST['email']
        regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-zA-Z0-9-.]+$'
        match=re.match(regex,email)
        number = req.POST['number']
        f = req.FILES.get('file')
        print('file',f)
        
        if users.filter(email = email).exists():
            messages.info(req,"Email already exist !!")
            return render(req,'TLprofile_edit.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
        elif email == "":
            messages.info(req,"Email Field is required !!")
            return render(req,'devprofile_edit.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
        elif match == False :
            messages.info(req,"Invalid Email !!")
            return render(req,'devprofile_edit.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
        elif not email.lower().endswith('.com'):
            messages.info(req,"Invalid Email..   include .com")
            return render(req,'devprofile_edit.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
        elif number == "":
            messages.info(req,"Contact Number Field is required !!")
            return render(req,'devprofile_edit.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
        elif len(number) != 10 :         
            messages.info(req,"Mobile number must be 10 digits long !!")
            return render(req,'devprofile_edit.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})  
        else :
            member.user.first_name = req.POST['fname']
            member.user.last_name = req.POST['lname']
            member.address = req.POST['addr']
            member.user.email = req.POST['email']
            member.number = req.POST['number']
            member.course = req.POST['course']
            if f == None:
                member.file = cer
            else:
                member.file = req.FILES.get('file')            

            member.department = req.POST['dept']
            member.save()
            member.user.save()
            messages.info(req,"Profile updated")
            return render(req,'dev_profile.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
    return render(req,'dev_profile.html',{'m':member,'dev':dev,'udev':dev_user,'mcount':mcount,'uid':uid})
def client_profile(request,id):
    print('id',id)
    uid= request.user.id
    pr=project.objects.get(id=id)
    print('pr',pr)
    print('pro_id',uid)
    return render(request,'client_profile.html',{'pr':pr}) 
def view_moduledev(request,id):
    print('id',id)
    uid= request.user.id
    print('tl_id',uid)
    m_dev=module_dev.objects.filter(modu = id)
    print('m_dev',m_dev)
    return render(request,'view_moduledev.html',{'m_dev':m_dev})  
def tl_project(request,id):
    print('id',id)
    uid= request.user.id
    print('tl_id',uid)
    tlp=project_TL.objects.filter(project_name = id)
    print('tlp',tlp)
    return render(request,'tl_project.html',{'tlp':tlp})
def project_updatefun(request,id):
    now=datetime.now()
    c_date=now.strftime("%Y-%m-%d")
    work=request.FILES.get('file')
    # tlpr = project_TL.objects.filter(project_, user__status = '2')

