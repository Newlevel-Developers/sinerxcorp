from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from .models_courses import Course, Lesson


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        'Calificación',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('Comentario', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['course', 'student'], name='unique_course_review_per_student')
        ]

    def __str__(self):
        return f"Reseña {self.rating}/5 de {self.student.username} para {self.course.title}"


class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField('Comentario')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.lesson.title}"