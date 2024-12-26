from django.shortcuts import render, redirect
from .models import Student, Company, UserPreference, Guide,PreferenceTimeframe,Faculty
from django.forms import modelform_factory
from django.utils import timezone
import datetime  # Correct import
from .forms import PreferenceForm


# views.py
from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta





def home_view(request):
    return render(request, 'home.html')


from django.utils import timezone




from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def student_id_view(request):
    timeframe = PreferenceTimeframe.objects.first()  # Fetch your actual timeframe object

    time_left = None
    if timeframe:
        now = timezone.now()
        if now < timeframe.end_time:
            time_left = (timeframe.end_time - now).total_seconds()  # Get time left in seconds

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        if roll_number:
            request.session['roll_number'] = roll_number
            # Call the check function and handle its response
            check_response = check(request)  # Pass the request to check
            if check_response:
                return check_response  # Return check's response (render/redirect)

    return render(request, 'student_id.html', {'time_left': time_left})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def check(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        if roll_number:
            if Company.objects.filter(rollno=roll_number).exists():
                return render(request, 'not_eligible.html')  # Show "Not eligible" message
            elif UserPreference.objects.filter(rollno=roll_number).exists():
                return redirect('preference')  # Redirect to preferences page
            # Continue to industrial_experience if eligible
            return redirect('industrial_experience')
    return render(request) # Return None if no action is taken

from django.utils.timezone import make_aware, now, localtime





from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.timezone import make_aware, localtime, now
from .models import PreferenceTimeframe, UserPreference, Student

def industrial_experience_view(request):
    # Fetch the preference timeframe
    timeframe = PreferenceTimeframe.objects.first()  

    if timeframe:
        # Ensure start_time, end_time, and allotment_time are timezone-aware
        if timezone.is_naive(timeframe.start_time):
            timeframe.start_time = make_aware(timeframe.start_time)
        if timezone.is_naive(timeframe.end_time):
            timeframe.end_time = make_aware(timeframe.end_time)
        if timezone.is_naive(timeframe.allotment_time):
            timeframe.allotment_time = make_aware(timeframe.allotment_time)

        current_time = localtime(now())
        
        # Check if the current time is before the start time
        if current_time < timeframe.start_time:
            return render(request, 'not_started.html', {'start_time': timeframe.start_time})
        
        # Check if the current time is after the allotment time (guide allotted)
        if current_time >= timeframe.allotment_time:
            return render(request, 'allotted_guide.html', {'guide': 'Guide details here'})
        
        # Check if the current time is after the end time (process ended)
        if current_time > timeframe.end_time:
            return render(request, 'ended.html', {'end_time': timeframe.end_time})

    # Automatically redirect based on user selection (no need for submit button)
    if request.method == 'POST':
        experience = request.POST.get('experience')
        roll_number = request.session.get('roll_number')

        # Fetch the student from the database
        try:
            student = Student.objects.get(roll_number=roll_number)
        except Student.DoesNotExist:
            return render(request, 'student_not_found.html', {
                'message': f'Student with roll number {roll_number} does not exist.'
            })

        # Check if the roll number already exists in the UserPreference table
        if UserPreference.objects.filter(rollno=student).exists():
            return render(request, 'already_submitted.html', {
                'message': 'You have already submitted your preference list. Would you like to edit it?'
            })

        if experience == 'yes':
            # Redirect to the company details page where user can enter details
            return redirect('company_details')
        elif experience == 'no':
            # Redirect to the preferences page
            return redirect('preference')

    return render(request, 'industrial_experience.html')



def company_details_view(request):
    message = None
    if request.method == 'POST':
        roll_number = request.session.get('roll_number')
        student = Student.objects.get(roll_number=roll_number)
        company_name = request.POST.get('company_name')
        company_role = request.POST.get('company_role')
        years_of_experience = request.POST.get('years_of_experience')
        

        # Create company entry for the student
        Company.objects.create(
            rollno=student, 
            company_name=company_name,
            company_role=company_role,
            years_of_experience=years_of_experience
        )

        # After submission, show the "Not eligible" message
    
        message = 'You are not eligible for further process.'

    return render(request, 'company_details.html', {
        'message': message
    })





def edit_preference_view(request):
    roll_number = request.session.get('roll_number')

    # Check if roll_number is available in the session
    if not roll_number:
        # If roll number is not in session, redirect to the student ID page
        return redirect('home')

    try:
        # Try to retrieve the student from the database
        student = Student.objects.get(roll_number=roll_number)
    except Student.DoesNotExist:
        # If the student is not found, show an error or redirect
        return render(request, 'student_not_found.html', {
            'message': f'Student with roll number {roll_number} does not exist.'
        })

    # Check if the student already has preferences in the UserPreference table
    try:
        user_pref = UserPreference.objects.get(rollno=student)
    except UserPreference.DoesNotExist:
        # If no preferences exist, redirect to the normal preference view
        return redirect('preference')  # 'preference' is the name of your original preference view

    # If preferences exist, allow the user to edit them
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            action = request.POST.get('action') 
            # Collect new preferences
            preferences = [
                form.cleaned_data[f'preference{i}']
                for i in range(1, Guide.objects.count() + 1)
                if form.cleaned_data.get(f'preference{i}')
            ]
            
            print(action)
            # Update the user's preferences
            user_pref.preferences = preferences
            if action == "submit":
                user_pref.is_final = False
            else:
                user_pref.is_final = True

            user_pref.save()

            return redirect('successpage')  # Redirect to success page after saving
    else:
        # Prepopulate the form with the existing preferences
        initial_data = {
            f'preference{i}': pref for i, pref in enumerate(user_pref.preferences, 1)
        }
        form = PreferenceForm(initial=initial_data)

    return render(request, 'preferences.html', {'form': form})





def preference_view(request):
    roll_number = request.session.get('roll_number')
    
    if not roll_number:
        return redirect('home')

    try:
        student = Student.objects.get(roll_number=roll_number)
    except Student.DoesNotExist:
        return render(request, 'student_not_found.html', {
            'message': f'Student with roll number {roll_number} does not exist.'
        })
    if Company.objects.filter(rollno=student).exists():
        return render(request, 'not_eligible.html', {
            'message': 'You are not eligible to fill preferences because you have industrial experience.'
        })
    
    if UserPreference.objects.filter(rollno=student).exists():
        x=UserPreference.objects.get(rollno=student)
        if x.is_final==False:
            return redirect('successpage')
        
        if request.method == 'POST':
            if 'edit' in request.POST:
                return redirect('edit_preference')
            else:
                return redirect('home')
        return render(request, 'edit_prompt.html')

    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            action = request.POST.get('action')
            
            preferences = [
                form.cleaned_data[f'preference{i}']
                for i in range(1, Guide.objects.count() + 1)
                if form.cleaned_data.get(f'preference{i}')
            ]

            user_pref = UserPreference(rollno=student)
            user_pref.preferences = preferences
            print(action)
            if action == "Submit":
                user_pref.is_final = False
            else:
                user_pref.is_final = True

            user_pref.save()
            return redirect('successpage')
    else:
        form = PreferenceForm()

    return render(request, 'preferences.html', {'form': form})








def successpage(request):
    return render(request, 'success_page.html')







