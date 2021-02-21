from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import datetime #added for date
from django.db.models import Sum
from django.db.models import Count  #added to sum

def index(request):
    # if 'user_id' in request.session:
    #     user= User.objects.filter(id=request.session['user_id'])
    #     if user:
    #         return redirect('/dashboard')
    context ={
        'blogs':Blog.objects.all()
    }
    return render(request, 'index.html', context)

def login(request):
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            return redirect('/dashboard')
    if request.method =="GET":
        return render (request, 'login.html')
    if not User.objects.log_validation(request.POST['email'], request.POST['password']):
        messages.error(request, 'invalid Email/Password')
        return redirect('/login')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id']=user.id
    return redirect('/dashboard')

def register(request):
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            return redirect('/dashboard')
    if request.method == "GET":
        return redirect('/login')
    errors=User.objects.reg_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        password= request.POST['password']
        pw_hash= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create (
            first_name= request.POST['fname'],
            last_name= request.POST['lname'],
            email= request.POST['email'],
            password = pw_hash
        )
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')

def logout(request):
    request.session.flush()
    messages.success(request, "Successfully Logged Out")
    return redirect('/')



def dashboard(request):
    now = datetime.date.today()
    if 'activities' not in request.session:
        request.session ['activities']=[]
    if 'user_id' in request.session:
        user=User.objects.filter(id=request.session['user_id'])
        if user:
            context ={
                'user': user[0],
                'meals': Meal.objects.filter(date_eaten=now, eater=request.session['user_id']),
                'foods': Food.objects.all(),
                'date':now,
                'weights':Weight.objects.all(),
                'exercises':Exercise.objects.filter(date_done=now, exerciser=request.session['user_id']),
                'food_cals': Meal.objects.filter(date_eaten=now, eater=request.session['user_id']).aggregate(total_cals=Sum('meal__food_calories')),
                'exer_cals': Exercise.objects.filter(date_done=now, exerciser=request.session['user_id']).aggregate(total_cals=Sum('exer_calories')),
            }
        return render(request, 'dashboard.html', context)
    return redirect('/')


def edit(request):
    return render(request, 'edit.html')

def add_food(request):
    user = User.objects.get(id=request.session['user_id'])
    #no error but message isn't showing up
    message= "Added food to the log"
    activity_type = "add_food"
    request.session['activities'].append({'message':message, 'type':activity_type})
    if request.method == "POST":
        Food.objects.create(
            food_name= request.POST["food_name"],
            food_calories= request.POST["calories"],
            fat=request.POST["fat"],
            carbs=request.POST["carbs"],
            protein=request.POST["protein"],
        )
        food= Food.objects.last()
        Meal.objects.create(
            meal_tag=request.POST.get("meal_tag"),
            date_eaten=request.POST['date_eaten'],
            eater=user,
            meal= food,
        )
    return redirect('/dashboard')

def add_exercise(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        Exercise.objects.create(
            exercise_name= request.POST["exname"],
            exer_calories= request.POST["excals"],
            exerciser = user,
            date_done=request.POST["date_done"],
        )
    return redirect('/dashboard')

def remove_meal(request, meal_id):
    meal_to_delete=Meal.objects.get(id=meal_id)
    meal_to_delete.delete()
    return redirect('/dashboard')

def remove_exercise(request, exercise_id):
    exercise_to_remove= Exercise.objects.get(id=exercise_id)
    exercise_to_remove.delete()

    return redirect('/dashboard')

def profile(request):
    now = datetime.date.today()
    if 'user_id' in request.session:
        user=User.objects.filter(id=request.session['user_id'])
        if user:
            context ={
                'user': user[0],
                'meals': Meal.objects.filter(date_eaten=now, eater=request.session['user_id']),
                'foods': Food.objects.all(),
                'date':now,
                'weights':Weight.objects.all(),
                'exercises':Exercise.objects.filter(date_done=now, exerciser=request.session['user_id']),
                'food_cals': Meal.objects.filter(date_eaten=now, eater=request.session['user_id']).aggregate(total_cals=Sum('meal__food_calories')),
                'exer_cals': Exercise.objects.filter(date_done=now, exerciser=request.session['user_id']).aggregate(total_cals=Sum('exer_calories')),
            }
        return render(request, 'profile.html', context)
    return redirect('/')

def add_weight(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        Weight.objects.create(
            weigh_in= request.POST["weight"],
            weigher= user,
        )
    return redirect('/dashboard')

def edit_food(request, meal_id):
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            context= {
                "user": user[0],
                "meals": Meal.objects.get(id=meal_id)
            }
    return render(request, 'update.html', context)

def update_food(request, meal_id):
    context= {
        "meals": Meal.objects.get(id=meal_id)
    }
    if request.method=="POST":
        newedit = Meal.objects.get(id=meal_id)
        newedit.meal.food_name = request.POST["food_name"]
        newedit.meal.food_calories = request.POST["calories"]
        newedit.meal.fat= request.POST["fat"]
        newedit.meal.carbs = request.POST["carbs"]
        newedit.meal.protein = request.POST["protein"]
        newedit.meal_tag= request.POST["meal_tag"]
        newedit.save()
    return redirect('/dashboard')

def read_blogs(request):
    if 'user_id' in request.session:
        user= User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                "blogs": Blog.objects.all()
            }
            return render(request, 'blogs.html', context)
    if request.method =="GET":
        return render (request, 'login.html')
    return redirect('/login')

def create_blog(request):
    if request.method == "POST":
        Blog.objects.create(
            title = request.POST['title'],
            author = request.POST['author'],
            content= request.POST['content'],
        )
    
    return redirect('/blogs')


def add_message(request):
    pass

def add_comment(request):
    pass

def prev_date(request):
    pass

def next_date(request):
    pass

