from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import date, timedelta
from .models import client, workoutplan, progress_tracker

# ------------------ HOME ------------------
def home(request):
    return render(request, 'home.html')


# ------------------ STATIC WORKOUT PLANS ------------------
PLANS = [
    {
        "id": 1,
        "plan_name": "Fat Burn Express",
        "plan_description": "High-intensity workouts for rapid fat loss.",
        "weekly_breakdown": ["Day 1: Cardio HIIT", "Day 2: Strength Training", "Day 3: Core + Yoga",
                             "Day 4: Rest", "Day 5: Full Body HIIT", "Day 6: Cardio Endurance", "Day 7: Stretching"],
        "goals": "Lose fat and improve stamina."
    },
    {
        "id": 2,
        "plan_name": "Lean Muscle Builder",
        "plan_description": "Strength training to build lean muscle mass.",
        "weekly_breakdown": ["Day 1: Upper Body Strength", "Day 2: Lower Body Strength", "Day 3: Core & Cardio",
                             "Day 4: Rest", "Day 5: Push Day", "Day 6: Pull Day", "Day 7: Active Recovery"],
        "goals": "Gain lean muscle and tone your body."
    },
    {
        "id": 3,
        "plan_name": "Endurance Booster",
        "plan_description": "Cardio-focused plan to build endurance.",
        "weekly_breakdown": ["Day 1: Long Run", "Day 2: Cycling", "Day 3: Core + Mobility",
                             "Day 4: Rest", "Day 5: HIIT", "Day 6: Swimming", "Day 7: Stretch & Recovery"],
        "goals": "Improve stamina and cardiovascular health."
    },
    {
        "id": 4,
        "plan_name": "Full Body Strength",
        "plan_description": "Balanced full-body training for strength.",
        "weekly_breakdown": ["Day 1: Upper Body", "Day 2: Lower Body", "Day 3: Cardio",
                             "Day 4: Rest", "Day 5: Full Body Strength", "Day 6: Core & Balance", "Day 7: Recovery"],
        "goals": "Develop strength across all muscle groups."
    },
    {
        "id": 5,
        "plan_name": "Core & Abs Shred",
        "plan_description": "Intense core-focused workouts.",
        "weekly_breakdown": ["Day 1: Core Blast", "Day 2: Cardio + Core", "Day 3: Pilates",
                             "Day 4: Rest", "Day 5: Core Strength", "Day 6: HIIT + Core", "Day 7: Yoga"],
        "goals": "Strengthen core muscles and define abs."
    },
    {
        "id": 6,
        "plan_name": "Yoga & Flexibility",
        "plan_description": "Gentle yoga plan for flexibility & balance.",
        "weekly_breakdown": ["Day 1: Hatha Yoga", "Day 2: Vinyasa Flow", "Day 3: Meditation",
                             "Day 4: Rest", "Day 5: Power Yoga", "Day 6: Balance Training", "Day 7: Deep Stretch"],
        "goals": "Improve flexibility and reduce stress."
    },
    {
        "id": 7,
        "plan_name": "Athletic Performance",
        "plan_description": "Sports-based training for athletes.",
        "weekly_breakdown": ["Day 1: Speed Drills", "Day 2: Strength Training", "Day 3: Agility Work",
                             "Day 4: Rest", "Day 5: Explosive Power", "Day 6: Endurance Runs", "Day 7: Recovery"],
        "goals": "Enhance athletic performance and agility."
    },
    {
        "id": 8,
        "plan_name": "Weight Gain Bulk",
        "plan_description": "Calorie surplus training for weight gain.",
        "weekly_breakdown": ["Day 1: Upper Body Strength", "Day 2: Lower Body Strength", "Day 3: Full Body",
                             "Day 4: Rest", "Day 5: Push Day", "Day 6: Pull Day", "Day 7: Recovery & Nutrition"],
        "goals": "Gain weight and build muscle mass."
    },
]

def plan_list(request):
    """Show all static workout plans as cards."""
    return render(request, 'plans/list.html', {'plans': PLANS})

