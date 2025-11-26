from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ViewSet):
    def list(self, request):
        courses = Course.objects.filter(deleted_at__isnull=True)
        
        # Filter by is_active query parameter
        is_active_param = request.query_params.get('is_active')
        if is_active_param is not None:
            if is_active_param.lower() == 'true':
                courses = courses.filter(is_active=True)
            elif is_active_param.lower() == 'false':
                courses = courses.filter(is_active=False)
        
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try: 
            course = Course.objects.get(pk=pk, deleted_at__isnull=True)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk, deleted_at__isnull=True)
            if course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk, deleted_at__isnull=True)
            if course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            course.deleted_at = timezone.now()
            course.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk, deleted_at__isnull=True)
            if course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            if course.is_active:
                return Response({'Error': 'Course is already active.'}, status=status.HTTP_400_BAD_REQUEST)
            
            course.is_active = True
            course.save()
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk, deleted_at__isnull=True)
            if course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            if not course.is_active:
                return Response({'Error': 'Course is already inactive.'}, status=status.HTTP_400_BAD_REQUEST)
            
            course.is_active = False
            course.save()
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk, deleted_at__isnull=True)
            lessons = Lesson.objects.filter(course=course, deleted_at__isnull=True)
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class LessonViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data.copy()
        
        # Automatic order - become first (lowest order number)
        course_id = data.get('course')
        if course_id:
            try:
                course_lessons = Lesson.objects.filter(
                    course_id=course_id, 
                    deleted_at__isnull=True
                ).order_by('order')
                if course_lessons.exists():
                    first_lesson = course_lessons.first()
                    data['order'] = first_lesson.order - 1.0  # Become before first
                else:
                    data['order'] = 1.0
            except:
                data['order'] = 1.0
        
        serializer = LessonSerializer(data=data)
        if serializer.is_valid():
            course = serializer.validated_data['course']
            if course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
            if lesson.course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            lesson.deleted_at = timezone.now()
            lesson.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
            if lesson.course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            lesson.is_published = True
            lesson.save()
            serializer = LessonSerializer(lesson)
            return Response(serializer.data)
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
            if lesson.course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            lesson.is_published = False
            lesson.save()
            serializer = LessonSerializer(lesson)
            return Response(serializer.data)
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def move(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(pk=pk, deleted_at__isnull=True)
            if lesson.course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            before_lesson_id = request.data.get('before_lesson_id')
            course_lessons = Lesson.objects.filter(
                course=lesson.course, 
                deleted_at__isnull=True
            ).exclude(pk=lesson.pk).order_by('order')
            
            if before_lesson_id:
                # Move before specific lesson
                try:
                    before_lesson = Lesson.objects.get(
                        pk=before_lesson_id, 
                        course=lesson.course,
                        deleted_at__isnull=True
                    )
                    # Simple implementation - set order slightly less than before_lesson
                    lesson.order = before_lesson.order - 0.1
                    lesson.indentation = before_lesson.indentation
                except Lesson.DoesNotExist:
                    return Response({"error": "Before lesson not found"}, status=400)
            else:
                # Move to the end
                if course_lessons.exists():
                    last_lesson = course_lessons.last()
                    lesson.order = last_lesson.order + 1.0
                else:
                    lesson.order = 1.0
                lesson.indentation = 0
            
            lesson.save()
            return Response({"order": lesson.order, "indentation": lesson.indentation})
            
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)