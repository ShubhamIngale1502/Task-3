from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .serializer import StudSerializer 
from authapp.serializer import User
from rest_framework.response import Response
from .models import Student
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from .utils import EmailThread
from django.conf import settings


loggers = logging.getLogger('mylogger')


@api_view(http_method_names=(['GET', 'POST']))
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def studentView(request, format = None):
    if request.method == 'POST':
        try:
            serializer = StudSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info('Student Created SuccesFylly')
            user_email = request.user.email
            subject = 'Registration Successful'
            message = 'User Created Succesfully'
            if user_email:
                EmailThread(
                    subject =subject,
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details:Email Send SuccesFully'})
            return Response(data=serializer.data, status=201)
        except:
            loggers.error("Error in Creating the Student")
            return Response(data=serializer.errors, status=404)
        
    if request.method=='GET':
        try:
            obj = Student.objects.all()
            serializer = StudSerializer(obj, many=True)
            loggers.info('Student Data Featched SuccesFylly')
            return Response(data=serializer.data, status=200)
        except:
            loggers.error(data=serializer.errors, status = 404)
            
@api_view(http_method_names=(['GET','PUT','PATCH','DELTE']))
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def details_api(request, pk):
    obj = get_object_or_404(Student,pk=pk)
    if request.method == 'GET':
        try:
            serializer = StudSerializer(obj)
            loggers.info('Student Featched Successfully')
            return Response(data=serializer.data,status=200)
        except:
            loggers.error('Failed to retrieve data')
            return Response(data={'details:Data Not Found'}, status=404)
        
    if request.method == 'PUT':
        try:
            serializer =StudSerializer(data=request.data, instance =obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info("Data Updated!!")
            user_email = request.user.email
            subject = 'Project Email'
            message = 'User Created Succesfully'
            if user_email:
                EmailThread(
                    subject =subject,
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details:Email Send SuccesFully'})
            return Response(data=serializer.data, status=205)
        except:
            loggers.error("Updation Failed!!!")
            return Response(data=serializer.errors, status=404)
    
    if request.method == 'PATCH':
        try:
            serializer =StudSerializer(data=request.data, instance =obj, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            loggers.info("Data Updated!!")
            return Response(data=serializer.data, status=205)
        except:
            loggers.error("Updation Failed!!!")
            return Response(data=serializer.errors, status=400)    
    
    if request.method == 'DELETE':
        try:
            obj.delete()
            loggers.info("Deleted Sucessfully")
            user_email = request.user.email
            subject = 'Project Email'
            message = 'User Created Succesfully'
            if user_email:
                EmailThread(
                    subject =subject,
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()
                return Response(data={'details:Email Send SuccesFully'})
            return Response(data="Delete Successful", status=210)
        except:
            loggers.error("Delete failed")
            return Response(data='Error in Delete',status=406)
        
        