#!/usr/bin/env python3
"""
Simple NutriVeda Backend with Database Support
Fixed version with proper imports
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import path, include
from django.core.wsgi import get_wsgi_application
import json
import pandas as pd
from datetime import datetime, timedelta
import uuid

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Django Settings Configuration
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='nutriveda-secret-key-2024',
        ALLOWED_HOSTS=['*'],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'corsheaders',
            'backend',  # Our app
        ],
        MIDDLEWARE=[
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ],
        ROOT_URLCONF=__name__,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'nutriveda.db',
            }
        },
        CORS_ALLOW_ALL_ORIGINS=True,
        CORS_ALLOW_CREDENTIALS=True,
        STATIC_URL='/static/',
        MEDIA_URL='/media/',
    )

django.setup()

# Import models after Django setup
from backend.models import Patient, FoodItem, DietChart, DoshaAssessment

# API Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def patients_api(request):
    """Patient management API"""
    if request.method == 'GET':
        patients = Patient.objects.all().order_by('-created_at')
        patients_data = []
        for patient in patients:
            patients_data.append({
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'phone': patient.phone,
                'email': patient.email,
                'height': patient.height,
                'weight': patient.weight,
                'bmi': patient.bmi,
                'prakriti': patient.prakriti,
                'diet': patient.diet,
                'meal_frequency': patient.meal_frequency,
                'water_intake': patient.water_intake,
                'activity_level': patient.activity_level,
                'bowel_movement': patient.bowel_movement,
                'sleep_hours': patient.sleep_hours,
                'stress_level': patient.stress_level,
                'medical_history': patient.medical_history,
                'current_medications': patient.current_medications,
                'allergies': patient.allergies,
                'occupation': patient.occupation,
                'exercise_frequency': patient.exercise_frequency,
                'last_visit': patient.last_visit.strftime('%Y-%m-%d'),
                'created_at': patient.created_at.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({
            'success': True,
            'data': patients_data,
            'total': len(patients_data)
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Calculate BMI if height and weight provided
            bmi = None
            if data.get('height') and data.get('weight'):
                height_m = float(data['height']) / 100
                bmi = round(float(data['weight']) / (height_m * height_m), 1)
            
            # Create new patient in database
            patient = Patient.objects.create(
                name=data.get('name'),
                age=data.get('age'),
                gender=data.get('gender'),
                phone=data.get('phone', ''),
                email=data.get('email', ''),
                height=data.get('height'),
                weight=data.get('weight'),
                bmi=bmi,
                prakriti=data.get('prakriti', ''),
                diet=data.get('diet', 'Vegetarian'),
                meal_frequency=data.get('meal_frequency', 3),
                water_intake=data.get('water_intake', 2.5),
                activity_level=data.get('activity_level', 'Moderate'),
                bowel_movement=data.get('bowel_movement', 'Regular'),
                sleep_hours=data.get('sleep_hours', 7),
                stress_level=data.get('stress_level', 'Medium'),
                medical_history=data.get('medical_history', ''),
                current_medications=data.get('current_medications', ''),
                allergies=data.get('allergies', ''),
                occupation=data.get('occupation', ''),
                exercise_frequency=data.get('exercise_frequency', '')
            )
            
            # Return patient data
            patient_data = {
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'phone': patient.phone,
                'email': patient.email,
                'height': patient.height,
                'weight': patient.weight,
                'bmi': patient.bmi,
                'prakriti': patient.prakriti,
                'diet': patient.diet,
                'meal_frequency': patient.meal_frequency,
                'water_intake': patient.water_intake,
                'activity_level': patient.activity_level,
                'bowel_movement': patient.bowel_movement,
                'sleep_hours': patient.sleep_hours,
                'stress_level': patient.stress_level,
                'medical_history': patient.medical_history,
                'current_medications': patient.current_medications,
                'allergies': patient.allergies,
                'occupation': patient.occupation,
                'exercise_frequency': patient.exercise_frequency,
                'last_visit': patient.last_visit.strftime('%Y-%m-%d'),
                'created_at': patient.created_at.strftime('%Y-%m-%d')
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Patient added successfully',
                'data': patient_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def food_database_api(request):
    """Food database API"""
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    # Start with all food items
    foods = FoodItem.objects.all()
    
    # Apply filters
    if category:
        foods = foods.filter(category__iexact=category)
    
    if search:
        foods = foods.filter(name__icontains=search)
    
    # Convert to list format
    foods_data = []
    for food in foods:
        foods_data.append({
            'id': food.id,
            'name': food.name,
            'category': food.category,
            'calories': food.calories,
            'serving': food.serving,
            'protein': food.protein,
            'carbs': food.carbs,
            'fat': food.fat,
            'fiber': food.fiber,
            'virya': food.virya,
            'digestion': food.digestion,
            'rasa': food.rasa,
            'guna': food.guna,
            'vata': food.vata_effect,
            'pitta': food.pitta_effect,
            'kapha': food.kapha_effect,
            'season': food.season,
            'benefits': food.benefits,
            'precautions': food.precautions,
            'description': food.description
        })
    
    return JsonResponse({
        'success': True,
        'data': foods_data,
        'total': len(foods_data)
    })

def generate_database_driven_diet_chart(patient, target_calories, goal):
    """Generate diet chart using foods from the database based on patient constitution"""
    constitution = patient.prakriti.lower() if patient.prakriti else 'vata'
    
    # Define meal structure with calorie distribution
    meal_structure = [
        {'name': 'Early Morning', 'time': '6:00 AM', 'calorie_percent': 0.05},
        {'name': 'Breakfast', 'time': '8:00 AM', 'calorie_percent': 0.25},
        {'name': 'Mid-Morning Snack', 'time': '11:00 AM', 'calorie_percent': 0.10},
        {'name': 'Lunch', 'time': '1:00 PM', 'calorie_percent': 0.35},
        {'name': 'Evening Snack', 'time': '4:00 PM', 'calorie_percent': 0.10},
        {'name': 'Dinner', 'time': '7:00 PM', 'calorie_percent': 0.15}
    ]
    
    meals = []
    
    for meal_info in meal_structure:
        meal_calories = int(target_calories * meal_info['calorie_percent'])
        meal_items = select_foods_for_meal(constitution, meal_info['name'], meal_calories)
        
        meal = {
            'name': meal_info['name'],
            'time': meal_info['time'],
            'items': meal_items,
            'totalCalories': sum(item['calories'] for item in meal_items)
        }
        meals.append(meal)
    
    # Add bedtime drink
    bedtime_items = select_foods_for_meal(constitution, 'Bedtime', 50)
    meals.append({
        'name': 'Bedtime',
        'time': '9:00 PM',
        'items': bedtime_items,
        'totalCalories': sum(item['calories'] for item in bedtime_items)
    })
    
    return {
        'patientName': patient.name,
        'constitution': patient.prakriti,
        'goal': goal,
        'calories': target_calories,
        'duration': 30,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'meals': meals,
        'guidelines': get_constitution_guidelines(constitution),
        'seasonalRecommendations': get_seasonal_recommendations(),
        'doNotEat': get_foods_to_avoid(constitution)
    }

def select_foods_for_meal(constitution, meal_name, target_calories):
    """Select appropriate foods from database for a specific meal based on constitution"""
    foods = []
    
    # Define meal categories and their calorie distribution
    if meal_name == 'Early Morning':
        categories = ['Beverages', 'Nuts']
        calorie_distribution = [0.3, 0.7]
    elif meal_name == 'Breakfast':
        categories = ['Grains', 'Fruits', 'Beverages']
        calorie_distribution = [0.6, 0.3, 0.1]
    elif meal_name == 'Mid-Morning Snack':
        categories = ['Beverages', 'Nuts', 'Fruits']
        calorie_distribution = [0.2, 0.5, 0.3]
    elif meal_name == 'Lunch':
        categories = ['Grains', 'Legumes', 'Vegetables', 'Dairy']
        calorie_distribution = [0.4, 0.3, 0.2, 0.1]
    elif meal_name == 'Evening Snack':
        categories = ['Beverages', 'Nuts', 'Fruits']
        calorie_distribution = [0.3, 0.4, 0.3]
    elif meal_name == 'Dinner':
        categories = ['Grains', 'Vegetables', 'Dairy']
        calorie_distribution = [0.5, 0.3, 0.2]
    elif meal_name == 'Bedtime':
        categories = ['Beverages', 'Dairy']
        calorie_distribution = [0.7, 0.3]
    else:
        categories = ['Grains', 'Vegetables']
        calorie_distribution = [0.6, 0.4]
    
    # Select foods for each category
    for i, category in enumerate(categories):
        if i < len(calorie_distribution):
            category_calories = int(target_calories * calorie_distribution[i])
            category_foods = get_foods_by_category_and_constitution(category, constitution, category_calories)
            foods.extend(category_foods)
    
    # If no foods found, add some basic items
    if not foods:
        foods = get_fallback_foods(meal_name, target_calories)
    
    return foods

def get_foods_by_category_and_constitution(category, constitution, target_calories):
    """Get foods from database filtered by category and constitution compatibility"""
    try:
        # Get foods from the category
        category_foods = FoodItem.objects.filter(category__iexact=category)
        
        # Filter by constitution compatibility
        constitution_foods = []
        for food in category_foods:
            if is_food_compatible_with_constitution(food, constitution):
                constitution_foods.append(food)
        
        # If no compatible foods found, get any foods from category
        if not constitution_foods:
            constitution_foods = list(category_foods)
        
        # Select foods to meet calorie target
        selected_foods = []
        remaining_calories = target_calories
        
        # Sort by constitution compatibility (prefer foods that balance the constitution)
        constitution_foods.sort(key=lambda x: get_constitution_compatibility_score(x, constitution), reverse=True)
        
        for food in constitution_foods[:5]:  # Limit to 5 foods per category
            if remaining_calories <= 0:
                break
                
            # Calculate quantity based on calories
            quantity = min(remaining_calories / food.calories, 3)  # Max 3 servings
            if quantity >= 0.5:  # Only include if at least half serving
                selected_foods.append({
                    'name': food.name,
                    'quantity': f"{quantity:.1f} {food.serving}",
                    'calories': int(food.calories * quantity),
                    'virya': food.virya,
                    'rasa': food.rasa,
                    'category': food.category
                })
                remaining_calories -= int(food.calories * quantity)
        
        return selected_foods
        
    except Exception as e:
        print(f"Error selecting foods: {e}")
        return []

def is_food_compatible_with_constitution(food, constitution):
    """Check if food is compatible with patient's constitution"""
    if constitution == 'vata':
        # Vata needs grounding, warming foods
        return food.virya.lower() in ['hot', 'warm'] and food.guna.lower() in ['heavy', 'moist']
    elif constitution == 'pitta':
        # Pitta needs cooling, calming foods
        return food.virya.lower() in ['cold', 'cool'] and food.guna.lower() in ['light', 'cooling']
    elif constitution == 'kapha':
        # Kapha needs light, warming foods
        return food.virya.lower() in ['hot', 'warm'] and food.guna.lower() in ['light', 'dry']
    return True  # Default to compatible

