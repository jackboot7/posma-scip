from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from django.utils.datastructures import MultiValueDict

from apps.organization.models import *
from apps.api.serializers import *


class UsersView(APIView):
    """
    Main /username/ endpoint view
    """
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get(self, request, format=None):
        users = User.objects.exclude(is_staff=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificUserView(APIView):
    """
    /users/{username} endpoint view
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_object(username)    # get or create <----
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # si no existe debe crearlo y enviar 201

    def delete(self, request, username, format=None):
        user = self.get_object(username)
        try:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserWorkdaysView(APIView):
    """
    /users/{username}/workdays/ endpoint view
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        usr = self.get_object(username)
        workdays = usr.workday_set.all()
        serializer = WorkdaySerializer(workdays, many=True)
        return Response(serializer.data)

    def post(self, request, username, format=None):
        usr = self.get_object(username)
        last = usr.workday_set.latest('start')
        if not last.finish:
            return Response({'detail': "Last workday hasn't finished yet for given user."},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        data = MultiValueDict(request.DATA)
        data['user'] = username
        serializer = WorkdaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLastWorkdayView(APIView):
    """
    /users/{username}/workdays/last/ endpoint view
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, username):
        try:
            workday = Workday.objects.user(username).latest('start')
            return workday
        except User.DoesNotExist:
            raise Http404
        except Workday.DoesNotExist:
            return None

    def get(self, request, username, format=None):
        serializer = WorkdaySerializer(self.get_object(username))
        return Response(serializer.data)

    def put(self, request, username, format=None):
        workday = self.get_object(username)
        if workday.finish:
            return Response({'detail': "Selected workday has already finished. It can't be edited."},
                            status=status.HTTP_412_PRECONDITION_FAILED)

        data = MultiValueDict(request.DATA)
        data['user'] = username
        serializer = WorkdaySerializer(workday, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        workday = self.get_object(username)
        try:
            workday.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WorkdaysView(APIView):
    """
    Main /workdays/ endpoint API view
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        users = Workday.objects.all()
        serializer = WorkdaySerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WorkdaySerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificWorkdayView(APIView):
    """
    /workdays/{id} endpoint API view
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, id):
        try:
            return Workday.objects.get(pk=id)
        except Workday.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        workday = self.get_object(pk)
        serializer = WorkdaySerializer(workday)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        workday = self.get_object(pk)
        if workday.finish:
            return Response({'detail': "Selected workday has already finished. It can't be edited."},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        serializer = WorkdaySerializer(workday, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        workday = self.get_object(pk)
        try:
            workday.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
