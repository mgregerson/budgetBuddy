from django.shortcuts import  render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register_request(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('profile')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = CustomUserCreationForm()
	return render (request=request, template_name="auth/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        print('METHOD IS POST')
        if form.is_valid():
            print('FORM IS VALID')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'auth/profile.html', context)

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")