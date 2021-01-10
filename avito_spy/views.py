from django.shortcuts import render

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from avito_spy.models import Target
from avito_spy.serializers import TargetSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@method_decorator(csrf_exempt, name="dispatch")
class TargetView(viewsets.ModelViewSet):
    queryset = Target.objects.all().order_by("title")
    serializer_class = TargetSerializer


"""   def post(self, request):
        serializer = TargetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