def get_constitution_compatibility_score(food, constitution):
    """Get a score indicating how well a food suits the constitution"""
    score = 0
    
    if constitution == 'vata':
        if food.virya.lower() in ['hot', 'warm']: score += 2
        if food.guna.lower() in ['heavy', 'moist']: score += 2
        if food.vata_effect == '↓': score += 3  # Foods that reduce vata
    elif constitution == 'pitta':
        if food.virya.lower() in ['cold', 'cool']: score += 2
        if food.guna.lower() in ['light', 'cooling']: score += 2
        if food.pitta_effect == '↓': score += 3  # Foods that reduce pitta
    elif constitution == 'kapha':
        if food.virya.lower() in ['hot', 'warm']: score += 2
        if food.guna.lower() in ['light', 'dry']: score += 2
        if food.kapha_effect == '↓': score += 3  # Foods that reduce kapha
    
    return score

def get_fallback_foods(meal_name, target_calories):
    """Provide fallback foods if database selection fails"""
    fallback_foods = {
        'Early Morning': [
            {'name': 'Warm Water with Lemon', 'quantity': '1 glass', 'calories': 5, 'virya': 'Hot'},
            {'name': 'Soaked Almonds', 'quantity': '5-6 pieces', 'calories': 35, 'virya': 'Hot'}
        ],
        'Breakfast': [
            {'name': 'Oatmeal with Fruits', 'quantity': '1 bowl', 'calories': int(target_calories * 0.6), 'virya': 'Cold'},
            {'name': 'Herbal Tea', 'quantity': '1 cup', 'calories': 5, 'virya': 'Hot'}
        ],
        'Mid-Morning Snack': [
            {'name': 'Green Tea', 'quantity': '1 cup', 'calories': 2, 'virya': 'Hot'},
            {'name': 'Mixed Nuts', 'quantity': '10-12 pieces', 'calories': int(target_calories * 0.8), 'virya': 'Hot'}
        ],
        'Lunch': [
            {'name': 'Dal with Rice', 'quantity': '1 plate', 'calories': int(target_calories * 0.6), 'virya': 'Hot'},
            {'name': 'Vegetable Curry', 'quantity': '1 serving', 'calories': int(target_calories * 0.3), 'virya': 'Hot'},
            {'name': 'Chapati', 'quantity': '2 pieces', 'calories': int(target_calories * 0.1), 'virya': 'Hot'}
        ],
        'Evening Snack': [
            {'name': 'Herbal Tea', 'quantity': '1 cup', 'calories': 5, 'virya': 'Hot'},
            {'name': 'Roasted Chana', 'quantity': '1 small bowl', 'calories': int(target_calories * 0.8), 'virya': 'Hot'}
        ],
        'Dinner': [
            {'name': 'Chapati with Sabzi', 'quantity': '2 pieces', 'calories': int(target_calories * 0.7), 'virya': 'Hot'},
            {'name': 'Dal', 'quantity': '1 bowl', 'calories': int(target_calories * 0.3), 'virya': 'Hot'}
        ],
        'Bedtime': [
            {'name': 'Warm Milk with Turmeric', 'quantity': '1 glass', 'calories': 50, 'virya': 'Hot'}
        ]
    }
    
    return fallback_foods.get(meal_name, [
        {'name': 'Balanced Meal', 'quantity': '1 serving', 'calories': target_calories, 'virya': 'Hot'}
    ])

