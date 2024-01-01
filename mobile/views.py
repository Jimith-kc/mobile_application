from django.shortcuts import render,redirect

from django.views.generic import View
#for import form
from mobile.forms import MobileForm,RegistrationForm,LoginForm 

from mobile.models import Mobiles

from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator

#create decorator
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request," invalid session.........!")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(signin_required,name="dispatch")
# Create your views here.
class MobileListView(View):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
# filter using brand
        if "brand" in request.GET:
            brand=request.GET.get("brand")
            qs=qs.filter(brand__iexact=brand)
#filter using display
        if "display" in request.GET:
            display=request.GET.get("display")
            qs=qs.filter(display__iexact=display)
#filter using price
        if "price_lt" in request.GET:
            amount=request.GET.get("price_lt")
            qs=qs.filter(price__lte=amount)
        if "price_gt" in request.GET:
            amount=request.GET.get("price_gt")
            qs=qs.filter(price__gte=amount)


        return render(request,"mobile_list.html",{"data":qs})

#localhost:8000/mobiles/{id}
@method_decorator(signin_required,name="dispatch")
class MobileDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        print(id)
        qs=Mobiles.objects.get(id=id)
        return render(request,"mobile_details.html",{"data":qs})

#localhost:8000/mobiles/{id}/remove
@method_decorator(signin_required,name="dispatch")
class MobileDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Mobiles.objects.get(id=id).delete()
        messages.success(request,"mobile data has been deleted")
        return redirect("mobile-all")

#localhost:8000/mobiles/add
#get => mobiles_add.html
#post => save data
@method_decorator(signin_required,name="dispatch")
class MobilesCreateView(View):
    def get(self,request,*args,**kwargs):
        form=MobileForm()
        return render(request,"mobile_add.html",{"form":form})


    def post(self,request,*args,**kwargs):
        form=MobileForm(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"mobile data created successfully")
            return redirect("mobile-all")

        else:
            messages.error(request," cant create data error.........!")
            return render(request,"mobile_add.html",{"form":form})
        
#localhost:8000/mobiles/{mobile_id}/change
#get
#post
@method_decorator(signin_required,name="dispatch")
class MobileUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(instance=obj)
        return render(request,"mobile_edit.html",{"form":form})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(request.POST,instance=obj,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"mobile change updated successfully")
            return redirect("mobile-all")

        else:

            messages.error(request,"cant update data...!")
            return render(request,"mobile_edit.html",{"form":form})        

# view for registration>>>>>>
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)

        if form.is_valid():
            #form.save() for encrypt password
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Account created successfully")
            return render(request,"register.html",{"form":form})
        else:

            messages.error(request,"failed to create account ..!")
            return render(request,"register.html",{"form":form})        

#login    >>>>>>>>>>>>>>>>>>>>>>>>>>>
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")

            print(uname)
            print(pwd)

            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                print("valid credentials")
                #start session
                login(request,user_object)
                print(request.user)# if no user anonymous user

                messages.success(request,"Login successfully")
                return redirect("mobile-all")
            else:
                print("invalid credentials")

            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})

#logout    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"Log out successfully")
        return redirect("signin")


        