# NutriVeda Database Models
from django.db import models
from django.contrib.auth.models import User
import json
import uuid

class Patient(models.Model):
    """Patient model for storing patient information"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    height = models.FloatField(null=True, blank=True)  # in cm
    weight = models.FloatField(null=True, blank=True)  # in kg
    bmi = models.FloatField(null=True, blank=True)
    prakriti = models.CharField(max_length=50, blank=True)
    diet = models.CharField(max_length=50, default='Vegetarian')
    meal_frequency = models.IntegerField(default=3)
    water_intake = models.FloatField(default=2.5)  # liters per day
    activity_level = models.CharField(max_length=20, default='Moderate')
    bowel_movement = models.CharField(max_length=20, default='Regular')
    sleep_hours = models.IntegerField(default=7)
    stress_level = models.CharField(max_length=20, default='Medium')
    medical_history = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    exercise_frequency = models.CharField(max_length=50, blank=True)
    last_visit = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (ID: {self.id})"
    
    def calculate_bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight:
            height_m = self.height / 100
            self.bmi = round(self.weight / (height_m * height_m), 1)
            self.save()
        return self.bmi

class FoodItem(models.Model):
    """Food database model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    calories = models.IntegerField()
    serving = models.CharField(max_length=50)
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField()
    virya = models.CharField(max_length=20)  # Hot/Cold
    digestion = models.CharField(max_length=20)
    rasa = models.CharField(max_length=20)  # Six tastes
    guna = models.CharField(max_length=20)  # Heavy/Light
    vata_effect = models.CharField(max_length=5)  # ↑, ↓, =
    pitta_effect = models.CharField(max_length=5)
    kapha_effect = models.CharField(max_length=5)
    season = models.JSONField(default=list)  # List of seasons
    benefits = models.JSONField(default=list)  # List of benefits
    precautions = models.JSONField(default=list)  # List of precautions
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class DietChart(models.Model):
    """Diet chart model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    goal = models.CharField(max_length=50)
    target_calories = models.IntegerField()
    duration = models.IntegerField()  # days
    chart_data = models.JSONField()  # Store the entire diet chart
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')
    
    def __str__(self):
        return f"Diet Chart for {self.patient.name} - {self.goal}"

class DoshaAssessment(models.Model):
    """Dosha assessment model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    assessment_type = models.CharField(max_length=20, default='comprehensive')
    responses = models.JSONField()  # Store all responses
    primary_dosha = models.CharField(max_length=20)
    dosha_scores = models.JSONField()  # Store individual dosha scores
    confidence = models.FloatField()
    recommendations = models.JSONField()  # Store recommendations
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dosha Assessment - {self.primary_dosha} ({self.confidence:.2f})"
