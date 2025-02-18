from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import Meal, BMI
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions  import IsAuthenticated, AllowAny
from .serializers import UserSerializer, MealSerializer

User = get_user_model()

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action == "create":
            
            return [AllowAny()] 
        return [IsAuthenticated]
            

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class= MealSerializer
    permission_classes = [IsAuthenticated] 
    
    
    # filtrer les repas par utilisateur connecte 
    def get_queryset(self):
        
        user = self.request.user
        return Meal.objects.filter(user=user) 
    
    
    def perform_create(self, serializer):
        print(f"Utilisateur assigné : {self.request.user} - Type : {type(self.request.user)}")

        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_bmi(request):
    print("Données reçues:", request.data)
    
    try:
        
        # Vérifie si la requête contient du JSON
        user=request.user
        data = request.data  # Utiliser request.data au lieu de json.loads(request.body)

        # Récupération des valeurs
        weight = data.get("weight", None)
        height = data.get("height", None)

        # Vérification des valeurs
        if weight is None or height is None:
            return JsonResponse({"error": "Weight and height are required"}, status=400)

        if height <= 0:
            return JsonResponse({"error": "Height must be greater than zero"}, status=400)

        bmi_value = round(weight / ((height / 100) ** 2), 2)

        # Stocker le calcul
        bmi_entry = BMI.objects.create(user=user, weight=weight, height=height, bmi_value=bmi_value)

        return JsonResponse({
            "bmi": bmi_value,
            "date": bmi_entry.date_calcul
        }, status=201)
        
        
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bmi_history(request): 
    user = request.user
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    bmi_records = BMI.objects.filter(user=user)

    if start_date and end_date:
        bmi_records = bmi_records.filter(date_calcul__range=[start_date, end_date])

    # Sérialiser les données
    data = [{"bmi": record.bmi_value, "date": record.date_calcul} for record in bmi_records]

    return JsonResponse({"history": data}, status=200)
