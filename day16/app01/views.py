from django.shortcuts import render,redirect,HttpResponse
from django.core import validators
from django.core.exceptions import ValidationError
from django import forms

from app01.utils.pagination import Pagination
# Create your views here.

from app01 import models
def sql_list(request):
    from django.db import connection

    queries = connection.queries
    for query in queries:
        print(query['sql'])
    context = queries if queries else "<没有SQL>"
    return HttpResponse(context)

def depart_list(request):
    # models.Department.objects.create(title="研发部")
    query_set = models.Department.objects.all()
        # 分页操作
    pagination = Pagination(request, query_set)
    context = {
        "depart_list":pagination.page_query_set,
        "page_outhtml":pagination.html(),
    }
    return render(request, "depart_list.html",context)

def depart_add(request):
    if request.method == 'GET':
        return render(request, "depart_add.html")
    else:
        # print(request.POST)
        title = request.POST.get("title")
        models.Department.objects.create(title=title)

        return redirect("/depart/list")

def depart_del(request):
    req_id = request.GET.get("id")
    models.Department.objects.filter(id=req_id).delete()
            
    return redirect("/depart/list")

def depart_edit(request):
    if request.method == 'GET':
        req_id = request.GET.get("id")
        ret_obj = models.Department.objects.filter(id=req_id).first()
        return render(request, "depart_edit.html",{"depart":ret_obj})
    else:
        # print(request.POST)
        req_id = request.POST.get("id")
        req_title = request.POST.get("title")
        models.Department.objects.filter(id=req_id).update(title=req_title)
        return redirect("/depart/list")
    
def depart_edit2(request,req_id):
    if request.method == 'GET':
        # req_id = request.GET.get("id")
        ret_obj = models.Department.objects.filter(id=req_id).first()
        return render(request, "depart_edit.html",{"depart":ret_obj})
    else:
        # print(request.POST)
        req_id2 = request.POST.get("id")
        if req_id==int(req_id2) :
            req_title = request.POST.get("title")
            models.Department.objects.filter(id=req_id).update(title=req_title)
        return redirect("/depart/list")
   

def user_list(request):
    query_set = models.UserInfo.objects.all()
    # 分页操作
    pagination = Pagination(request, query_set)
    context = {
        "user_list":pagination.page_query_set,
        "page_outhtml":pagination.html(),
    }
    return render(request, "user_list.html",context)

def user_add(request):
    if request.method == 'GET':
        query_set = models.Department.objects.all()
        content ={
            "depart_list":query_set,
            "gender_choices":models.UserInfo.gender_choices
            }
        
        return render(request, "user_add.html",content)
    else:
        # print(request.POST)
        { 'name': ['谢谢谢谢'], 'login_account': ['XXXX'], 'password': ['XXXXXXX'], 'gender': ['1'], 'age': ['35'], 'account': ['2222'], 'depart': ['1']}

        name = request.POST.get("name")
        login_account = request.POST.get("login_account")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        account = request.POST.get("account")
        req_depart_id = request.POST.get("depart")
        depart = models.Department.objects.filter(id=req_depart_id).first()
        
        models.UserInfo.objects.create(name=name, 
                                         login_account=login_account,
                                         password=password,
                                         gender=gender,
                                         age=age,
                                         account=account,
                                         depart=depart)

        return redirect("/user/list")

def user_edit(request,uid):

    if request.method == 'GET':
        
        # req_id = request.GET.get("id")
        ret_obj = models.UserInfo.objects.filter(id=uid).first()
        query_set = models.Department.objects.all()
        content ={
            "user":ret_obj,
            "depart_list":query_set,
            "gender_choices":models.UserInfo.gender_choices
            }

        return render(request, "user_edit.html",content)
    else:
        # print(request.POST)
        id = request.POST.get("id")
        name = request.POST.get("name")
        login_account = request.POST.get("login_account")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        account = request.POST.get("account")
        form_depart_id = request.POST.get("depart")
        create_time = request.POST.get("create_time")
        depart = models.Department.objects.filter(id=form_depart_id).first()

        print(request.POST)
        models.UserInfo.objects.filter(id=id).update(id=id,
                                                    name=name, 
                                                    login_account=login_account,
                                                    password=password,
                                                    gender=gender,
                                                    age=age,
                                                    account=account,
                                                    depart=depart,
                                                    create_time=create_time)
        return redirect("/user/list")

def user_delete(request,pid):
    models.UserInfo.objects.filter(id=pid).delete()
    return redirect("/user/list")

def pretty_list(request):
    print(type(request))
    # for num in range(1,400):
    #     models.PrettyNum.objects.create(mobile=str(13920001000+num), price=1.01+num,level=1,status=0)
    query_dict = {}
    req_q = request.GET.get("q","")
    req_page = request.GET.get("page",1)
    req_pagesize = request.GET.get("pagesize",10)
    if req_q:
        query_dict["mobile__contains"]=req_q
    query_set = models.PrettyNum.objects.filter(**query_dict).order_by("id")
    # 分页操作
    pagination = Pagination(request, query_set)
    context = {
        "pretty_list":pagination.page_query_set,
        "page_outhtml":pagination.html(),
        "q":req_q,
    }
    return render(request, "pretty_list.html", context)

    # return HttpResponse("")

class PrettyModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[validators.RegexValidator(r"^1[3-9]\d{9}$","手机号格式错误")]
    )
    # price = forms.DecimalField(label="价格", widget=forms.NumberInput)

    class Meta:
        model = models.PrettyNum
        fields=["mobile","price","level","status"]
        # fields = "__all__"
        pass

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            # print(name,field)
            # if name=='price':
            #     field.widget=forms.NumberInput
            #     pass
            from django.forms.fields import  DecimalField
            field.widget.attrs={"class":"form-control","placeholder":field.label}
    
    def clean_mobile(self):
        input_mobile = self.cleaned_data["mobile"]
        # input_mobile = self.cleaned_data["mobile"]
        is_exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=input_mobile,).exists()
        # print(input_mobile)
        if is_exists:
            raise ValidationError("手机号已存在")
        return input_mobile
    pass

def pretty_add(request):
    form = PrettyModelForm()
    content = { "form":form}
    if request.method == 'GET':
        return render(request, "pretty_add.html",content)
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list") 
    content = { "form":form}
    return render(request, "pretty_add.html",content)

class PrettyEditModelForm2(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields=["price","level","status"]
        # fields = "__all__"
        pass

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs={"class":"form-control","placeholder":field.label}
    

    pass

class PrettyEditModelForm(PrettyModelForm):
    # mobile = forms.CharField(label="手机靓号", disabled=True)
    pass

def pretty_edit(request,pid):
    ret_obj = models.PrettyNum.objects.filter(id=pid).first()
    
    if request.method == 'GET':
        form = PrettyEditModelForm(instance=ret_obj)
        content = { "form":form}
        return render(request, "pretty_edit.html",content)
    
    form = PrettyEditModelForm(data=request.POST, instance=ret_obj)
    if form.is_valid():
        form.save()
        return  redirect("/pretty/list") 
    content = { "form":form}
    return render(request, "pretty_edit.html",content)

def pretty_delete(request,pid):
    pass

def pretty_delete(request,pid):
    models.PrettyNum.objects.filter(id=pid).delete()
    return redirect("/pretty/list")


