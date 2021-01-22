from django.shortcuts import render
from django import db
from .forms import TargetForm
from .models import Target, Ad
from .module import AvitoGetTarget


def main_page(request):
    targets = Target.objects.all()
    return render(request, "ads_checker/main_page.html", {"targets": targets})


def poll(request, target_id):       # "POST /1/poll HTTP/1.1" 500 73278
    target = Target.objects.get(id=target_id)   # return [1 object]
    ads = AvitoGetTarget(target).get_info()
    target.active_ads = len(ads[0])
    target.average_price = ads[1]
    target.price_difference = ads[2]
    target.dynamic = ads[3]
    target.save()
    for ad in ads[0]:
        if not Ad.objects.filter(link=ad[1]):
            target_ad = Ad(target=target, title=ad[0], link=ad[1], price=ad[2])    # if item not in db
            target_ad.save()
            db.connections.close_all()
    return main_page(request)


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
    context = {"target": target, "ads": ads}
    return render(request, "ads_checker/view_target.html", context)


def delete_target(request, target_id):
    target = Target.objects.filter(pk=target_id)
    target.delete()
    return main_page(request)