def get_constitution_guidelines(constitution):
    """Get dietary guidelines based on constitution"""
    guidelines = {
        'vata': [
            'Eat warm, cooked foods',
            'Include sweet, sour, and salty tastes',
            'Avoid cold, raw foods',
            'Maintain regular meal times',
            'Include healthy fats and oils'
        ],
        'pitta': [
            'Eat cooling, calming foods',
            'Include sweet, bitter, and astringent tastes',
            'Avoid spicy, hot foods',
            'Eat at regular intervals',
            'Include fresh fruits and vegetables'
        ],
        'kapha': [
            'Eat light, warm foods',
            'Include pungent, bitter, and astringent tastes',
            'Avoid heavy, oily foods',
            'Eat smaller portions',
            'Include plenty of vegetables and spices'
        ]
    }
    return guidelines.get(constitution, [
        'Eat balanced, nutritious meals',
        'Maintain regular meal times',
        'Include variety in your diet',
        'Stay hydrated'
    ])

def get_seasonal_recommendations():
    """Get seasonal dietary recommendations"""
    return [
        'Include seasonal fruits and vegetables',
        'Adjust spices according to season',
        'Stay hydrated with herbal teas',
        'Modify cooking methods for seasonal needs'
    ]

def get_foods_to_avoid(constitution):
    """Get foods to avoid based on constitution"""
    avoid_foods = {
        'vata': ['Cold foods', 'Raw vegetables', 'Excess bitter taste', 'Dry foods'],
        'pitta': ['Spicy foods', 'Hot beverages', 'Sour foods', 'Fried foods'],
        'kapha': ['Heavy foods', 'Oily foods', 'Sweet foods', 'Cold drinks']
    }
    return avoid_foods.get(constitution, ['Processed foods', 'Excess sugar', 'Artificial additives'])

