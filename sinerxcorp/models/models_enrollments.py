from django.db import models
from django.conf import settings
from .models_courses import Course, Lesson


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField('Fecha de inscripción', auto_now_add=True)
    is_active = models.BooleanField('Inscripción activa', default=True)

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course_enrollment')
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} inscrito en {self.course.title}"

    def get_progress_percentage(self):
        """Calcula el porcentaje de progreso del alumno en el curso."""
        total_lessons = Lesson.objects.filter(module__course=self.course).count()
        if total_lessons == 0:
            return 0.0

        completed_lessons = LessonProgress.objects.filter(
            student=self.student,
            lesson__module__course=self.course,
            is_completed=True
        ).count()

        return round((completed_lessons / total_lessons) * 100, 2)


class LessonProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField('Completada', default=False)
    completed_at = models.DateTimeField('Fecha de finalización', null=True, blank=True)

    class Meta:
        verbose_name = 'Progreso de lección'
        verbose_name_plural = 'Progresos de lecciones'
        constraints = [
            models.UniqueConstraint(fields=['student', 'lesson'], name='unique_student_lesson_progress')
        ]

    def __str__(self):
        status = "Completada" if self.is_completed else "En progreso"
        return f"{self.student.username} - {self.lesson.title}: {status}"