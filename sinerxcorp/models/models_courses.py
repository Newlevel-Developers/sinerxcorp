from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('Nombre', max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='courses_taught'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField('Subtítulo', max_length=255, blank=True)
    description = models.TextField('Descripción')
    cover_image = models.ImageField('Imagen de portada', upload_to='course_covers/')
    price = models.DecimalField('Precio', max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    is_published = models.BooleanField('Publicado', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField('Título del módulo', max_length=200)
    order = models.PositiveIntegerField('Orden', default=1)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['course', 'order'], name='unique_module_order_per_course')
        ]

    def __str__(self):
        return f"{self.course.title} - Módulo {self.order}: {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Título de la lección', max_length=200)
    description = models.TextField('Descripción', blank=True)
    video_url = models.URLField('URL del video', max_length=500)
    duration_in_seconds = models.PositiveIntegerField('Duración en segundos', default=0)
    is_free_preview = models.BooleanField('Vista previa gratuita', default=False)
    order = models.PositiveIntegerField('Orden', default=1)

    class Meta:
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['module', 'order'], name='unique_lesson_order_per_module')
        ]

    def __str__(self):
        return f"{self.module.title} - Lección {self.order}: {self.title}"


class LessonResource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField('Título del recurso', max_length=150)
    file = models.FileField('Archivo adjunto', upload_to='lesson_resources/')

    class Meta:
        verbose_name = 'Recurso de lección'
        verbose_name_plural = 'Recursos de lecciones'

    def __str__(self):
        return f"Recurso: {self.title} ({self.lesson.title})"