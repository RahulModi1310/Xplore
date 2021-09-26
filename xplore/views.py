from hashlib import sha256
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Users,Course
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tokenCreator import generateToken
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import connection
import json
cursor = connection.cursor()
regEmail = ""
def register(request):
    if request.method=="GET":
        return render(request,"main.html")
    username = request.POST.get('username',"demoName")
    password = request.POST.get('password',"noPass")
    email = request.POST.get("email","someEmail")
    confPass = request.POST.get('confPass','somePass')
    if password==confPass:
        emailTaken = False
        usernameTaken = False
        accountInactive = True
        global regEmail
        regEmail = email
        if username!="demoName" and password!="noPass" and email!="someEmail":
            try: 
                usr1 = Users.objects.get(username=username)
                if usr1.username == username:
                    usernameTaken=True
            except Users.DoesNotExist:
                usernameTaken=False    
            if usernameTaken:
                return HttpResponse("Username is already taken by someone")
            else:    
                try:
                    usr = Users.objects.get(email=email)
                    if usr.accountActive==True:
                        accountInactive=False
                    if usr.email==email:
                        emailTaken=True    
                    
                except Users.DoesNotExist:
                    emailTaken = False
                if emailTaken==False and accountInactive:
                    password = sha256(password.encode()).hexdigest()
                    print(username,password,email)
                    user = Users(username=username,password=password,email=email,accountActive=False)

                # Send the email
                    subject = "Account confirmation"
                
                    token = generateToken(email)
                    url = 'http://localhost:8000/confirm/{}'.format(token)
                    message = render_to_string('regEmail.html',{'link':url})
                    plain_message = strip_tags(message)
                    from_email = 'pwnworld10@gmail.com'
                    to = email
                    send_mail(subject,plain_message,from_email,[to],html_message=message)
                    user.save()
                    return HttpResponse('Confirmation mail sent')
                elif emailTaken==True and accountInactive:
                    subject = "Account confirmation"
                    token = generateToken(email)
                    url = 'http://localhost:8000/confirm/{}'.format(token)
                    message = render_to_string('regEmail.html',{'link':url})
                    plain_message = strip_tags(message)
                    from_email = 'pwnworld10@gmail.com'
                    to = email
                    send_mail(subject,plain_message,from_email,[to],html_message=message)
                    return HttpResponse('Confirmation mail sent')
                elif emailTaken and accountInactive==False:
                    return HttpResponse("Email is already taken")    

        else:
            return render(request,"main.html")  
    else :
        return HttpResponse("Passwords do not match")        


def signin(request):
    if request.POST:
        email = request.POST.get('email','invalid')
        password = request.POST.get('password','invalid')
        password = sha256(password.encode()).hexdigest()
        try:
            user = Users.objects.get(email=email)
            if user.accountActive==True:
                email = user.email
                username = user.username
                
                authUser =authenticate(request,username=username,password=password)
                if authUser is not None:
                    login(request,authUser)
                    return redirect("/courses/")
                else:
                    return HttpResponse("Invalid credentials")  

            else:
                return HttpResponse("Your account is not activated. Please check the email sent before. If it does not work, register again")    
        except Users.DoesNotExist:
            return HttpResponse("Account with that email does not exist")
    return render(request,"main.html")

@login_required(login_url='/main/')
def courses(request):
    coursesToSend = []
    cursor.execute("SELECT * FROM xplore_course;")
    courses = cursor.fetchall();
    for course in courses:
            crs = {
                "courseName":course[1],
                "coursePlatform":course[2],
                "imageUrl":course[3],
                "courseUrl":course[4],
                "rating":course[5],
                "details":course[6],
                "status":course[7]
            }
            coursesToSend.append(crs)
    if request.method=="POST":
        coursesToSend = []
        filterMode = request.POST.get("filter")
        if filterMode == "Free":
            cursor.execute("SELECT * FROM xplore_course WHERE status='free';")
            courses = cursor.fetchall()
        elif filterMode=="Paid":
            cursor.execute("SELECT * FROM xplore_course WHERE status='paid';")
            courses = cursor.fetchall()
        elif filterMode=="Rating":
            cursor.execute("SELECT * FROM xplore_course ORDER BY rating DESC;")
            courses = cursor.fetchall()
        for course in courses:
            crs = {
                "courseName":course[1],
                "coursePlatform":course[2],
                "imageUrl":course[3],
                "courseUrl":course[4],
                "rating":course[5],
                "details":course[6],
                "status":course[7]
            }
            coursesToSend.append(crs)
        return render(request,"courses.html",{'courses':coursesToSend})

    return render(request,"courses.html",{'courses':coursesToSend})
