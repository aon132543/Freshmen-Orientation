from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blogs.models import OderCommand, UserProfile,Like,indexpic
from django.http import HttpResponse,HttpResponseRedirect


from blogs.form import signUpForm,setting_pic,setUp



from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from  django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .form import UserProfileForm,setting_pic
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib import messages
from django.conf import settings

from django.views.generic import View

import random
from .models import UserOTP
from django.core.mail import send_mail
from django.core.mail import EmailMessage, EmailMultiAlternatives


from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse
from .utils import token_generator
from django.template.loader import get_template
from django.template import Context





# Create your views here.


def hello (request):
    like_obj = Like.objects.filter(status=True)
    users = User.objects.filter()
    maxcount = 0
    maxobj = None
    lstobj = []
    for user in users:
        countlike =  len(like_obj.filter(idmy_id = user.id))
        lstobj.append([user,countlike])
    lstobj.sort(key=lambda x:x[1],reverse=True)
    
    #เอา obj UserProfile ของ TOP 5
    top1 = UserProfile.objects.get(user_id = lstobj[0][0])
    top2 = UserProfile.objects.get(user_id = lstobj[1][0])
    top3 = UserProfile.objects.get(user_id = lstobj[2][0])
    top4 = UserProfile.objects.get(user_id = lstobj[3][0])
    top5 = UserProfile.objects.get(user_id = lstobj[4][0])
    context = {'top1' : top1.profile_pic.url, 
               'top2': top2.profile_pic.url,
               'top3':top3.profile_pic.url,
               'top4':top4.profile_pic.url,
               'top5':top5.profile_pic.url}
    return render(request,'index.html',context)

def page1(request):
    openserver = 1
    if openserver == 1:

        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request,user)
                    return redirect('appsend')
                else:
                    return redirect('index')


        else:
            form =AuthenticationForm()

        return render(request,'page1.html',{'form':form})
    else:
        return render(request,'errorlayout1.html')

def page2(request):
    return render(request,'contract.html')







