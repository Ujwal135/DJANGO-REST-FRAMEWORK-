from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,JsonResponse
from student.models import Student
from .serializer import StudentSerializers,EmployeesSerializers
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
from Employees.models import Employees
from rest_framework.views import APIView
from rest_framework import mixins ,generics,viewsets
from django.http import Http404




# Static api response

def studentsApi1(request):
    
    student = {
        'id':1,
        'name':'Ujjwal',
        'class': 'Backend-dev'
    }
    
    return JsonResponse(student)


# FATCHING DATA FROM DATABASE using MANUAL serialization 

 
def studentsApi2(request):
    
    student = Student.objects.all() # extracting all data from database 
    
    students_list = list(student.values())  # Converting it into a list becouse its not readable 
    
    return JsonResponse(students_list,safe=False)
    

# Fatching data using Function based views from serializer.py 

@api_view(['GET'])
def studentsApi3(request):
    if request.method == 'GET':
        
        student = Student.objects.all()  
        
        serializer = StudentSerializers(student,many = True) 
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Storeing data using POST using fucnction based views

@api_view(['GET','POST'])
def studentsApi4(request):
    if request.method == 'GET':
        
        student = Student.objects.all()
        
        serializer = StudentSerializers(student,many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        
        serializer = StudentSerializers(data = request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    


## Geting specific student data using primary key

@api_view(['GET'])
def studentDetailsview(request,pk):
    
    try:
        student = Student.objects.get(pk=pk)
        
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        serializer = StudentSerializers(student)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
## Upadating spesific user using primary key and update it in database

@api_view(["GET","PUT","DELETE"])    
def student_Data_update(request,pk):
    
    try:
        student = Student.objects.get(pk=pk)
        
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        
        serializer = StudentSerializers(student)
        
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        
        serializer = StudentSerializers(student ,data = request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
        
    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    
    
##########################################################################################################################################
## Class Based Serialzers 
##########################################################################################################################################


class Employee(APIView):
    def get(self,request):
        employe = Employees.objects.all()
        serializer = EmployeesSerializers(employe,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = EmployeesSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
##########################################################################################################################################
## Class Based Serialzers                                 ################ CRUD ##################
##########################################################################################################################################

class Employee_details(APIView):
    def get_object(self,pk):
        
        try:
            return Employees.objects.get(pk = pk)
        
        except Employees.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        
        employee = self.get_object(pk)
        
        serializer = EmployeesSerializers(employee)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
    def post(self,request,pk):
        
        employee = self.get_object(pk)
        
        serializer = EmployeesSerializers(data = request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def put(self,request,pk):
        
        employee = self.get_object(pk)
        
        serializer = EmployeesSerializers(employee,data = request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

##########################################################################################################################################
## Class Based Serialzers using MIXINS            (for all )                   ################ CRUD ##################
##########################################################################################################################################


class Employees_mixins(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializers
    
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    
    
       

##########################################################################################################################################
## Class Based Serialzers using MIXINS primary key based (indivisual)                       ################ CRUD ##################
##########################################################################################################################################

    
class Employees_mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin ,generics.GenericAPIView):
    
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializers
    
    def get(self,request,pk):
        return self.retrieve(request,pk)     # Retrieve
     
    def put(self,request,pk):
        return self.update(request,pk)       # Update
    
    def delete(self,request,pk):
        return self.destroy(request,pk)      # Distroy 
    
    
##########################################################################################################################################
## Class Based Serialzers using Genrics                       ################ CRUD ##################
##########################################################################################################################################

    
class Employees_genrics(generics.ListAPIView  ,  generics.CreateAPIView):  # to view/list all employees & create/new employee 
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializers
    
    
##########################################################################################################################################
## Class Based Serialzers using Genrics primary key user specific   ################ CRUD ##################
##########################################################################################################################################
"""
class Employees_genrics_pk(generics.RetrieveAPIView,generics.UpdateAPIView,generics.CreateAPIView,generics.DestroyAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializers
    lookup_field = 'pk'
"""
    
class Employees_genrics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializers
    lookup_field = 'pk'
    

################################################################################################################
###################### ViewSet  ################################# ViewSet ######################################


class EmployeeViewSet(viewsets.ViewSet):
    
    def list(self,request):
        employee = Employees.objects.all()
        serializer = EmployeesSerializers(employee,many = True)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    
    def create(self,request):
        employee = Employees.objects.all()
        serializer = EmployeesSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    