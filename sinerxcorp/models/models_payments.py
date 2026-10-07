from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from .models_courses import Course


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        STRIPE = 'STRIPE', 'Stripe'
        MERCADOPAGO = 'MERCADOPAGO', 'Mercado Pago'
        PAYPAL = 'PAYPAL', 'PayPal'

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        COMPLETED = 'COMPLETED', 'Completado'
        FAILED = 'FAILED', 'Fallido'
        REFUNDED = 'REFUNDED', 'Reembolsado'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.DecimalField('Monto pago', max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    payment_method = models.CharField('Método de pago', max_length=20, choices=PaymentMethod.choices)
    transaction_id = models.CharField('ID Transacción', max_length=255, unique=True)
    status = models.CharField('Estado', max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pago {self.transaction_id} - {self.user.email} ({self.status})"