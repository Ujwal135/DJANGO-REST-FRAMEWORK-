from student.models import Student
from rest_framework import serializers
from Employees.models import Employees
from Blog.models import Blog,Comment

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
        
class EmployeesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = "__all__"



        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many = True , read_only = True)
    class Meta:
        model = Blog
        fields = "__all__"