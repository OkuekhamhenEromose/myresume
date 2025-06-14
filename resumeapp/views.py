from django.shortcuts import render, reverse
from .serializers import ResumeSerializer
from .models import Resume
from django.views import View
from rest_framework import status,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction


# from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
# import requests
from . serializers import *
from . models import *


class HomeView(View):
 def get(self, request):
  form = ResumeSerializer()
  candidates = Resume.objects.all()
  return render(request, 'myapp/home.html', { 'candidates':candidates, 'form':form})

 def post(self, request):
  form = ResumeSerializer(request.POST, request.FILES)
  if form.is_valid():
   form.save()
   return render(request, 'myapp/home.html', {'form':form})

class CandidateView(View):
 def get(self, request, pk):
  candidate = Resume.objects.get(pk=pk)
  return render(request, 'myapp/candidate.html', {'candidate':candidate})

class ResumeView(APIView):
    def get(self,request):
        try:
            listing = Resume.objects.all() 
            serializer = ResumeSerializer(listing,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # permission_classes=[permissions.IsAdminUser]
    def post(self,request):
        try:
            serializer = ResumeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResumeEditView(APIView):
    def get(self,request,pk):
        try:
            listing = get_object_or_404(Resume,pk=pk)
            serializer = ResumeSerializer(listing)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request,pk):
        try:
            listing = get_object_or_404(Resume,pk=pk)
            serializer = ResumeSerializer(listing,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request,pk):
        try:
            product = get_object_or_404(Resume,pk=pk)
            product.delete()
            return Response({"Message":"Listing deleted"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AddToResumeView(APIView):
    def get(self, request, id):
        try:
            resume = Resume.objects.get(pk=id)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data)
        except Resume.DoesNotExist:
            return Response(
                {'error': 'Resume not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    def post(self,request,id):
        try:
            # fet the product
            listing = get_object_or_404(Resume,id=id)
            # get the cart id
            userlisting_id = request.session.get('userlisting_id',None)
            
            with transaction.atomic():
                if userlisting_id:
                    userlisting = UserListing.objects.filter(id=userlisting_id).first()
                    if userlisting is None:
                        userlisting = UserListing.objects.create(total=0)
                        request.session['userlisting_id'] = userlisting.id
                    
                    this_listing = userlisting.singlelisting_set.filter(listing=listing)

                    # assigning cart to a user 
                    if request.user.is_authenticated and hasattr(request.user,'profile'):
                        userlisting.profile = request.user.profile
                        userlisting.save()

                    if this_listing.exists():
                        singlelisting = this_listing.last()
                        singlelisting.quantity +=1                    
                        singlelisting.save()
                        # update our cart
                        userlisting.save()
                        return Response({"Message":"Item increase in the resume"})
                    else:
                        singlelisting = SingleListing.objects.create(userlisting=userlisting,listing=listing,quantity=1)
                        singlelisting.save()
                        # update our cart
                        userlisting.save()
                        return Response({"Message":"A new Item added to cart"})

                else:
                    # create a cart
                    userlisting = UserListing.objects.create(total=0)
                    request.session['userlisting_id'] = userlisting.id
                    singlelisting = SingleListing.objects.create(userlisting=userlisting,listing=listing,quantity=1)
                    singlelisting.save()
                    # update our cart
                    userlisting.save()
                    return Response({"Message":"A new resume created"})

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyResumeView(APIView):
    def get(self,request):
        try:
            userlisting_id = request.session.get('userlisting_id', None)
            if userlisting_id:
                userlisting = get_object_or_404(UserListing,id=userlisting_id)
                # assigning cart to a user 
                if request.user.is_authenticated and hasattr(request.user,'profile'):
                    userlisting.profile = request.user.profile
                    userlisting.save()
                serializer = UserListingSerializer(userlisting)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error":"cart not found"},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ManageResumeView(APIView):
    def post(self,request,id):
        action = request.data.get('action')
        try:
            userlisting_obj = get_object_or_404(SingleListing,id=id)
            userlisting = userlisting_obj.userlisting
            if action == "inc":
                userlisting_obj.quantity +=1
                userlisting_obj.subtotal += userlisting_obj.product.price
                userlisting_obj.save()
                userlisting.total +=userlisting_obj.product.price
                userlisting.save()
                return Response({"Message":"Item increase"},status=status.HTTP_200_OK)
            elif action == "dcr":
                userlisting_obj.quantity -=1
                userlisting_obj.subtotal -= userlisting_obj.product.price
                userlisting_obj.save()
                userlisting.total -=userlisting_obj.product.price
                userlisting.save()
                if userlisting_obj.quantity == 0:
                    userlisting_obj.delete()
                return Response({"Message":"Item decrease"},status=status.HTTP_200_OK)
            elif action == 'rmv':
                userlisting.total -= userlisting_obj.subtotal
                userlisting.save()
                userlisting_obj.delete()
                return Response({"Message":"Item removed"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

