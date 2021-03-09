from rest_framework import serializers
from api.models import Employee,Companyinfo


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id',
                  'firstname',
                  'lastname','company')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companyinfo
        fields = ('id',
                  'companyname',
                  'description')

