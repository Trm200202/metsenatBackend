from rest_framework import serializers
from django.db.models import Sum
from . import models

class SponsorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sponsor
        fields = (
            "full_name",
            "phone_number",
            "organization_name",
            "amount",
            "type",
        )

        extra_kwargs = {
            "id" : {
                "read_only": True
            }
        }

    def validate(self, attrs):
        types = attrs.get("type")
        org_name = attrs.get("organization_name")
        if types=="physical" and org_name:
            raise serializers.ValidationError(
                detail={"error": "Jismoniy shaxs tashkilot nomiga ega emas"})
        if types=="legal" and not org_name:
            raise serializers.ValidationError(
                detail={"error": "Tashkilot nomi kiritilishi shart"})
            
        return attrs

class SponsorListSerializer(serializers.ModelSerializer):
    sponsor_amount = serializers.SerializerMethodField()

    def get_sponsor_amount(self, obj):
        a = obj.student_sponsors.aggregate(Sum("amount"))
        return a["amount__sum"] if a["amount__sum"] else 0


    class Meta:
        model = models.Sponsor
        fields = (
            "id",
            "full_name",
            "phone_number",
            "amount",
            "created_at",
            "status",
            "sponsor_amount"
        )


class SponsorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sponsor
        fields = "__all__"


    


class SponsorStudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSponsor
        fields = "__all__"

    def create(self, validated_data):
        amount = validated_data.get("amount")
        student = validated_data.get("student")
        sponsor = validated_data.get("sponsor")

        # talabaga ajratiladigan pul miqdori oshib ketmasligi kk

        total_amount=sum(models.StudentSponsor.objects.filter(student=student).values_list("amount", flat=True))
        if total_amount + amount > student.contract:
            raise serializers.ValidationError(
                detail={"error": f"Siz bu talabaga {student.contract-total_amount} dan ko'p pul o'tkazolmaysiz"
                        }
                                                )

        if amount>sponsor.amount:
            raise serializers.ValidationError(
                detail={"error": f"Sizning hisobingizda faqat {sponsor.amount} pul qolgan"
                        }
                                                )



        return super().create(validated_data)
    

class StudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Student
        fields = "__all__"

    extra_kwargs = {
            "id" : {
                "read_only": True
            }
        }


class StudentListSerializer(serializers.ModelSerializer):
    student_amount = serializers.SerializerMethodField(method_name="total_student_amount")

    def total_student_amount(self, obj):
        result = sum(models.StudentSponsor.objects.filter(student=obj).values_list("amount", flat=True))
        return result
    

    class Meta:
        model = models.Student
        fields = (
            "id",
            "full_name",
            "contract",
            "degree",
            "university",
            "student_amount"
        )
class StudentDetailSerializer(serializers.ModelSerializer):
    student_amounts = serializers.SerializerMethodField(method_name="total_student_amount")

    def total_student_amount(self, obj):
        r = sum(models.StudentSponsor.objects.filter(student=obj).values_list("amount", flat=True))
        return r

    class Meta:
        model = models.Student
        fields = (
            "full_name",
            "contract",
            "degree",
            "university",
            "student_amounts",
        )

# class StudentSponsorUpdateSerializer(serializers.ModelSerializer):
    # student_sponsor_phone_number = serializers.SerializerMethodField(method_name="phone_number")

    # def phone_number(self, obj):
    #     re = models.StudentSponsor.objects.filter(student=obj).values("phone_number", flat=True)
    #     return re

    # class Meta:
    #     model = models.Student
    #     fields = (
    #         "full_name",
    #         "contract",
    #         "university",
    #         "student_sponsor_phone_number"
    #     )

class StudentSponsorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSponsor
        fields = (
            "sponsor",
            "amount"
        )


class StudentSponsorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sponsor
        fields = (
            "full_name",
            "phone_number"
        )
        modell = models.Student
        fields = (
            "university",
            "contract"
        )


class StudentSponsorDeleteORCreateSerializer(serializers.ModelSerializer):
    


    class Meta:
        model = models.StudentSponsor
        fields = (
            "sponsor",
            "student",
            "amount",
        )