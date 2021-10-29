from django.shortcuts import render,redirect
from .forms import MessageForm
from .models import Message
# Create your views here.
from datetime import timedelta
from django.utils import timezone

def index(request):
    form = MessageForm(request.POST or None)

    msg = None
    date = None
    if request.method == "POST":

        if form.is_valid():
            note = form.save()
            msg = note.hash_key
            form = MessageForm()
            date = note.time_created + timedelta(days=note.destroy_days, hours=note.destroy_hours)

    return render(request, 'index.html', {'form':form,'msg':msg,'date':date})


def view_message(request, hash_key):
    msg = ''
    try:
        message = Message.objects.get(hash_key=hash_key)
        if message.viewed:
            date = message.time_viewed
            return render(request,'viewed.html',{'date':date,'hash_key':hash_key})

            pass
        elif message.time_created + timedelta(days=message.destroy_days, hours=message.destroy_hours) < timezone.now():
            expiry_date = message.time_created + timedelta(days=message.destroy_days, hours=message.destroy_hours)
            return render(request,'expired.html',{'expiry_date':expiry_date,'hash_key':hash_key})
        else:
            if message.hidden:
                return render(request,'hidden.html',{'hash_key':hash_key})
            else:
                msg = message.message
                message.viewed=True
                message.message=''
                message.time_viewed=timezone.now()
                message.save()
                return render(request, 'message.html', {'msg': msg})

    except Message.DoesNotExist:
        return render(request,'not_exist.html',{'hash_key':hash_key})


def hidden_message(request,hash_key):
    msg = ''
    try:
        message = Message.objects.get(hash_key=hash_key)
        msg = message.message
        if message.hidden:
            message.hidden=False
            message.save()
        return redirect('view_message', hash_key)
    except Message.DoesNotExist:
        print("invalid")

