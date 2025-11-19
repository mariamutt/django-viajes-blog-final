from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User

@login_required
def profile_detail(request, username=None):
    # Si no se pasa username, muestra el propio
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user
        
    return render(request, 'profiles/profile_detail.html', {'target_user': user_obj})

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('profiles:detail_own')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'profiles/profile_form.html', context)