import logging

from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from api.models import Employee,Companyinfo
from api.serializers import EmployeeSerializer

logger = logging.getLogger(__name__)

def setcookie(request):
    response = HttpResponse("Cookie Set")
    response.set_cookie('firstname', 'praveen')
    return response
def getcookie(request):
    value  = request.COOKIES['firstname']
    return HttpResponse("firstname is : "+ value)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def employee_list(request):
    if request.method == 'GET':
        print(request)
        logger.debug("inside get method")
        employee = Employee.objects.all()
        firstname = request.GET.get('firstname',None)
        print(firstname)
        companyname = request.GET.get('companyname',None)
        if firstname is not None:
            logger.debug("firstname is {}".format(firstname))
            employee = employee.filter(firstname=firstname)
        else:
            if companyname is not None:
                company = Companyinfo.objects.filter(companyname=companyname)[0]
                employee = Employee.objects.filter(company=company).count()
                return HttpResponse(employee)

        employee_serializer = EmployeeSerializer(employee, many=True)
        return JsonResponse(employee_serializer.data, safe=False)


    elif request.method == 'POST':
        logger.debug("inside post method")
        employee_data = JSONParser().parse(request)
        employee_serializer = EmployeeSerializer(data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse({"message": "valid"})
        else:
            return JsonResponse({ "message":"not valid"})

    elif request.method == 'DELETE':
        logger.debug("inside delete method")
        firstname = request.GET.get('firstname', None)
        employee = Employee.objects.filter(firstname=firstname)
        if firstname is not None:
            employee.delete()
            return JsonResponse({"message":"deleted successfully"})
        else:
            return JsonResponse({"message":"deletion not successful"})

    elif request.method == 'PUT':
        logger.debug("inside put method")
        employee_data = JSONParser().parse(request)
        firstname = employee_data.get("firstname")
        if firstname is not None:
            employee = Employee.objects.filter(firstname=firstname)
            employee.update(**employee_data)
            return JsonResponse({"message":"updated successful"})
        else:
            return JsonResponse({"message":"update failed"})

#    try:
#        employee = TEmployee.objects.get(id=10)
#    except TEmployee.DoesNotExist:
#        return HttpResponse("EXCEPTION")