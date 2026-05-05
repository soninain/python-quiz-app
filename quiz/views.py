from django.shortcuts import redirect, render
from django.db import transaction
from .models import *
from django.http import JsonResponse
import re 
from django.contrib.auth.hashers import check_password,make_password
import secrets,uuid
import time
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    if request.session.get("user_token"):
        all_course = Course.objects.all() 
        if all_course:
            context = {"all_course":all_course}
            return render(request,"Home.html",context)
  
    return redirect ("/")
    


def register(request):
    # try:
        with transaction.atomic():
            print("regitser")
            if request.method =="POST"  and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                email = request.POST["email"]
                print(email)
                password = request.POST["password"]
                if UserInfo.objects.filter(email=email):
                     return JsonResponse(
                        {
                            "success": False,
                            "error": "Email already taken try another email",
                        }
                    )
                elif not re.search(r"[a-zA-Z]", password):
                     return JsonResponse(
                        {
                            "success": False,
                            "error": "Password must contain at least one letter",
                        })
                elif len(password) < 8:
                        return JsonResponse( {
                            "success": False,
                            "error": "Password Should contain atleast 8 chracters",
                        })
                     
                else:
                    hash_password = make_password(password,password)
                    UserInfo.objects.create(email=email,password=hash_password)
                    user_token = f"{secrets.token_hex()}{uuid.uuid4()}"
                    request.session["email"] = email
                    request.session["user_token"] = user_token
                    return JsonResponse({"success": True})
            return render(request,"Register.html")
        

def login(request):
    # try:
        with transaction.atomic():
            if request.method =="POST"  and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                email= request.POST["email"]
                password = request.POST["password"]
                user_rgister =UserInfo.objects.filter(email=email)
                if user_rgister:
                    if check_password(password,user_rgister[0].password):
                       user_token = f"{secrets.token_hex()}{uuid.uuid4()}"
                       request.session["user_token"] = user_token
                       request.session["user_id"] = user_rgister[0].id
                       return JsonResponse({"success": True})
                    else:
                            return JsonResponse(
                                {"success": False, "error": "Invalid username and password."}
                            )
                else:
                    return JsonResponse(
                        {"success": False, "error": "Invalid username and password"}
                    )             
            return render(request,"Login.html")

def logout(request):
    del request.session["user_token"]
    return redirect ("/")
        

def submit_quiz(request,id):
    if request.session.get("user_token"):
        print(id)
        if request.method == "POST" :
            answers = request.POST.get("answer.id")
            print("Answers: ",answers)
            quiz_questions= Questions.objects.filter(course_id=id)
            all_ques = quiz_questions.count() * 5
            total_ques  = len(quiz_questions)
            answer_list = []
            score = 0
            correct_answer = 0
            for answer in quiz_questions:
                answer_ = request.POST.get(f"answer{answer.id}")
                if answer_ == answer.answer:
                    score += 5
                    correct_answer = score//5
                answer_list.append(answer_)
            context = {"quiz_questions":quiz_questions, "quiz_id":id, "score": score,"total_ques":total_ques,"correct_answer":correct_answer,"all_ques":all_ques}
            return render(request,"Quizresult.html",context)
        else:
            course_ques = Questions.objects.filter(course_id=id)
            course_name = Course.objects.get(id= id)
            if course_ques:
                context = {"course_ques":course_ques,"count_time":course_ques.count()*30*1000,"course_name":course_name}
                return render (request,"Quiz.html",context)
    return redirect ("/")

@csrf_exempt
def contact_us(request):
    if request.method == "POST":
        email=request.POST.get("email")
        name= request.POST.get("name")
        message= request.POST.get("message")
        ContactForm.objects.create(email=email,name=name,message=message)
        return redirect("/")
    return render (request,"Contact.html")
     


def test(request):
     pass