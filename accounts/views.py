from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Students, User,Ideas
import json
## fatima code using rest framework to reate Projects api for  crud methode 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Projects 
from .serializers import ProjectsSerializer
from rest_framework import serializers, mixins, viewsets, generics
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

def send_email(request, email1 , email2):
    user1 = get_user_model().objects.get(email=email1)
    user2 = get_user_model().objects.get(email=email2)
    sender_name = user1.first_name
    sender_email = user1.email
    recipient_name = user2.first_name

    context = {
        'recipient_name': recipient_name,
        'sender_name': sender_name,
        'sender_email': sender_email,
    }
    email_content = render_to_string('invitation_email.html',context)
    try:
        send_mail('Team Joining Invitation', '', 'projectmanagerxcontact@gmail.com', [email2], html_message=email_content)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

## end fatima code 
@csrf_exempt
def get_students(request):
    if request.method == 'GET':
        user_ids = Students.objects.values_list('user_id', flat=True)
        my_data = User.objects.filter(id__in=user_ids)
        data_list = []
        for item in my_data:
            created_at_date = item.created_at.strftime('%Y-%m-%d')
            skillsarray = item.skills.split(",")
            data_dict = {
                'email': item.email,
                'username': item.username,
                'first_name': item.first_name,
                'last_name': item.last_name,
                'skills' : skillsarray,
                'created_at' : created_at_date,
            }
            data_list.append(data_dict)
        return JsonResponse(data_list, safe=False)

def get_projects_by_user(request, email):
    user = User.objects.get(email=email)
    projects = user.projects_created.all()
    #projects = Projects.objects.filter(created=user_id)
    serializer = ProjectsSerializer(projects,many=True)
    
    return JsonResponse(serializer.data,safe=False)

def get_user_profile(request, email):
    try:
        user = User.objects.get(email=email)
        skillsarray = user.skills.split(",")
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'skills' : skillsarray,
            'created_at' : user.created_at,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    
@api_view(['POST'])
def update_profile(request, email):
    user = User.objects.get(email=email)
    if request.method == 'POST':
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.skills = request.data.get('skills')
        user.username = request.data.get('username')
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

#############################################################################################  
# fatima code : rest framework for projecs models 
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_projects': '/',
        'Search by Category': '/?category=category_name',
        #'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


## the creat methode for object 
##############################################################

# @api_view(['POST'])
# def add_Project(request):
#     serializer = ProjectsSerializer(data=request.data)
    
#     if Projects.objects.filter(**request.data).exists():
#         raise serializers.ValidationError('This data already exists')
#     # TODO: create_by ==> id --> object_id , suprivased_by ==> object_id 
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
##############################################################
@api_view(['POST'])
def upload_image(request, project_id):
    project = Projects.objects.get(id=project_id)
    image = request.FILES.get('image')
    project = project(image=image)
    project.save()
    return Response({'message': 'Image uploaded successfully'})

from .serializers import ProjectsSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class ProjectUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ProjectsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class AddProject(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView,
                  mixins.UpdateModelMixin): 
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
    ## the add   methode for projects
    def post(self, request):
        serializer = ProjectsSerializer(data=request.data)
    
        # if Projects.objects.filter(**request.data).exists():
        #     raise serializers.ValidationError('This data already exists')
      
        if serializer.is_valid():
            project = serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    ## the update  methode for projects
    def put(self, request,project_id):
            project = Projects.objects.get(id=project_id)
            print(project)
            serializer = ProjectsSerializer(project,data=request.data)
        
            # if Projects.objects.filter(**request.data).exists():
            #     raise serializers.ValidationError('This data already exists')
        
            if serializer.is_valid():
                project = serializer.save()


                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



## the view / listing  methode for projects

   
@api_view(['GET'])
def view_Projects(request):
	
	
    projects = Projects.objects.all()
    serializer = ProjectsSerializer(projects,many=True)
    
    return JsonResponse(serializer.data,safe=False)


## the delete  methode for object
@api_view(['DELETE'])
def delete_project(request,project_id):
    try:
        project = Projects.objects.get(id=project_id)
    except Projects.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)








####### filter by category ###
class CategoryList(generics.ListAPIView):
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return Projects.objects.filter(category=self.kwargs['category'])
    
    
    
######## filter by multiple parameter ###


## or between multiple parameters version  ###


# class ProjectsViewSet(APIView):
#     def get(self, request):
        
#         category = request.GET.get('category')
#         year = request.GET.get('year')
#         used_techs = request.GET.get('used_techs')
        
#         query = Q(category=category, year=year)
#         if ',' in used_techs:
#             used_techs = used_techs.split(',')            
#             for search_string in used_techs:
#                 query |= Q(used_techs__contains=search_string)
#         else:
#             query |= Q(used_techs__contains=used_techs)
        
#         results = Projects.objects.filter(query)  
#         print(category, year,used_techs)
     
#         serializer = ProjectsSerializer(results,many=True)  
#         return JsonResponse(serializer.data,safe=False)
    


## and  between multiple parameters version  ###
class ProjectsViewSet(APIView):
    def get(self, request):
        category = request.GET.get('category')
        year = request.GET.get('year')
        used_techs = request.GET.get('used_techs')
        query = Q()
        if category:
            query &= Q(category=category)
        if year:
            query &= Q(year=year)
        if used_techs:
            if ',' in used_techs:
                used_techs = used_techs.split(',')
                for search_string in used_techs:
                    query &= Q(used_techs__contains=search_string)
            else:
                query &= Q(used_techs__contains=used_techs)

        results = Projects.objects.filter(query)
        print(category, year, used_techs)

        serializer = ProjectsSerializer(results, many=True)
        return JsonResponse(serializer.data, safe=False)

def get_user_first_name(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        first_name = user.first_name
        return JsonResponse({'first_name': first_name})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
@api_view(['POST'])
def create_idea(request):
    title = request.data.get('title')
    description = request.data.get('description')
    ideas = Ideas(title=title, description=description)
    ideas.save()

    return JsonResponse({'success': True})


def get_all_ideas(request):
    ideas = Ideas.objects.all()
    data = []
    for idea in ideas:
        created_at_date = idea.created_at.strftime('%Y-%m-%d')
        idea_data = {
            'title': idea.title,
            'created_at' : created_at_date,
            'description': idea.description,
        }
        data.append(idea_data)

    return JsonResponse(data, safe=False)