def page3(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            emailfind = User.objects.filter(email__exact=str(email))
            User_Obj = User.objects.get(email__exact=str(email))
            email_Check = UserProfile.objects.get(user_id=User_Obj.id)
        except User.DoesNotExist:
            messages.success(request,"อีเมลไม่มีในระบบ ไม่ได้ลงทะเบียนไว้ กรุณาติดต่อ admin")
            return render(request,'login_emailmim.html',{"mes":True})
        
        if int(email_Check.count) == 1:
            messages.error(request,"เคยลงทะเบียนไปแล้ว ถ้า หากมั่นใจแล้วว่าถูกต้อง ติดต่อรุ่นพี่")
            return render(request,'login_emailmim.html')
        else: 
            user = User.objects.get(email__exact=str(email))
            #path_to_view
            #-getting domain we are on
            # -reletive url to verification
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            domain =  get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
            
            activate_url = 'https://'+domain+link
            
            
            htmly     = get_template('email.html')
            
            con = ({ "activate_url":activate_url})
            
            html_content = htmly.render(con)
            
            
            email_subject ="ปกส้ม CPE|ยืนยัน"
            email_body = 'สวัสดีครับ ลิ้งค์ที่ให้เป็นเป็นหน้าตั้งค่าบัญชีนะครับ\n'+'อธิบาย \n'+'Username และ Password ไว้สำหรับ LOGIN เข้าสู่ระบบ \n'+'กรุณา อัพโหลดรููปโปรไฟล์และ รูปพื้นหลังด้วย\n'+'<a href='+'"'+activate_url+' " ' +">"+"เปิดใช้งาน"+"</a>"
            email = EmailMultiAlternatives(
                email_subject,
                email_body,
                'no reply',
                [email],
            )
            email.attach_alternative(html_content,"text/html")
            email.send(fail_silently=False)
            messages.success(request,"ส่งอีเมลไปแล้วนะ")
            return render(request,'login_emailmim.html',{'send':True})
    return render(request,'login_emailmim.html')

def page4(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            emailfind = User.objects.filter(email__exact=str(email))
            User_Obj = User.objects.get(email__exact=str(email))
            email_Check = UserProfile.objects.get(user_id=User_Obj.id)
        except User.DoesNotExist:
            messages.success(request,"อีเมลไม่มีในระบบ ไม่ได้ลงทะเบียนไว้ กรุณาติดต่อ admin")
            return render(request,'login_emailmim.html',{"mes":True})
        
        if len(emailfind)==0 :
            messages.error(request,"กรอกอีเมลผิด ถ้า หากมั่นใจแล้วว่าถูกต้อง ติดต่อรุ่นพี่")
            return render(request,'login_emailmim.html')
        else: 
            user = User.objects.get(email__exact=str(email))
            #path_to_view
            #-getting domain we are on
            # -reletive url to verification
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            domain =  get_current_site(request).domain
            link = reverse('forget',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
            
            activate_url = 'https://'+domain+link
            
            
            htmly     = get_template('emailpassword.html')
            
            con = ({ "activate_url":activate_url})
            
            html_content = htmly.render(con)
            
            
            email_subject ="ปกส้ม CPE|reset password"
            email_body = 'สวัสดีครับ ลิ้งค์ที่ให้เป็นเป็นหน้าตั้งค่าบัญชีนะครับ\n'+'อธิบาย \n'+'Username และ Password ไว้สำหรับ LOGIN เข้าสู่ระบบ \n'+'กรุณา อัพโหลดรููปโปรไฟล์และ รูปพื้นหลังด้วย\n'+'<a href='+'"'+activate_url+' " ' +">"+"เปิดใช้งาน"+"</a>"
            email = EmailMultiAlternatives(
                email_subject,
                email_body,
                'no reply',
                [email],
            )
            email.attach_alternative(html_content,"text/html")
            email.send(fail_silently=False)
            messages.success(request,"ส่งอีเมลไปแล้วนะ")
            return render(request,'login_emailmim.html',{'send':True})
    return render(request,'forgotpassword.html')



def forget(request,uidb64,token):
    id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(pk=id)
    password1 = request.POST.get('password1')
    password2 = request.POST.get('passsword2')
    if request.method == 'POST':
        if password1 != password2:
            messages.error(request,"กรอกรหัสยืนยันไม่ตรงกัน")
            mess= {'mes':False}
            return render(request,'forgotpasswordemail.html',mess)
        else:   
            hashed_pass =make_password(password1)
            user.update(password = hashed_pass)
            messages.success(request,"Pssword ถูกเปลี่ยนเรียบร้อย กรุณา LOGIN")
            mess= {'mes':True}
            return redirect('page1')
            
            
    
    return render(request,'forgotpasswordemail.html')

class VerificationView(View):
    def get(self, request,uidb64,token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        request.session["userid"] = id
        return redirect("setup")
    

class LoginView(View):
    def get(self,request):
        return render(request,page1)

def setup(request):
    
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('passsword2')
    displayname = request.POST.get('displayname')

    
    userid = request.session['userid']
    user = UserProfile.objects.get(user_id=userid)
    form = UserProfileForm(instance=user)
    user_profile_obj = UserProfile.objects.get(user_id = userid)

    if int(user.count) == 0 :
        if request.method == 'POST':
            form = UserProfileForm(request.POST,request.FILES,instance=user)
            
            if password1 != password2:
                messages.error(request,"กรอกรหัสยืนยันไม่ตรงกัน")
                mess= {'mes':False,'form':form}
                return render(request,'setup_test.html',mess)
            
            elif form.is_valid():
                hashed_pass =make_password(password1)
                oder = User.objects.filter(id=userid)
                usernamefine = User.objects.filter(username =username)
                if len(usernamefine) != 0 :
                    messages.error(request,"Username นี้ มีผู้ใช้แล้ว")
                    mess= {'mes':False,'form':form}
                    return render(request,'setup_test.html',mess)
                user_profile_obj.displayname = displayname
                oder.update(password = hashed_pass)
                oder.update(username = username)
                user.count = 1
                oder.is_active =1
                user.save()
                form.save()
                messages.success(request,"ลงทะเบียนครั้งแรกเรียบร้อย กรุณา LOGIN")
                mess= {'mes':True}
                return redirect('page1')
        context = {'form':form}
        return render(request,'setup_test.html',context)
    messages.success(request,"เคยลงทะเบียนแล้วครับ LOGIN ได้เลย !!")
    return redirect('page1')












def adduser(request):
    return render(request,'confirm1.html')

@login_required (login_url='page1')
def adduser_admin(request):
    useradminor = request.user.is_superuser
    if useradminor == 1:


        if request.method =='POST':
            form = signUpForm(request.POST)
            profile_form = UserProfileForm(request.POST)

            if form.is_valid() and profile_form.is_valid():
                # บันทึกข้อมูล
                user = form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()




                # บันทึก GROUP
                # ดึง username มาใช้
                username = form.cleaned_data.get('username')
                #คิวรี่
                signUpUser =User.objects.get(username=username)
                user_group = Group.objects.get(name = "user")

                user_group.user_set.add(signUpUser)

                #--------

        else:
            form = signUpForm()
            profile_form = UserProfileForm()
        context = {'form':form ,'profile_form':profile_form}
        return render(request,'adduser.html',context)
    else:
        return  redirect(page1)

def resualt (request):
    username = request.POST['user2']
    std = request.POST['std']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    edu = request.POST['edu']
    user = User.objects.create_user(
        username = username,
        password= "0000",
        #std = std ,
        first_name = firstname,
        last_name = lastname,
        #edu = edu

    )
    user.save()
    return render(request,'resualt.html')



@login_required (login_url='page1')
def appsend(request):
    if request.user.is_authenticated:
        idcpe = str(request.user.id)
        test = UserProfile.objects.all()
        oders = OderCommand.objects.filter(idcpesend=idcpe)
        like_obj = Like.objects.all()

        paginator = Paginator(oders, 8)

        try:
           page = int (request.GET.get('page','1'))
        except:
            page = 1
        try :
            productperPage = paginator.page(page)
        except(EmptyPage,InvalidPage) :
            productperPage = paginator.page(paginator.num_pages)

        userobj = User.objects.all()
        contxt = {"oders":productperPage,"test":test,"likes":like_obj,"User":userobj}



    return render(request,'appsend.html',contxt)

def _card_id(request):
    card = request.session.session_key
    if not card :
        card = request.session.create()

    return  card
def signOutView(request):
    logout(request)
    return  redirect('index')

@login_required (login_url='page1')
def license (request):
    edumy =request.user.userprofile.edu
    if edumy == "1":
        
        if request.method == 'POST':
            iduser = request.POST.get('iduser')
            try:
                user_Profile = UserProfile.objects.get(user_id=iduser)
            except UserProfile.DoesNotExist:
                messages.success(request,"ไม่มี ID นี้ หรือกรอกผิด")
                return render(request,'license.html',{"mes":True})
            print(user_Profile.cpenumber)
            messages.success(request,"รายละเอียด")
            return render(request,'license.html',{"user_Profile":user_Profile})
        return render(request, 'license.html')
            
    else:
        return redirect('appsend')




def final (request,myid,idsendto):
    print("Myid : ",myid)
    print("idsendto:",idsendto)
    if request.user.is_authenticated:
        idsend =idsendto #ส่งหาเขา
        idmy = myid #ไอดีของฉัน
        name = User.objects.all()
        idrequestsendmy = OderCommand.objects.filter(idcpesend = idmy)
        idsend = int(idsend)
        boolen = False
        # บันทึกข้อมูล
        context = {"mes":True}
        if idsend != request.user.id:
            if boolen == False:
                for i in OderCommand.objects.filter(idcpesend = idmy):
                    if i.idcpeto == idsend:
                        messages.success(request,"น้องเคยขอลายเซ็นคนนี้ไปแล้วนะ")
                        return render(request, 'license.html',context)
                        #return redirect(license)
                    else:
                        boolen = True
                else:
                    oder = OderCommand.objects.create \
                            (
                            idcpesend=request.user.id,
                            idcpeto=idsend,
                            status=False
                        )
                    messages.success(request,"ส่งคำขอไปแล้วนะ")
                    oder.save()
                    return render(request, 'license.html',context)
                    #return redirect(license)



        else:
            messages.success(request,"เราจะกรอก ID ตัวเองไม่ได้น้าเว้ย เราจะปั้มยอดลายเซ็นหรอ") 
            
            #return redirect(license)
            return render(request, 'license.html',context)



@login_required (login_url='page1')
def confirmlicn(request):
    if request.user.is_authenticated:
        idcpe = str(request.user.id)
        oders = OderCommand.objects.filter(idcpeto=idcpe)
        test = UserProfile.objects.all()
        like_obj = Like.objects.all()
        userobj = User.objects.all()	

        paginator = Paginator(oders, 5)
            
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        try:
            productperPage = paginator.page(page)
        except(EmptyPage, InvalidPage):
            productperPage = paginator.page(paginator.num_pages)
        if request.method == 'POST':
            id_UserProfile = request.POST.get('userid')
            object_UserProFile =  UserProfile.objects.filter(id = id_UserProfile)
            context = {'object_UserProFile':object_UserProFile}

            messages.success(request,context,"helloworld")
            return render(request,'confirmlicnew.html',{"oders":productperPage,"test":test,"likes":like_obj,"User":userobj})       

    return render(request,'confirmlicnew.html',{"oders":productperPage,"test":test,"likes":like_obj,"User":userobj})

def confirmsend(request,oder_id):
    if request.user.is_authenticated:
        oder = OderCommand.objects.filter(id=oder_id)
        oder.update(status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def confirmsendall(request,idcpeto):
    itemoder_obj = OderCommand.objects.filter(idcpeto=idcpeto)
    itemoder_obj = itemoder_obj.filter(status=False)
    if len(itemoder_obj) == 0:
        messages.success(request,"เราเซ็นทั้งหมดแล้วหนิ ? ")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    print(itemoder_obj)
    for oder in itemoder_obj:
        oder.status =True
        oder.save()
    messages.success(request,"เซ็นทั้งหมดให้แล้วนะ  ")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def removeodercheck(request,oder_id):
    if request.user.is_authenticated:
        oder = oder_id
        requestsend = {'id':oder}
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removeoder(request,oder_id):
    if request.user.is_authenticated:
        oder = OderCommand.objects.filter(id=oder_id)
        oder.delete()
        messages.success(request,"ลบเรียบร้อยแล้วครับ")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def error(request):
    return render(request,'error.html')

def findstd(request):
    stdsend =request.POST['std']
    userprofilestd = UserProfile.objects.filter(std = stdsend )
    for i in userprofilestd:
        userid = i.user_id
        edu = i.edu
        nickname = i.nickname
        cpenumber = i.cpenumber
        count = i.count
    object_user = User.objects.filter(id = userid)
    for k in object_user:
        username = k.username
    if count == "0":
        userprofilestd.update(count=1)
        requestsend = {"userid":userid,"edu":edu,"nickname":nickname,"username":username,"cpenumber":cpenumber}
        return render(request,'login1_2.html',requestsend)
    else:
        return render(request, 'errori.html')


def setpassword (request):
    password =request.POST['password']
    iduser = request.POST['userid']
    hashed_pass = make_password(password)
    oder = User.objects.filter(id = iduser)
    oder.update(password = hashed_pass)
    return  redirect(page1)

@login_required (login_url='page1')
def admincheckinput (request):
    useradminor = request.user.is_superuser
    if useradminor == 1:
        return render(request,'admincheckinput.html')
    else:
        return redirect(page1)


@login_required (login_url='page1')
def admincheck (request):
    useradminor = request.user.is_superuser
    if useradminor == 1:
        stdsend = request.POST['std']
        userprofilestd = UserProfile.objects.filter(std=stdsend)
        for i in userprofilestd:
            userid = i.user_id
            edu = i.edu
            nickname = i.nickname
            cpenumber = i.cpenumber
            count = i.count
        test = UserProfile.objects.all()
        oders = OderCommand.objects.filter(idcpesend=userid)

        odercout = 0
        for k in oders :
            if k.idcpesend == userid:
                odercout += 1

        contxt = {"oders": oders, "test": test,"nickname":nickname,"cpenumber":cpenumber,"userid":userid,"odercout":odercout}
        return render(request,'admincheck.html',contxt)
    else:
        return redirect(page1)

@login_required(login_url='page1')
def checklicense (request):
    if request.user.is_authenticated:
        edumy = request.user.userprofile.edu
        if edumy == "1":

            idcpe = int(request.user.id)
            oders = OderCommand.objects.filter(idcpesend=idcpe)
            countall = 0
            #เซ็นให้แล้ว
            edu1a =0
            edu2a =0
            edu3a =0
            edu4a =0
            #ยังไม่เซ็น
            edu1s =0
            edu2s =0
            edu3s =0
            edu4s =0






            for i in oders:
                test = UserProfile.objects.filter(user_id = i.idcpeto)
                if i.idcpesend == idcpe:
                    countall += 1
                for k in test :
                    if k.edu == "1":
                        if i.status == True:
                            edu1a += 1
                        else:
                            edu1s += 1
                    elif k.edu == "2":
                        if i.status == True:
                            edu2a += 1
                        else:
                            edu2s += 1
                    else:
                        if i.status == True:
                            edu3a += 1
                        else:
                            edu3s += 1
                    


            #จำนวนลายเซ็นต์ทั้งหมด
            edu1 = edu1s+edu1a
            edu2 = edu2s+edu2a
            edu3 = edu3s+edu3a
            edu4 = edu4s+edu4a

            #จำนวนลายเซ็นต์ที่ยังขาด
            sumedu1 = 70-edu1a
            sumedu2 = 40 -edu2a
            sumedu3 = 20 -edu3a
            sumedu4 =  20- edu4

            if sumedu1 < 0:
                sumedu1 = 0
            if sumedu2 < 0 :
                sumedu2 = 0
            if sumedu3 < 0 :
                sumedu3 = 0
            if sumedu4 <= 0 :
                sumedu4 = 0


            contxt = {"countall":countall,"edu1":edu1,"edu2":edu2,"edu3":edu3,"edu4":edu4,"sumedu1":sumedu1,
                      "sumedu2":sumedu2,"sumedu3":sumedu3,"sumedu4":sumedu4,
                      "edu1a":edu1a,"edu2a":edu2a,"edu3a":edu3a,"edu4a":edu4a,
                      "edu1s":edu1s,"edu2s":edu2s,"edu3s":edu3s,"edu4s":edu4s}
            return render(request,'checklicense.html',contxt)
        else:
            return render(request,'errorlayout2.html')

@login_required(login_url='page1')
def adminchecklicense(request,userid):
    useradminor = request.user.is_superuser
    if useradminor == 1:
        idcpe = userid
        oders = OderCommand.objects.filter(idcpesend=idcpe)
        countall = 0
        #เซ็นให้แล้ว
        edu1a =0
        edu2a =0
        edu3a =0
        edu4a =0
        #ยังไม่เซ็น
        edu1s =0
        edu2s =0
        edu3s =0
        edu4s =0






        for i in oders:
            test = UserProfile.objects.filter(user_id = i.idcpeto)
            if i.idcpesend == idcpe:
                countall += 1
            for k in test :
                if k.edu == "1":
                    if i.status == True:
                        edu1a += 1
                    else:
                        edu1s += 1
                elif k.edu == "2":
                    if i.status == True:
                        edu2a += 1
                    else:
                        edu2s += 1
                elif k.edu == "3":
                    if i.status == True:
                        edu3a += 1
                    else:
                        edu3s += 1
                else :
                    if i.status == True:
                        edu4a += 1
                    else:
                        edu4s += 1


            #จำนวนลายเซ็นต์ทั้งหมด
        edu1 = edu1s+edu1a
        edu2 = edu2s+edu2a
        edu3 = edu3s+edu3a
        edu4 = edu4s+edu4a

            #จำนวนลายเซ็นต์ที่ยังขาด
        sumedu1 = 106-edu1a
        sumedu2 = 50 -edu2a
        sumedu3 = 30 -edu3a
        sumedu4 =  20- edu4

        if sumedu1 < 0:
            sumedu1 = 0
        if sumedu2 < 0 :
            sumedu2 = 0
        if sumedu3 < 0 :
            sumedu3 = 0
        if sumedu4 <= 0 :
            sumedu4 = 0


        contxt = {"countall":countall,"edu1":edu1,"edu2":edu2,"edu3":edu3,"edu4":edu4,"sumedu1":sumedu1,
                      "sumedu2":sumedu2,"sumedu3":sumedu3,"sumedu4":sumedu4,
                      "edu1a":edu1a,"edu2a":edu2a,"edu3a":edu3a,"edu4a":edu4a,
                      "edu1s":edu1s,"edu2s":edu2s,"edu3s":edu3s,"edu4s":edu4s}
        return render(request,'adminchecklicense.html',contxt)


        return render(request,adminchecklicense)

    else:
        return redirect(page1)

def testlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('confirmlic')
        else:
            messages.error(request,"รหัสผิดครับ กรุณากรอกใหม่")
            return render(request,'login_mim.html',{'mes':True})
        
    return render(request,'login_mim.html')

@login_required(login_url='page1')
def setting(request):
    user_id = str(request.user.id)
    user = UserProfile.objects.get(user_id=user_id)
    form = UserProfileForm(instance=user)
    object_UserProFile = UserProfileForm(instance=user)
    if request.method == 'POST':
        if len(request.POST.get('display_name')) != 0:
       	   user.displayname = request.POST.get('display_name')
        if len(request.FILES)!=0:
            if request.FILES.get('image-profile',False):
                user.profile_pic = request.FILES.get('image-profile')
            if request.FILES.get('image-bg',False):
                user.profile_bg_pic = request.FILES.get('image-bg')
        user.save()
        messages.success(request,"สำเร็จ")
        return redirect('setting')
    context = {'form':form,'user_profile':user}
    return render(request,'setting.html',context)
    


#like sysyem
@login_required(login_url='page1')
def like_s(request,oder_id):
    if request.user.is_authenticated:
            oder = Like.objects.filter(id=oder_id)
            oder.update(status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
@login_required(login_url='page1') 
def like_d(request,oder_id):
    if request.user.is_authenticated:
            oder = Like.objects.filter(id=oder_id)
            oder.update(status=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#======================================

def test(request):
    return render(request,'test.html')
    
