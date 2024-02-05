from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
import random
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def signupView(request):
    if request.method == "POST":
        role = request.POST['role']
        if role=="candidate":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            #========= otp =====================
            otp = random.randint(200000,900000)
            print(otp,"oooooottttppppppppppppppppppppppp")
            mastermodel = masterModel.objects.create(email=email,pasword=password, otp=otp,role=role)
            usermodel = userModel.objects.create(mastermodel=mastermodel,firstname = fname, lastname = lname)
            return redirect('otp/',{"role":role}) 
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            #========= otp ======================
            otp = random.randint(200000,900000)
            print(otp,"oooooooooootttttttttttttppppppppppppppppppppppp")
            mastermodel = masterModel.objects.create(email=email,pasword=password, otp=otp,role = role)
            usermodel = companyModel.objects.create(mastermodel_id= mastermodel.id,firstname=fname,lastname=lname)
            return redirect('otp/',{"role":role})            
    return render(request,"signup.html")

def loginView(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_instance = masterModel.objects.get(email=email, pasword=password)
            try:
                request.session['id'] = user_instance.id
                request.session['pk'] = user_instance.id
            except:
                return redirect('login')
            if user_instance.role == "candidate":
                return redirect('jobprofile')
            else:
                return redirect('companyprofile' )
        except masterModel.DoesNotExist:
            message = "Invalid Credential !!"
            return render(request, "login.html", {"message": message})
    return render(request, "login.html")
    
def otpveryfyView(request):
    if request.method =="POST":
        otp = request.POST['otp']
        try:
            checkotp = masterModel.objects.get(otp=otp)   
            if checkotp.role=="candidate":
                userid = userModel.objects.get(mastermodel=checkotp)
                try:
                    request.session['id']=userid.id
                except:
                    return redirect('login')
                return redirect("jobprofile")
            else:
                id = masterModel.objects.get(otp = otp)
                cid = companyModel.objects.get(mastermodel_id=id)
                try:
                    request.session['pk'] = checkotp.id
                    request.session['id'] = cid.id
                except:
                    return redirect('login')
                return redirect("/companyprofile/")               
        except:
            message = "Invalid Otp !!"
            return render(request,"otppage.html",{"message":message})
    return render(request,"otppage.html")


def jobprofileView(request):
    try:
        id = request.session['id']
    except KeyError:
        return redirect('login')

    getid = userModel.objects.get(mastermodel_id=id)
    firstname = getid.firstname
    lastname = getid.lastname

    sjobtitle = request.GET.get('sjobtitle')
    city = request.GET.get('city') if request.GET.get('city') !="" else ""
    if sjobtitle or city:
        all_jobs = postjobModel.objects.filter(Q(companyname__icontains=sjobtitle) | Q(jobtitle__icontains=sjobtitle) | Q(city__icontains=city) | Q(state__icontains=city))
    else:
        all_jobs = postjobModel.objects.all()
    items_per_page = 10
    paginator = Paginator(all_jobs, items_per_page)
    page = request.GET.get('page')

    try:
        alldata = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        alldata = paginator.page(1)

    return render(request, "jobprofile.html", {
        "firstname": firstname,
        "lastname": lastname,
        "alldata": alldata,
    })

def userprofileView(request):
    try:
        id = request.session['id']
    except:
        return redirect('login')
    instancem = masterModel.objects.get(id=id)
    instanceum = userModel.objects.get(mastermodel_id=instancem)
    if request.method == "POST":
        instancem.email = request.POST['email']
        instanceum.firstname = request.POST['fname']
        instanceum.lastname = request.POST['lname']
        instanceum.mobile = request.POST['mobile']
        instanceum.city = request.POST['city']
        instanceum.state = request.POST['state']
        try:
            instanceum.candidatelogo = request.FILES['candidatelogo']
        except:
            pass
        instanceum.save()
        instancem.save()
    email = instancem.email
    firstname = instanceum.firstname
    lastname = instanceum.lastname
    mobile = instanceum.mobile
    city = instanceum.city
    state = instanceum.state
    candidatelogo = instanceum.candidatelogo.url if instanceum.candidatelogo !="" else ''
    return render(request,"usersprofile.html",{"email":email,"firstname":firstname,"lastname":lastname,"mobile":mobile,"city":city,"state":state,"candidatelogo":candidatelogo})

def companyprofileView(request):
    try:
        pk=request.session['pk']
    except:
        return redirect('login')
    masterid = masterModel.objects.get(id=pk)
    candidateid = companyModel.objects.get(mastermodel_id=masterid)
    email = masterid.email
    firstname = candidateid.firstname
    lastname = candidateid.lastname
    mobile = candidateid.mobile
    city = candidateid.city
    state = candidateid.state
    companylogo = candidateid.companylogo.url if candidateid.companylogo !="" else ''
    return render(request,"company/companyprofile.html",{"email":email,"firstname":firstname,"lastname":lastname,"mobile":mobile,"city":city,"state":state,"companylogo":companylogo})

def companyupdatepView(request):
    try:
        id = request.session['pk']
    except:
        return redirect('login')
    
    masterid = masterModel.objects.get(id=id)
    candidateid = companyModel.objects.get(mastermodel = masterid)    
    if request.method=="POST":
        masterid.email = request.POST['email']
        candidateid.firstname = request.POST['firstname']
        candidateid.lastname = request.POST['lastname']
        candidateid.mobile = request.POST['mobile']
        candidateid.city = request.POST['city']
        candidateid.state = request.POST['state']
        try:
            candidateid.companylogo = request.FILES['companylogo']
        except:
            pass
        candidateid.save()
        masterid.save()
        
    email = masterid.email
    firstname = candidateid.firstname
    lastname = candidateid.lastname
    mobile = candidateid.mobile
    city = candidateid.city
    state = candidateid.state
    companylogo = candidateid.companylogo.url if candidateid.companylogo else ''
    return render(request,"company/companyupdatep.html",{"email":email,"firstname":firstname,"lastname":lastname,"mobile":mobile,"city":city,"state":state,"companylogo":companylogo})

def jobpostView(request):
    try:
        pk=request.session['pk']
    except:
        return redirect('login')
    masterid = masterModel.objects.get(id=pk)
    companyid = companyModel.objects.get(mastermodel_id=masterid)
    if request.method=="POST":
        companyname = request.POST['companyname']
        jobtitle = request.POST['jobtitle']        
        jobdescription = request.POST['jobdescription']
        city = request.POST['city']
        state = request.POST['state']
        salary = request.POST['salary']
        salarytype = request.POST['salarytype']
        companyimage = request.FILES['companyimage']
        postjob = postjobModel.objects.create(companyname=companyname,companyid_id=companyid.id, jobtitle=jobtitle,jobdescription=jobdescription,city=city,state=state,salary=salary,salarytype=salarytype,companyimage=companyimage)
        return redirect('companyprofile')
    return render(request,'company/jobpost.html')

def postedjobseeView(request):
    try:
        id=request.session['pk']
        print(id,'kkkkkkkkkkkkkkk')
    except:
        pass
    companyid = companyModel.objects.get(mastermodel_id=id)
    jobid = postjobModel.objects.filter(companyid_id=companyid)
    return render(request,"company/postedjobsee.html",{"jobid":jobid})
    

def logoutView(request):
    logout(request)
    return redirect('/')