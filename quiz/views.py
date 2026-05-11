from django.shortcuts import redirect, render
from django.db import transaction
from .models import *
from django.http import JsonResponse
import re
from django.contrib.auth.hashers import check_password, make_password
import secrets, uuid
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    if request.session.get("user_token"):
        all_course = Course.objects.all()
        context = {"all_course": all_course}
        return render(request, "Home.html", context)
    return redirect("/")


def register(request):

    with transaction.atomic():

        if (
            request.method == "POST"
            and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        ):

            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")

            if not email or not password:
                return JsonResponse(
                    {"success": False, "error": "Email and password are required."}
                )

            if UserInfo.objects.filter(email=email).exists():
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Email already taken, try another email.",
                    }
                )

            if not re.search(r"[a-zA-Z]", password):
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Password must contain at least one letter.",
                    }
                )

            if len(password) < 8:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Password must be at least 8 characters.",
                    }
                )

            hash_password = make_password(password, password)

            UserInfo.objects.create(email=email, password=hash_password)

            return JsonResponse({"success": True})

        return render(request, "Register.html")


def login(request):

    request.session.flush()

    with transaction.atomic():

        if (
            request.method == "POST"
            and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        ):

            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")

            user_qs = UserInfo.objects.filter(email=email)

            if user_qs.exists():

                if check_password(password, user_qs[0].password):

                    user_token = f"{secrets.token_hex()}{uuid.uuid4()}"

                    request.session["user_token"] = user_token
                    request.session["user_id"] = user_qs[0].id
                    request.session["email"] = user_qs[0].email

                    return JsonResponse({"success": True})

                else:
                    return JsonResponse(
                        {"success": False, "error": "Invalid email or password."}
                    )

            else:
                return JsonResponse(
                    {"success": False, "error": "Invalid email or password."}
                )

        return render(request, "Login.html")


def logout(request):

    request.session.pop("user_token", None)
    request.session.pop("user_id", None)
    request.session.pop("email", None)

    return redirect("/")


def submit_quiz(request, id):

    if not request.session.get("user_token"):
        return redirect("/")

    if request.method == "POST":

        quiz_questions = Questions.objects.filter(course_id=id)

        total_ques = quiz_questions.count()
        all_ques = total_ques * 5

        score = 0
        correct_answer = 0

        for question in quiz_questions:

            answer_ = request.POST.get(f"answer{question.id}")

            if answer_ and answer_ == question.answer:

                score += question.markes if question.markes else 5
                correct_answer += 1

        wrong_answers = total_ques - correct_answer

        # SAVE RESULT IN DATABASE
        user_id = request.session.get("user_id")

        if user_id:

            user = UserInfo.objects.get(id=user_id)
            course = Course.objects.get(id=id)

            QuizResult.objects.create(
                user=user,
                course=course,
                total_questions=total_ques,
                correct_answers=correct_answer,
                wrong_answers=wrong_answers,
                total_marks=all_ques,
                obtained_marks=score,
            )

        context = {
            "quiz_questions": quiz_questions,
            "quiz_id": id,
            "score": score,
            "total_ques": total_ques,
            "correct_answer": correct_answer,
            "wrong_answers": wrong_answers,
            "all_ques": all_ques,
        }

        return render(request, "Quizresult.html", context)

    else:

        course_ques = Questions.objects.filter(course_id=id)

        try:
            course_name = Course.objects.get(id=id)

        except Course.DoesNotExist:
            return redirect("/home/")

        if not course_ques.exists():
            return redirect("/home/")

        context = {
            "course_ques": course_ques,
            "count_time": course_ques.count() * 30 * 1000,
            "course_name": course_name,
        }

        return render(request, "Quiz.html", context)


def contact_us(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        name = request.POST.get("name", "").strip()
        message = request.POST.get("message", "").strip()

        if email and name and message:

            # Save in database
            ContactForm.objects.create(email=email, name=name, message=message)

            # Send real email
            send_mail(
                subject=f"Quiz Website Contact Message {name}",
                message=f"""
Name: {name}

Email: {email}

Message:
{message}
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email, "youremail@gmail.com"],
                fail_silently=False,
            )

        return redirect("/contact_us/")

    return render(request, "Contact.html")