def assign_plan(request, plan_id):
    """Assign a selected plan to a client."""
    selected_plan = next((p for p in PLANS if p["id"] == plan_id), None)
    if not selected_plan:
        messages.error(request, "Invalid plan selected.")
        return redirect('plan_list')

    clients = client.objects.all()

    if request.method == "POST":
        client_id = request.POST.get("client")
        selected_client = get_object_or_404(client, id=client_id)

        workoutplan.objects.create(
            client=selected_client,
            plan_name=selected_plan["plan_name"],
            plan_description=selected_plan["plan_description"],
            duration_weeks=4,  # Default
            goals=selected_plan["goals"]
        )
        messages.success(request, f"Plan '{selected_plan['plan_name']}' assigned to {selected_client.name}!")
        return redirect('client_list')

    return render(request, "plans/assign.html", {"plan": selected_plan, "clients": clients})


# ------------------ CLIENT CRUD WITH PLAN STATUS ------------------
def client_list(request):
    """List all clients with their plan status."""
    clients_data = []
    today = date.today()
    for c in client.objects.all():
        plan = workoutplan.objects.filter(client=c).order_by('-id').first()
        status, expiry_date, days_left = "No Plan", None, None
        if plan and c.joining_date:
            expiry_date = c.joining_date + timedelta(weeks=plan.duration_weeks)
            if expiry_date >= today:
                status = "Active"
                days_left = (expiry_date - today).days
            else:
                status = "Expired"
                days_left = 0
        clients_data.append({
            'client': c,
            'plan': plan,
            'status': status,
            'expiry_date': expiry_date,
            'days_left': days_left
        })
    return render(request, 'clients/list.html', {'clients_data': clients_data})

def add_client(request):
    if request.method == 'POST':
        joining_date = request.POST.get('joining_date') or None
        client.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            joining_date=joining_date
        )
        messages.success(request, 'Client added successfully!')
        return redirect('client_list')
    return render(request, 'clients/add.html')

def edit_client(request, id):
    c = get_object_or_404(client, id=id)
    if request.method == 'POST':
        for field in ['name', 'email', 'phone', 'address', 'age', 'gender']:
            setattr(c, field, request.POST.get(field, getattr(c, field)))
        # Handle joining_date separately (skip if empty)
        joining_date = request.POST.get('joining_date')
        if joining_date:
            c.joining_date = joining_date
        c.save()
        messages.success(request, 'Client updated successfully!')
        return redirect('client_list')
    return render(request, 'clients/edit.html', {'client': c})

def delete_client(request, id):
    get_object_or_404(client, id=id).delete()
    messages.success(request, 'Client deleted!')
    return redirect('client_list')


# ------------------ PROGRESS TRACKER CRUD ------------------
def progress_list(request):
    progress = progress_tracker.objects.select_related('client').all()
    return render(request, 'progress/list.html', {'progress': progress})

def add_progress(request):
    clients = client.objects.all()
    if request.method == 'POST':
        progress_tracker.objects.create(
            client_id=request.POST['client'],
            date=request.POST['date'],
            weight=request.POST['weight'],
            bmi=request.POST['bmi'],
            notes=request.POST['notes']
        )
        messages.success(request, 'Progress entry added!')
        return redirect('progress_list')
    return render(request, 'progress/add.html', {'clients': clients})

def edit_progress(request, id):
    progress = get_object_or_404(progress_tracker, id=id)
    clients = client.objects.all()
    if request.method == 'POST':
        for field in ['date', 'weight', 'bmi', 'notes']:
            setattr(progress, field, request.POST.get(field, getattr(progress, field)))
        progress.client_id = request.POST['client']
        progress.save()
        messages.success(request, 'Progress updated!')
        return redirect('progress_list')
    return render(request, 'progress/edit.html', {'progress': progress, 'clients': clients})

def delete_progress(request, id):
    get_object_or_404(progress_tracker, id=id).delete()
    messages.success(request, 'Progress deleted!')
    return redirect('progress_list')
