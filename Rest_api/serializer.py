from student.models import Student
from rest_framework import serializers
from Employees.models import Employees


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
        
class EmployeesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = "__all__"

