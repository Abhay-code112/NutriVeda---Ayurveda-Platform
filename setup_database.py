#!/usr/bin/env python3
"""
Database Setup Script for NutriVeda
Creates database tables and migrates existing data
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

# Import models after Django setup
from backend.models import Patient, FoodItem, DietChart, DoshaAssessment

def create_tables():
    """Create database tables"""
    print("🗄️ Creating database tables...")
    
    # Create migrations
    execute_from_command_line(['manage.py', 'makemigrations', 'backend'])
    
    # Apply migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Database tables created successfully!")

def migrate_sample_data():
    """Migrate sample data to database"""
    print("📊 Migrating sample data...")
    
    # Sample patients
    sample_patients = [
        {
            'name': 'Raj Kumar',
            'age': 35,
            'gender': 'Male',
            'phone': '+91-9876543210',
            'email': 'raj.kumar@email.com',
            'height': 175,
            'weight': 70,
            'bmi': 22.9,
            'prakriti': 'Vata',
            'diet': 'Vegetarian',
            'meal_frequency': 3,
            'water_intake': 3.0,
            'activity_level': 'Moderate',
            'bowel_movement': 'Regular',
            'sleep_hours': 7,
            'stress_level': 'Medium',
            'medical_history': 'Anxiety, digestive issues',
            'current_medications': 'None',
            'allergies': 'None',
            'occupation': 'Software Engineer',
            'exercise_frequency': '3 times/week'
        },
        {
            'name': 'Priya Sharma',
            'age': 28,
            'gender': 'Female',
            'phone': '+91-9876543211',
            'email': 'priya.sharma@email.com',
            'height': 165,
            'weight': 58,
            'bmi': 21.3,
            'prakriti': 'Pitta',
            'diet': 'Vegetarian',
            'meal_frequency': 4,
            'water_intake': 3.5,
            'activity_level': 'High',
            'bowel_movement': 'Regular',
            'sleep_hours': 6,
            'stress_level': 'High',
            'medical_history': 'Acidity, skin sensitivity',
            'current_medications': 'Antacid',
            'allergies': 'Dairy',
            'occupation': 'Marketing Manager',
            'exercise_frequency': '5 times/week'
        }
    ]
    
    # Create sample patients
    for patient_data in sample_patients:
        patient, created = Patient.objects.get_or_create(
            name=patient_data['name'],
            defaults=patient_data
        )
        if created:
            print(f"✅ Created patient: {patient.name}")
        else:
            print(f"ℹ️ Patient already exists: {patient.name}")
    
    # Sample food items
    sample_foods = [
        {
            'name': 'Basmati Rice',
            'category': 'Grains',
            'calories': 205,
            'serving': '100g cooked',
            'protein': 4.3,
            'carbs': 45,
            'fat': 0.4,
            'fiber': 0.6,
            'virya': 'Cold',
            'digestion': 'Easy',
            'rasa': 'Sweet',
            'guna': 'Light',
            'vata_effect': '↓',
            'pitta_effect': '↓',
            'kapha_effect': '↑',
            'season': ['All'],
            'benefits': ['Easy digestion', 'Cooling effect', 'Energy providing'],
            'precautions': ['May increase Kapha if consumed excessively'],
            'description': 'High-quality aromatic rice, ideal for daily consumption'
        },
        {
            'name': 'Moong Dal',
            'category': 'Proteins',
            'calories': 347,
            'serving': '100g raw',
            'protein': 24,
            'carbs': 63,
            'fat': 1.2,
            'fiber': 16,
            'virya': 'Cold',
            'digestion': 'Easy',
            'rasa': 'Sweet',
            'guna': 'Light',
            'vata_effect': '↓',
            'pitta_effect': '↓',
            'kapha_effect': '=',
            'season': ['All'],
            'benefits': ['Complete protein', 'Easy to digest', 'Detoxifying'],
            'precautions': ['None for most people'],
            'description': 'Excellent source of plant protein, perfect for all constitutions'
        },
        {
            'name': 'Ghee',
            'category': 'Dairy',
            'calories': 900,
            'serving': '1 tbsp (15g)',
            'protein': 0,
            'carbs': 0,
            'fat': 15,
            'fiber': 0,
            'virya': 'Cold',
            'digestion': 'Easy',
            'rasa': 'Sweet',
            'guna': 'Heavy',
            'vata_effect': '↓',
            'pitta_effect': '↓',
            'kapha_effect': '↑',
            'season': ['Winter', 'Summer'],
            'benefits': ['Improves digestion', 'Enhances absorption', 'Nourishing'],
            'precautions': ['Use in moderation', 'Avoid in obesity'],
            'description': 'Clarified butter, considered nectar in Ayurveda'
        }
    ]
    
    # Create sample food items
    for food_data in sample_foods:
        food, created = FoodItem.objects.get_or_create(
            name=food_data['name'],
            defaults=food_data
        )
        if created:
            print(f"✅ Created food item: {food.name}")
        else:
            print(f"ℹ️ Food item already exists: {food.name}")
    
    print("✅ Sample data migration completed!")

def main():
    """Main setup function"""
    print("🕉️ NutriVeda Database Setup")
    print("=" * 50)
    
    try:
        # Create database tables
        create_tables()
        
        # Migrate sample data
        migrate_sample_data()
        
        print("\n" + "=" * 50)
        print("✅ Database setup completed successfully!")
        print("=" * 50)
        print("📊 Summary:")
        print(f"   Patients: {Patient.objects.count()}")
        print(f"   Food Items: {FoodItem.objects.count()}")
        print(f"   Diet Charts: {DietChart.objects.count()}")
        print(f"   Dosha Assessments: {DoshaAssessment.objects.count()}")
        print("\n🚀 Your NutriVeda platform now has persistent data storage!")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
