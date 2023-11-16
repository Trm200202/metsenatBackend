from django.shortcuts import render
from .models import *
from django.db.models import Sum
# Create your views here.
from . import serializers
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Response


class SponsorCreateAPIView(CreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorCreateSerializer

class SponsorListAPIView(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorListSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend, ]
    search_fields = ("full_name", )
    filterset_fields = ("created_at", "status", "amount", )

class SponsorDetailAPIView(RetrieveAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorCreateSerializer

class SponsorUpdateAPIView(UpdateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorUpdateSerializer

class SponsorStudentCreateAPIView(CreateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = serializers.SponsorStudentCreateSerializer

class StudentCreateAPIView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentCreateSerializer

class StudentListAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentListSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend, ]
    search_fields = ("full_name", )
    filterset_fields = ("degree", "university", )



class DashboardStatisticAPIView(APIView):

    def get(self, request):
        
        total_paid_money = StudentSponsor.objects.aggregate(Sum("amount"))["amount__sum"]
        


        total_contract = Student.objects.aggregate(Sum("contract"))["contract__sum"]



        return Response({
            "total_paid_money":total_paid_money,



            "total_contract":total_contract,
            "total_left_money": total_contract - total_paid_money
        })
    
class StudentDetailAPIView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentDetailSerializer

class StudentSponsorAPIView(ListAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorListSerializer

class StudentSponsorUpdateAPIView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentUpdateSerializer

class StudentSponsorCreateAPIView(CreateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorCreateSerializer


class StudentSponsorDeleteAPIView(DestroyAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorDeleteORCreateSerializer


class GraphicAPIView( APIView):
    
    def get(self, request):
        from datetime import date, timedelta
        import calendar

        this_year = date.today().year

        start_date = date(this_year, 1, 1)

        end_date = date(this_year, 12, 31)


        result = []

        while start_date<end_date:
            this_month = start_date.month
            this_year  = start_date.year
            num_days = calendar.monthrange(this_year, this_month)[1]
            queryset = Sponsor.objects.filter(created_at__range = (start_date, 
                                                                          date(this_year,
                                                                                this_month,
                                                                                 num_days))).count()
            
            
            result.append({
                "month": start_date.strftime("%B"),
                "sponsor_count": queryset,
            })

            start_date += timedelta(days=num_days)

        return Response(result)
    

        