from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('student1/',views.studentsApi1), # static data 
    path('student2/',views.studentsApi2), # Manual Serialization 
    path('student3/',views.studentsApi3), # Using rest Serializer -> Function basedviews get Student data
    path('student4/',views.studentsApi4), # get and post data in database
    path('student/<int:pk>',views.studentDetailsview), # To view specific student data 
    path('student-update/<int:pk>',views.student_Data_update), # we can update date delete date of specific student 
    
    ### Employees class based view 
    
    path('employees/',views.Employee.as_view()),
    
    # CRUD in employees using class based viws
    path('employees/<int:pk>',views.Employee_details.as_view()),
    
    # Handling API Using Mixins 
    path('employees_mixins/',views.Employees_mixins.as_view()),
    
    # Handling primary key based operations using mixins
    path('employees_mixins_pk/<int:pk>',views.Employees_mixins_pk.as_view())
    
    
    
]   