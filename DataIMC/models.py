from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="dataimc_user_groups",  # Ajout d'un related_name unique  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="dataimc_user_permissions",  # Ajout d'un related_name unique
        blank=True,
    )
    
    
class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=255)
    calories= models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}-{self.calories} kcal"
    
        
class BMI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bmi_records")
    weight = models.FloatField(null=False, blank=False)
    height = models.FloatField(null=False, blank=False)
    bmi_value = models.FloatField(null=True, blank=True)   # IMC calculé
    date_calcul = models.DateTimeField(auto_now_add=True)  # Date du calcul de l'IMC

    def save(self, *args, **kwargs):
        # Calculer l'IMC avant de sauvegarder
        if self.weight and self.height:
            self.bmi = round(self.weight / ((self.height / 100) ** 2), 2)  # IMC = poids / taille^2 (taille en mètre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.bmi}({self.date_calcul})"
