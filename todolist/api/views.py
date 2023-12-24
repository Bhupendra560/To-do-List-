from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Task, Tag
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .serializers import InputSerializer, OutputSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class TASKMODELVIEW(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def validation_duedate(self, serializer):
        timestamp_created = datetime.now().date()
        due_date = serializer.validated_data.get('due_date')

        if due_date and timestamp_created and due_date < timestamp_created:
            raise serializers.ValidationError('Due Date cannot be before Timestamp created')

    def post(self, request):
        # creating new task in db with exception handling
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            self.validation_duedate(serializer)
            validated_data = serializer.data
            try:
                new_task = Task(
                    title=validated_data.get('title'),
                    status=validated_data.get('status'),
                    description=validated_data.get('description')
                )
                if 'due_date' in validated_data:
                    new_task.due_date = str(validated_data.get('due_date'))

                new_task.save()

                if 'tags' in validated_data:
                    tags_list = validated_data.get('tags', [])
                    for tag_value in tags_list:
                        # create the tag based on the value
                        tag_instance, created = Tag.objects.get_or_create(value=str(tag_value))
                        if created:
                            tag_instance.value = str(tag_value)
                            tag_instance.save()

                        # Adding tag to the many-to-many relationship
                        new_task.tags.add(tag_instance)

                return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'Duplicate Entry.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            try:
                # fetching particular task
                task = Task.objects.get(id=pk)
                serializer = OutputSerializer(task).data
                return Response(serializer)

            except Task.DoesNotExist:
                return Response({'message': 'Task with id {} not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                # fetching all tasks from db
                all_tasks = Task.objects.all()
                if all_tasks:
                    serializer = OutputSerializer(all_tasks, many=True).data
                    return Response(serializer)
                else:
                    return Response({'message': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            # checking if task exist, then update it
            existing_task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task with id {} not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'message': 'Duplicate Entry.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not request.data:
            return Response({'message': 'No fields were modified'}, status=status.HTTP_400_BAD_REQUEST)

        tags_data = request.data.pop('tags', None)

        serializer = InputSerializer(existing_task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.validation_duedate(serializer)
        serializer.save()

        if tags_data is not None:
            # Creating new tags and add them to the task
            for tag_id in tags_data:
                tag, created = Tag.objects.get_or_create(id=tag_id)
                existing_task.tags.add(tag)

        return Response({'message': 'Task updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if pk is not None:
            try:
                # Deleting a particular Task
                task = get_object_or_404(Task, id=pk)
                task.delete()
                return Response({'message': f'Task with id {pk} deleted successfully'}, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({'message': 'Task model not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
