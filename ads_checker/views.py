from django.shortcuts import render, redirect
from django.urls import reverse
from django import db
from .forms import TargetForm, UpdateTargetForm
from .models import Target, Ad
from .module import AvitoGetTarget


def main_page(request):
    targets = Target.objects.all()
    # print("main_page")
    return render(request, "ads_checker/main_page.html", {"targets": targets})


def poll(request, target_id):       # "POST /1/poll HTTP/1.1" 500 73278
    target = Target.objects.filter(id=target_id)   # return 1 object
    ads = AvitoGetTarget(target[0]).get_info()
    for ad in ads:
        target_ad = Ad(target=target[0], title=ad[1], link=[0], price=ad[2])    # if item not in db
        target_ad.save()
        db.connections.close_all()
    return redirect(reverse("view_target", target_id))


def add_target(request):
    if request.method == "POST":
        form = TargetForm(request.POST)
        form.save()
    form = TargetForm()
    context = {"form": form}
    return render(request, "ads_checker/add_target.html", context)


def view_target(request, target_id):
    target = Target.objects.get(pk=target_id)
    ads = Ad.objects.filter(target_id=target_id)
    # print(ads)
    context = {"target": target, "ads": ads}
    return render(request, "ads_checker/view_target.html", context)

