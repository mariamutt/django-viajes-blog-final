from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm

@login_required
def inbox_list(request):
    # Lógica para agrupar conversaciones (último mensaje de cada par)
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    
    conversations = {}
    for msg in messages:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        if other_user not in conversations:
            conversations[other_user] = msg
            
    return render(request, 'inbox/inbox_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, username):
    other_user = get_object_or_404(User, username=username)
    messages_list = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    # Marcar como leídos
    messages_list.filter(receiver=request.user).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('inbox:detail', username=username)
    else:
        form = MessageForm()

    return render(request, 'inbox/detail.html', {
        'other_user': other_user,
        'messages': messages_list,
        'form': form
    })

@login_required
def new_message(request):
    if request.method == 'POST':
        username = request.POST.get('to_user')
        try:
            user = User.objects.get(username=username)
            return redirect('inbox:detail', username=username)
        except User.DoesNotExist:
            pass # Manejar error
    return render(request, 'inbox/new.html')