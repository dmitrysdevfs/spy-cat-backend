from django.db import models
from django.core.validators import MinValueValidator

class SpyCat(models.Model):
    name = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.name

class Mission(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    
    cat = models.ForeignKey(
        SpyCat, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True, 
        related_name='missions'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )

    def __str__(self):
        return f"Mission {self.id} ({self.status})"

class Target(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    mission = models.ForeignKey(
        Mission, 
        on_delete=models.CASCADE, 
        related_name='targets'
    )
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    def __str__(self):
        return f"Target {self.name} ({self.status})"