@csrf_exempt
def analytics_api(request):
    """Analytics and statistics API"""
    total_patients = Patient.objects.count()
    total_diet_charts = DietChart.objects.count()
    total_assessments = DoshaAssessment.objects.count()
    
    # Constitution distribution
    constitution_counts = {}
    for patient in Patient.objects.all():
        const = patient.prakriti or 'Unknown'
        constitution_counts[const] = constitution_counts.get(const, 0) + 1
    
    # Recent patients
    recent_patients = []
    for patient in Patient.objects.all().order_by('-created_at')[:5]:
        recent_patients.append({
            'id': patient.id,
            'name': patient.name,
            'created_at': patient.created_at.strftime('%Y-%m-%d')
        })
    
    return JsonResponse({
        'success': True,
        'data': {
            'total_patients': total_patients,
            'total_diet_charts': total_diet_charts,
            'total_assessments': total_assessments,
            'constitution_distribution': constitution_counts,
            'recent_patients': recent_patients,
            'food_categories': list(set(food.category for food in FoodItem.objects.all()))
        }
    })

@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def diet_charts_api(request):
    """Diet charts API"""
    if request.method == 'GET':
        charts = DietChart.objects.all().order_by('-created_at')
        charts_data = []
        for chart in charts:
            charts_data.append({
                'id': str(chart.id),
                'patient_id': chart.patient.id,
                'patientName': chart.patient.name,
                'patient_name': chart.patient.name,
                'goal': chart.goal,
                'target_calories': chart.target_calories,
                'duration': chart.duration,
                'chart_data': chart.chart_data,
                'createdDate': chart.created_at.strftime('%Y-%m-%d'),
                'created_at': chart.created_at.strftime('%Y-%m-%d'),
                'status': chart.status,
                'chart': {
                    'duration': chart.duration
                }
            })
        
        return JsonResponse({
            'success': True,
            'data': charts_data,
            'total': len(charts_data)
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Generate diet chart based on patient constitution
            patient_id = data.get('patient_id')
            patient = Patient.objects.get(id=patient_id)
            
            # Generate diet chart using foods from database
            target_calories = data.get('target_calories', 2000)
            diet_chart_data = generate_database_driven_diet_chart(patient, target_calories, data.get('goal', 'Maintenance'))
            
            new_chart = DietChart.objects.create(
                patient=patient,
                goal=data.get('goal', 'Maintenance'),
                target_calories=data.get('target_calories', 2000),
                duration=data.get('duration', 30),
                chart_data=diet_chart_data
            )
            
            chart_data = {
                'id': str(new_chart.id),
                'patient_id': patient_id,
                'patientName': patient.name,
                'patient_name': patient.name,
                'goal': new_chart.goal,
                'target_calories': new_chart.target_calories,
                'duration': new_chart.duration,
                'chart_data': new_chart.chart_data,
                'createdDate': new_chart.created_at.strftime('%Y-%m-%d'),
                'created_at': new_chart.created_at.strftime('%Y-%m-%d'),
                'status': new_chart.status,
                'chart': {
                    'duration': new_chart.duration
                }
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Diet chart generated successfully',
                'data': chart_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            chart_id = data.get('chart_id')
            
            if not chart_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Chart ID is required'
                }, status=400)
            
            # Find and delete the diet chart
            chart = DietChart.objects.get(id=chart_id)
            patient_name = chart.patient.name
            chart.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Diet chart for {patient_name} deleted successfully'
            })
            
        except DietChart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Diet chart not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

