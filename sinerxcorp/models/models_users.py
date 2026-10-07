from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    class Roles(models.TextChoices):
        STUDENT = 'STUDENT', 'Estudiante'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        ADMIN = 'ADMIN', 'Administrador'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField('Rol', max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    profile_picture = models.ImageField('Foto de perfil', upload_to='profiles/', null=True, blank=True)
    bio = models.TextField('Biografía', blank=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"