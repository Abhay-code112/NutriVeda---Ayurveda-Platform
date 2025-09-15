#!/usr/bin/env python3
"""
Script to add food items from Book1.csv to the Food Database
"""

import csv
import json

def get_ayurvedic_properties(food_name, category):
    """Assign Ayurvedic properties based on food characteristics"""
    
    # Basic categorization
    food_lower = food_name.lower()
    
    # Determine category
    if any(word in food_lower for word in ['leaves', 'leaf', 'green', 'spinach', 'coriander', 'mint']):
        category = 'Vegetables'
        virya = 'Cold'
        rasa = 'Bitter'
        guna = 'Light'
        vata = '↑'
        pitta = '↓'
        kapha = '↓'
    elif any(word in food_lower for word in ['apple', 'fruit', 'mango', 'banana', 'orange', 'grape']):
        category = 'Fruits'
        virya = 'Cold'
        rasa = 'Sweet'
        guna = 'Light'
        vata = '↓'
        pitta = '↓'
        kapha = '↑'
    elif any(word in food_lower for word in ['fish', 'chicken', 'meat', 'egg']):
        category = 'Proteins'
        virya = 'Hot'
        rasa = 'Sweet'
        guna = 'Heavy'
        vata = '↓'
        pitta = '↑'
        kapha = '↑'
    elif any(word in food_lower for word in ['almond', 'nut', 'cashew', 'walnut']):
        category = 'Nuts'
        virya = 'Cold'
        rasa = 'Sweet'
        guna = 'Heavy'
        vata = '↓'
        pitta = '↓'
        kapha = '↑'
    elif any(word in food_lower for word in ['rice', 'wheat', 'barley', 'oats', 'millet']):
        category = 'Grains'
        virya = 'Cold'
        rasa = 'Sweet'
        guna = 'Light'
        vata = '↓'
        pitta = '↓'
        kapha = '↑'
    else:
        category = 'Other'
        virya = 'Neutral'
        rasa = 'Sweet'
        guna = 'Light'
        vata = '='
        pitta = '='
        kapha = '='
    
    # Season determination
    if any(word in food_lower for word in ['mango', 'watermelon', 'cucumber']):
        season = ['Summer']
    elif any(word in food_lower for word in ['apple', 'pomegranate', 'dates']):
        season = ['Winter']
    else:
        season = ['All']
    
    # Benefits and precautions
    if 'leaves' in food_lower or 'leaf' in food_lower:
        benefits = ['Rich in vitamins', 'Detoxifying', 'High in fiber']
        precautions = ['Use in moderation', 'May cause gas if consumed excessively']
    elif 'fish' in food_lower:
        benefits = ['High protein', 'Omega-3 fatty acids', 'Complete amino acids']
        precautions = ['Avoid if allergic', 'Consume fresh']
    elif 'almond' in food_lower or 'nut' in food_lower:
        benefits = ['Brain health', 'Heart healthy', 'Rich in minerals']
        precautions = ['High in calories', 'Use in moderation']
    else:
        benefits = ['Nutritious', 'Natural food']
        precautions = ['Consume in moderation']
    
    return {
        'virya': virya,
        'rasa': rasa,
        'guna': guna,
        'vata': vata,
        'pitta': pitta,
        'kapha': kapha,
        'season': season,
        'benefits': benefits,
        'precautions': precautions
    }

def parse_food_data():
    """Parse Book1.csv and create food database entries"""
    
    food_items = []
    current_id = 100  # Start from 100 to avoid conflicts
    
    try:
        with open('Book1.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            for row_num, row in enumerate(reader):
                if row_num == 0:  # Skip header
                    continue
                
                if len(row) < 3 or not row[0] or row[0] == '-':
                    continue
                
                food_name = row[0].strip()
                if not food_name or food_name == '-':
                    continue
                
                # Extract nutritional data (simplified)
                try:
                    calories = float(row[2]) if row[2] and row[2] != '' else 0
                    protein = float(row[4]) if len(row) > 4 and row[4] and row[4] != '' else 0
                    fat = float(row[5]) if len(row) > 5 and row[5] and row[5] != '' else 0
                    carbs = float(row[6]) if len(row) > 6 and row[6] and row[6] != '' else 0
                    fiber = float(row[7]) if len(row) > 7 and row[7] and row[7] != '' else 0
                except (ValueError, IndexError):
                    calories = protein = fat = carbs = fiber = 0
                
                # Get Ayurvedic properties
                ayurvedic = get_ayurvedic_properties(food_name, '')
                
                # Create food item
                food_item = {
                    'id': current_id,
                    'name': food_name,
                    'category': ayurvedic.get('category', 'Other'),
                    'calories': round(calories, 1),
                    'serving': '100g',
                    'protein': round(protein, 1),
                    'carbs': round(carbs, 1),
                    'fat': round(fat, 1),
                    'fiber': round(fiber, 1),
                    'virya': ayurvedic['virya'],
                    'digestion': 'Easy' if 'leaves' in food_name.lower() or 'fruit' in food_name.lower() else 'Moderate',
                    'rasa': ayurvedic['rasa'],
                    'guna': ayurvedic['guna'],
                    'vata': ayurvedic['vata'],
                    'pitta': ayurvedic['pitta'],
                    'kapha': ayurvedic['kapha'],
                    'season': ayurvedic['season'],
                    'benefits': ayurvedic['benefits'],
                    'precautions': ayurvedic['precautions']
                }
                
                food_items.append(food_item)
                current_id += 1
                
                # Limit to first 50 items for now
                if len(food_items) >= 50:
                    break
    
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    
    return food_items

def update_food_database():
    """Update the food database in app.js"""
    
    # Parse new food items
    new_foods = parse_food_data()
    
    if not new_foods:
        print("No food items found to add")
        return
    
    print(f"Found {len(new_foods)} food items to add")
    
    # Read current app.js
    try:
        with open('static/js/app.js', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the foodDatabase array start
        start_marker = '$scope.foodDatabase = ['
        start_idx = content.find(start_marker)
        
        if start_idx == -1:
            print("Could not find foodDatabase array in app.js")
            return
        
        # Find the end of the current array
        bracket_count = 0
        end_idx = start_idx + len(start_marker)
        
        for i in range(end_idx, len(content)):
            if content[i] == '[':
                bracket_count += 1
            elif content[i] == ']':
                bracket_count -= 1
                if bracket_count == -1:
                    end_idx = i
                    break
        
        # Create new food database content
        new_foods_json = json.dumps(new_foods, indent=8)
        
        # Replace the food database
        new_content = content[:start_idx + len(start_marker)] + '\n' + new_foods_json[1:-1] + '\n    ];'
        
        # Write back to file
        with open('static/js/app.js', 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"Successfully added {len(new_foods)} food items to the database!")
        print("Food items added:")
        for food in new_foods[:10]:  # Show first 10
            print(f"  - {food['name']} ({food['category']})")
        
        if len(new_foods) > 10:
            print(f"  ... and {len(new_foods) - 10} more items")
            
    except Exception as e:
        print(f"Error updating app.js: {e}")

if __name__ == "__main__":
    print("🍎 Adding food items from Book1.csv to Food Database...")
    update_food_database()
    print("✅ Food database updated successfully!")
