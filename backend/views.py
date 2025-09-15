"""
NutriVeda API Views
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from datetime import datetime

from .models import Patient, FoodItem, DietChart, DoshaAssessment

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

@csrf_exempt
@require_http_methods(["GET", "POST"])
def diet_charts_api(request):
    """Diet charts API"""
    if request.method == 'GET':
        charts = DietChart.objects.all().order_by('-created_at')
        charts_data = []
        for chart in charts:
            charts_data.append({
                'id': str(chart.id),
                'patient_id': chart.patient.id,
                'patient_name': chart.patient.name,
                'goal': chart.goal,
                'target_calories': chart.target_calories,
                'duration': chart.duration,
                'chart_data': chart.chart_data,
                'created_at': chart.created_at.strftime('%Y-%m-%d'),
                'status': chart.status
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
            
            diet_chart = generate_ayurvedic_diet_chart(patient, data)
            
            new_chart = DietChart.objects.create(
                patient=patient,
                goal=data.get('goal', 'Maintenance'),
                target_calories=data.get('target_calories', 2000),
                duration=data.get('duration', 30),
                chart_data=diet_chart
            )
            
            chart_data = {
                'id': str(new_chart.id),
                'patient_id': patient_id,
                'patient_name': patient.name,
                'goal': new_chart.goal,
                'target_calories': new_chart.target_calories,
                'duration': new_chart.duration,
                'chart_data': new_chart.chart_data,
                'created_at': new_chart.created_at.strftime('%Y-%m-%d'),
                'status': new_chart.status
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

@csrf_exempt
@require_http_methods(["POST"])
def dosha_assessment_api(request):
    """Dosha assessment API"""
    try:
        data = json.loads(request.body)
        
        # Process dosha assessment results
        assessment = DoshaAssessment.objects.create(
            patient_id=data.get('patient_id'),
            assessment_type=data.get('assessment_type', 'comprehensive'),
            responses=data.get('responses', {}),
            primary_dosha=data.get('primary_dosha'),
            dosha_scores=data.get('dosha_scores', {}),
            confidence=data.get('confidence', 0),
            recommendations=generate_dosha_recommendations(data.get('primary_dosha'))
        )
        
        assessment_data = {
            'id': str(assessment.id),
            'patient_id': assessment.patient_id,
            'assessment_type': assessment.assessment_type,
            'responses': assessment.responses,
            'primary_dosha': assessment.primary_dosha,
            'dosha_scores': assessment.dosha_scores,
            'confidence': assessment.confidence,
            'recommendations': assessment.recommendations,
            'created_at': assessment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return JsonResponse({
            'success': True,
            'message': 'Dosha assessment saved successfully',
            'data': assessment_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

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

# Helper functions
def generate_ayurvedic_diet_chart(patient, preferences):
    """Generate personalized Ayurvedic diet chart"""
    constitution = patient.prakriti.lower()
    goal = preferences.get('goal', 'Maintenance')
    target_calories = preferences.get('target_calories', 2000)
    
    # Base meal structure
    meals = []
    
    # Early Morning (6:00 AM)
    early_morning = {
        'name': 'Early Morning',
        'time': '6:00 AM',
        'items': [],
        'total_calories': 0
    }
    
    if 'vata' in constitution:
        early_morning['items'] = [
            {'name': 'Warm Water with Ginger', 'quantity': '1 glass', 'calories': 10, 'virya': 'Hot'},
            {'name': 'Soaked Almonds', 'quantity': '5-6 pieces', 'calories': 70, 'virya': 'Hot'}
        ]
    elif 'pitta' in constitution:
        early_morning['items'] = [
            {'name': 'Cool Water with Lime', 'quantity': '1 glass', 'calories': 8, 'virya': 'Cold'},
            {'name': 'Soaked Almonds (peeled)', 'quantity': '4-5 pieces', 'calories': 60, 'virya': 'Hot'}
        ]
    else:  # Kapha
        early_morning['items'] = [
            {'name': 'Warm Water with Honey', 'quantity': '1 glass', 'calories': 20, 'virya': 'Hot'},
            {'name': 'Light Herbal Tea', 'quantity': '1 cup', 'calories': 5, 'virya': 'Hot'}
        ]
    
    early_morning['total_calories'] = sum(item['calories'] for item in early_morning['items'])
    meals.append(early_morning)
    
    return {
        'meals': meals,
        'total_calories': sum(meal['total_calories'] for meal in meals),
        'constitution_guidelines': get_constitution_guidelines(constitution),
        'seasonal_recommendations': get_seasonal_recommendations(),
        'foods_to_avoid': get_foods_to_avoid(constitution)
    }

def get_constitution_guidelines(constitution):
    """Get dietary guidelines based on constitution"""
    guidelines = {
        'vata': [
            'Eat warm, cooked, and moist foods',
            'Favor sweet, sour, and salty tastes',
            'Maintain regular meal times',
            'Avoid cold, dry, and raw foods',
            'Include healthy oils and ghee'
        ],
        'pitta': [
            'Choose cooling and refreshing foods',
            'Favor sweet, bitter, and astringent tastes',
            'Avoid spicy, fried, and acidic foods',
            'Eat at regular intervals',
            'Include fresh fruits and vegetables'
        ],
        'kapha': [
            'Eat light, warm, and spicy foods',
            'Favor pungent, bitter, and astringent tastes',
            'Avoid heavy, oily, and sweet foods',
            'Maintain active lifestyle',
            'Use warming spices'
        ]
    }
    return guidelines.get(constitution, guidelines['vata'])

def get_seasonal_recommendations():
    """Get seasonal dietary recommendations"""
    current_month = datetime.now().month
    
    if current_month in [12, 1, 2]:  # Winter
        return ['Warming foods', 'Hot beverages', 'Cooked grains', 'Healthy fats']
    elif current_month in [3, 4, 5]:  # Spring
        return ['Light foods', 'Detox drinks', 'Fresh vegetables', 'Minimal oils']
    elif current_month in [6, 7, 8]:  # Summer
        return ['Cooling foods', 'Fresh fruits', 'Coconut water', 'Light meals']
    else:  # Monsoon
        return ['Warm foods', 'Digestive spices', 'Avoid raw foods', 'Herbal teas']

def get_foods_to_avoid(constitution):
    """Get foods to avoid based on constitution"""
    restrictions = {
        'vata': ['Cold foods', 'Raw vegetables', 'Dry foods', 'Excess bitter taste'],
        'pitta': ['Spicy foods', 'Sour foods', 'Fried foods', 'Alcohol', 'Excess heat'],
        'kapha': ['Heavy foods', 'Sweet foods', 'Dairy', 'Fried foods', 'Cold foods']
    }
    return restrictions.get(constitution, [])

def generate_dosha_recommendations(primary_dosha):
    """Generate recommendations based on primary dosha"""
    recommendations = {
        'Vata': {
            'diet': ['Warm, cooked foods', 'Sweet, sour, salty tastes', 'Regular meals'],
            'lifestyle': ['Regular routine', 'Gentle exercise', 'Meditation', 'Warm environment'],
            'herbs': ['Ashwagandha', 'Brahmi', 'Jatamansi']
        },
        'Pitta': {
            'diet': ['Cool, fresh foods', 'Sweet, bitter, astringent tastes', 'Avoid spicy foods'],
            'lifestyle': ['Moderate exercise', 'Cool environment', 'Avoid overwork'],
            'herbs': ['Amla', 'Neem', 'Shatavari']
        },
        'Kapha': {
            'diet': ['Light, warm foods', 'Pungent, bitter, astringent tastes', 'Avoid heavy foods'],
            'lifestyle': ['Vigorous exercise', 'Stimulating activities', 'Warm environment'],
            'herbs': ['Trikatu', 'Guggul', 'Turmeric']
        }
    }
    return recommendations.get(primary_dosha, recommendations['Vata'])