# URL Configuration
urlpatterns = [
    path('api/patients/', patients_api, name='patients'),
    path('api/food-database/', food_database_api, name='food_database'),
    path('api/diet-charts/', diet_charts_api, name='diet_charts'),
    path('api/analytics/', analytics_api, name='analytics'),
]

# Static file serving for development
from django.conf.urls.static import static
from django.views.static import serve

def serve_static(request, path):
    """Serve static files in development"""
    document_root = os.path.join(os.path.dirname(__file__), './')
    return serve(request, path, document_root=document_root)

urlpatterns += [
    path('<path:path>', serve_static),
]

def initialize_food_database():
    """Initialize comprehensive food database from Book1.csv"""
    
    import csv
    import os
    
    # Read from Book1.csv
    csv_file = os.path.join(os.path.dirname(__file__), 'Book1.csv')
    
    if not os.path.exists(csv_file):
        print("❌ Book1.csv not found, using default food items")
        return
    
    print("📖 Reading food data from Book1.csv...")
    
    # Parse CSV and create food items
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        
        for row in csv_reader:
            if len(row) < 3 or not row[0].strip():  # Skip empty rows
                continue
                
            try:
                # Extract data from CSV row
                name = row[0].strip()
                if not name or name.startswith(','):  # Skip empty names
                    continue
                    
                # Map CSV columns to our food item structure
                # CSV structure: Name, Category, Calories, Water, Protein, Fat, Carbs, Fiber, etc.
                category_num = int(row[1]) if row[1] else 6
                calories = int(float(row[2])) if row[2] else 100
                water = float(row[3]) if row[3] else 80
                protein = float(row[4]) if row[4] else 5
                fat = float(row[5]) if row[5] else 2
                carbs = float(row[6]) if row[6] else 15
                fiber = float(row[7]) if row[7] else 2
                
                # Map category number to category name
                category_map = {
                    1: "Vegetables", 2: "Fruits", 3: "Grains", 4: "Proteins", 
                    5: "Dairy", 6: "Spices", 7: "Nuts", 8: "Oils", 9: "Beverages", 10: "Other"
                }
                category = category_map.get(category_num, "Other")
                
                # Determine Ayurvedic properties based on food type
                virya = "Cold" if category in ["Fruits", "Vegetables"] else "Hot"
                digestion = "Easy" if category in ["Fruits", "Vegetables"] else "Hard"
                rasa = "Sweet" if category in ["Fruits", "Dairy"] else "Pungent"
                guna = "Light" if category in ["Fruits", "Vegetables"] else "Heavy"
                
                # Dosha effects (simplified)
                vata_effect = "↓" if category in ["Dairy", "Grains"] else "↑"
                pitta_effect = "↓" if category in ["Fruits", "Vegetables"] else "↑"
                kapha_effect = "↑" if category in ["Dairy", "Grains"] else "↓"
                
                # Create food item if it doesn't exist
                if not FoodItem.objects.filter(name=name).exists():
                    FoodItem.objects.create(
                        name=name,
                        category=category,
                        calories=calories,
                        serving="100g",
                        protein=protein,
                        carbs=carbs,
                        fat=fat,
                        fiber=fiber,
                        virya=virya,
                        digestion=digestion,
                        rasa=rasa,
                        guna=guna,
                        vata_effect=vata_effect,
                        pitta_effect=pitta_effect,
                        kapha_effect=kapha_effect,
                        season=["All"],
                        benefits=["Nutritional value", "Health benefits"],
                        precautions=["Allergies"],
                        description=f"{name} is a {category.lower()} with {virya.lower()} virya and {rasa.lower()} rasa."
                    )
                    
            except (ValueError, IndexError) as e:
                continue  # Skip malformed rows
    
    print(f"✅ Food database initialized with {FoodItem.objects.count()} items from Book1.csv!")

# WSGI Application
application = get_wsgi_application()

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 8000))
    print(f"🕉️  NutriVeda Backend (Fixed) starting on port {port}")
    # Initialize food database if empty
    if FoodItem.objects.count() < 10:
        print("🍽️  Initializing comprehensive food database...")
        initialize_food_database()
    
    print(f"📊 Database: {Patient.objects.count()} patients, {FoodItem.objects.count()} food items")
    print(f"🌐 Access your application at: http://localhost:{port}")
    
    # Start development server
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])