def confirm(request,token):
    try:
        user = Users.objects.get(email=regEmail)
        if user.accountActive==False:
            user.accountActive = True
            user.save()
            username = user.username
            password = user.password
            email = user.email
            userAuth = User.objects.create_user(username,email,password)
            userAuth.save()
    except Users.DoesNotExist:
        return HttpResponse("Either your account has been activated or there was some error")  
    return HttpResponse("Account confirmed! Go to the homepage and signin")

def logOut(request):
    logout(request)
    return render(request,"main.html")



def insert(courseName,coursePlatform,imageUrl,courseUrl,rating,details,status):
    mod = Course.objects.create(courseName=courseName,coursePlatform=coursePlatform,imageUrl=imageUrl,courseUrl=courseUrl,rating=rating,details=details,status=status)
    mod.save()

def redi(request):
    return redirect("/main/")

def main(request):
    # insert("Competitive Programming","Geeks for Geeks","https://pbs.twimg.com/profile_images/1304985167476523008/QNHrwL2q.jpg","https://www.geeksforgeeks.org/","5","Whether you want to learn algorithms, data structures or it is the programming language on its own which interests you, GeeksforGeeks has covered everything!","free")
    # insert("Competitive Programming","Codeforces","https://res.cloudinary.com/practicaldev/image/fetch/s--N2_RJe5R--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/cer3l19eex0wy900b101.jpg","https://codeforces.com/","5","Codeforces is one of the best platforms for competitive coding and is usually known for its short challenges/contests where programmers from every corner of the world participate.","free")
    # insert("Ethical Hacking","Hack the Box","https://media-exp1.licdn.com/dms/image/C4D0BAQHvMeJi2yXd1A/company-logo_200_200/0/1593697095085?e=2159024400&v=beta&t=CWD6gscCVPvLfUcYoF6he_keM9GbK5Igr9kqCl6Zu08","https://www.hackthebox.eu/","5","Hack The Box is an online platform allowing you to test your penetration testing skills and exchange ideas and methodologies with other members of similar interests. It contains several challenges that are constantly updated.","paid")
    # insert("Web Penetration Testing","Pentester Labs","http://blog.razrsec.uk/content/images/2019/11/pt-lab-header-4.png","https://pentesterlab.com/","4","“PentesterLab is an awesome resource to get hands-on, especially for newbies in web penetration testing or pentesting in general.","paid")
    # insert("Web Penetration Testing","Portswigger","https://pbs.twimg.com/profile_images/1271377767091843073/ZIBb6Ur6_400x400.png","https://portswigger.net/","5","PortSwigger is a global leader in cybersecurity. We provide solutions that bring productivity, agility, reliability, and excellence to your web application security strategy.Our products and research help tens of thousands of users worldwide find and remediate vulnerabilities to keep your applications up and running. No matter where you are in your security maturity journey, PortSwigger is here to help you secure the web.","free")
    # insert("Web Development","The Complete 2020 Web Development Bootcamp","https://themuellenator.github.io/images/mountain.png","https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwiK1-_U-5rzAhUqmGYCHXH2Cy8YABAAGgJzbQ&ae=2&ohost=www.google.com&cid=CAESQOD2etJSN4gjehRjkTM4O7BfEiTxmMXI5-EGPv1xEqfmC0SKkLObNWbvMOzqQGZg6TqKuu9x8IGVSyxol8GZZLs&sig=AOD64_1sSYqgiuNnLjxBdb3QWSgpykbdPA&q&nis=1&adurl&ved=2ahUKEwje4-jU-5rzAhXnumMGHW38CVkQ0Qx6BAgCEAE","5","The course included detailed explanation and projects related to HTML, CSS, JS, Node.JS, Git, MongoDB and React","paid")
    # insert("Game Development","Brackeys","https://pbs.twimg.com/profile_images/935811479458189312/Oz5h25iF_400x400.jpg","https://www.youtube.com/user/brackeys","5","The best course available on the internet for Game Development","free")
    # insert("Programming Languages","w3 schools","https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/W3Schools_logo.svg/2175px-W3Schools_logo.svg.png","https://www.w3schools.com/","5","w3 schools is a platform where you can learn different programming languages like Python, JavaScript, C, SQL, etc.","free")

    return render(request,"main.html")
