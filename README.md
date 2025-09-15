# 🕉️ NutriVeda - Comprehensive Ayurvedic Nutrition Platform

## Overview

NutriVeda is a comprehensive cloud-based practice management and nutrient analysis software specifically designed for Ayurvedic dietitians. It combines ancient Ayurvedic wisdom with modern technology to provide personalized nutrition recommendations based on individual constitution (Prakriti) and current state (Vikriti).

![NutriVeda Dashboard](https://img.shields.io/badge/Status-Production%20Ready-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Django](https://img.shields.io/badge/Django-4.2+-success) ![License](https://img.shields.io/badge/License-MIT-orange)

## 🌟 Key Features

### 🏥 **Patient Management System**
- **Comprehensive Patient Profiles**: Store detailed information including age, gender, constitution, medical history, dietary preferences, and lifestyle factors
- **BMI Calculation & Health Metrics**: Automatic calculation and tracking of health parameters
- **Constitutional Analysis**: Track patient's Prakriti (natural constitution) and Vikriti (current state)
- **Appointment Scheduling**: Manage consultations and follow-ups

### 🍎 **Comprehensive Food Database**
- **8000+ Food Items**: Extensive database covering Indian, multicultural, and international cuisines
- **Ayurvedic Properties**: Complete nutritional data with Ayurvedic classifications
  - **Rasa** (Six Tastes): Sweet, Sour, Salty, Pungent, Bitter, Astringent
  - **Virya** (Potency): Hot or Cold
  - **Vipaka** (Post-digestive effect)
  - **Guna** (Qualities): Heavy/Light, Oily/Dry, etc.
  - **Dosha Effects**: Impact on Vata, Pitta, and Kapha
- **Seasonal Recommendations**: Foods recommended for different seasons
- **Therapeutic Benefits**: Health benefits and precautions for each food item

### 🤖 **AI-Powered Dosha Analysis**
- **Machine Learning Models**: Trained on 1200+ constitutional assessments
- **Dual Assessment Options**:
  - **Quick Assessment**: 8 key questions (5 minutes)
  - **Comprehensive Analysis**: 20 detailed characteristics (most accurate)
- **Real-time Results**: Instant constitutional analysis with confidence scores
- **Historical Tracking**: Track changes in constitution over time

### 📊 **Automated Diet Chart Generation**
- **Personalized Meal Plans**: Generated based on individual constitution and goals
- **Multiple Goals Support**:
  - Weight Management (Loss/Gain)
  - Therapeutic Healing
  - Digestive Health
  - Detoxification
  - Immunity Boosting
  - General Maintenance
- **Nutritionally Balanced**: Scientifically calculated macro and micronutrients
- **Ayurveda Compliant**: Follows traditional dietary guidelines
- **Customizable Duration**: 7 days to 12 months
- **Meal Timing**: Optimal eating times based on Ayurvedic principles

### 📈 **Advanced Analytics & Reporting**
- **Nutritional Analysis Charts**: Macronutrient distribution, Rasa balance, Dosha effects
- **Progress Tracking**: Monitor patient progress over time
- **Printable Reports**: Professional diet charts and assessment reports
- **Dashboard Analytics**: Real-time statistics and insights

### 🔒 **Security & Compliance**
- **Data Privacy**: HIPAA-compliant patient data handling
- **Secure Authentication**: User authentication and authorization
- **Data Backup**: Automated data backup and recovery
- **Audit Trails**: Complete activity logging

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/your-repo/nutriveda.git
   cd nutriveda
   ```

2. **Run Automated Setup**
   ```bash
   python setup.py
   ```

3. **Start the Platform**
   - **Windows**: Double-click `start_nutriveda.bat`
   - **Linux/Mac**: Run `./start_nutriveda.sh`

4. **Access the Application**
   - **Main Dashboard**: http://localhost:8080/main_dashboard.html
   - **Dosha Detector**: http://localhost:8080/dosha_detector.html
   - **Backend API**: http://localhost:8000/api/

### Manual Setup (Alternative)

1. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train ML Model (Optional)**
   ```bash
   python model_bridge.py
   ```

4. **Start Backend Server**
   ```bash
   python backend/app.py
   ```

5. **Start Frontend Server**
   ```bash
   python -m http.server 8080
   ```

## 🏗️ Architecture

### Technology Stack

#### Frontend
- **HTML5 + CSS3**: Modern responsive design
- **JavaScript (ES6+)**: Dynamic functionality
- **AngularJS 1.x**: Structure and data binding
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icons and graphics

#### Backend
- **Django 4.2+**: Main backend framework
- **Django REST Framework**: API development
- **SQLite/PostgreSQL**: Database management
- **Pandas**: Data processing
- **Scikit-learn**: Machine learning models

#### AI/ML Components
- **Constitutional Analysis**: Rule-based + ML hybrid approach
- **Decision Trees**: For dosha classification
- **Random Forest**: Ensemble method for accuracy
- **Feature Engineering**: 20+ physical and physiological characteristics

### Project Structure
```
nutriveda/
├── main_dashboard.html          # Main application interface
├── dosha_detector.html          # AI-powered constitutional analysis
├── index.html                   # Original prototype (legacy)
├── backend/
│   ├── app.py                   # Django backend server
│   └── apps/                    # Django applications
├── static/
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   └── images/                  # Image assets
├── templates/                   # HTML templates
│   ├── patients.html            # Patient management
│   ├── food-database.html       # Food database interface
│   ├── diet-charts.html         # Diet chart generator
│   └── dosha-analysis.html      # Dosha analysis tools
├── data/                        # Data files and datasets
├── model_bridge.py              # ML model training
├── Prakriti.csv                # Training dataset
├── requirements.txt             # Python dependencies
├── setup.py                     # Automated setup script
└── README.md                    # Documentation
```

## 🎯 Usage Guide

### 1. Patient Registration
1. Navigate to the **Patients** section
2. Click **"Add New Patient"**
3. Fill in comprehensive patient information:
   - Basic details (name, age, gender, contact)
   - Physical parameters (height, weight, BMI)
   - Constitutional information (Prakriti)
   - Lifestyle factors (diet, exercise, sleep)
   - Medical history and current medications
4. Save the patient profile

### 2. Constitutional Analysis
1. Go to **Dosha Analysis** section
2. Choose assessment type:
   - **Quick Assessment**: For basic analysis
   - **Comprehensive Assessment**: For detailed results
3. Answer questions about physical and physiological characteristics
4. Review detailed results with confidence scores
5. Save results to patient profile

### 3. Diet Chart Generation
1. Navigate to **Diet Charts** section
2. Click **"Generate New Chart"**
3. Select patient and set parameters:
   - Treatment goal (weight management, therapeutic, etc.)
   - Target calories and duration
   - Activity level and special considerations
4. Review generated meal plan with:
   - Constitutional guidelines
   - Seasonal recommendations
   - Foods to avoid
   - Nutritional analysis charts
5. Print or download the diet chart

### 4. Food Database Exploration
1. Access **Food Database** section
2. Search foods by name or browse categories
3. View comprehensive information:
   - Nutritional values
   - Ayurvedic properties
   - Dosha effects
   - Seasonal suitability
   - Health benefits and precautions

## 🔧 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### Patients API
```http
GET    /api/patients/           # List all patients
POST   /api/patients/           # Create new patient
GET    /api/patients/{id}/      # Get patient details
PUT    /api/patients/{id}/      # Update patient
DELETE /api/patients/{id}/      # Delete patient
```

#### Food Database API
```http
GET    /api/food-database/      # List foods
GET    /api/food-database/?category=Grains  # Filter by category
GET    /api/food-database/?search=rice      # Search foods
```

#### Diet Charts API
```http
GET    /api/diet-charts/        # List diet charts
POST   /api/diet-charts/        # Generate new chart
GET    /api/diet-charts/{id}/   # Get chart details
```

#### Dosha Assessment API
```http
POST   /api/dosha-assessment/   # Save assessment results
GET    /api/dosha-assessment/   # List assessments
```

### Example API Usage

**Create Patient:**
```json
POST /api/patients/
{
  "name": "John Doe",
  "age": 35,
  "gender": "Male",
  "height": 175,
  "weight": 70,
  "prakriti": "Vata",
  "diet": "Vegetarian"
}
```

**Generate Diet Chart:**
```json
POST /api/diet-charts/
{
  "patient_id": 1001,
  "goal": "Weight Loss",
  "target_calories": 1800,
  "duration": 30,
  "activity_level": "Moderate"
}
```

## 🎨 Customization

### Themes and Styling
- Modify CSS variables in `static/css/` to change colors and appearance
- Update logo and branding in templates
- Customize dashboard layout in `main_dashboard.html`

### Food Database Extension
- Add new food items via the API or directly in `backend/app.py`
- Include complete Ayurvedic properties for each food
- Support for multiple languages and regional cuisines

### Machine Learning Models
- Retrain models with your own dataset using `model_bridge.py`
- Customize assessment questions in `dosha_detector.html`
- Adjust scoring algorithms for constitutional analysis

## 🔌 Integrations

### Hospital Information Systems (HIS)
- REST API endpoints for integration with existing hospital systems
- Standard HL7 FHIR compatibility (planned)
- Electronic Health Records (EHR) synchronization

### Third-party Services
- **Botpress Chatbot**: Integrated AI assistant for patient queries
- **Payment Gateways**: Support for consultation payments
- **SMS/Email**: Automated reminders and notifications
- **Cloud Storage**: AWS S3, Google Cloud integration

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-django

# Run all tests
pytest

# Run specific test categories
pytest tests/test_patients.py
pytest tests/test_diet_charts.py
pytest tests/test_dosha_analysis.py
```

### Test Coverage
- Patient management operations
- Diet chart generation algorithms
- Constitutional analysis accuracy
- API endpoint functionality
- Database operations

## 🚀 Deployment

### Local Development
- Use the provided setup scripts for local development
- SQLite database for quick setup
- Django development server

### Production Deployment

#### Option 1: Cloud Platforms (Recommended)
```bash
# Deploy to Heroku
git push heroku main

# Deploy to AWS/Azure/GCP
# Follow cloud-specific deployment guides
```

#### Option 2: Traditional Server
```bash
# Install production dependencies
pip install gunicorn whitenoise

# Configure for production
export DJANGO_SETTINGS_MODULE=backend.production_settings

# Start with Gunicorn
gunicorn backend.app:application
```

#### Environment Variables
```bash
export DATABASE_URL=postgresql://user:pass@host/db
export SECRET_KEY=your-secret-key
export ALLOWED_HOSTS=yourdomain.com
export DEBUG=False
```

## 📊 Performance

### Optimization Features
- **Lazy Loading**: Load data as needed
- **Caching**: Redis-based caching for frequent queries
- **Database Indexing**: Optimized database queries
- **CDN Integration**: Static asset delivery
- **Compression**: Gzip compression for API responses

### Scalability
- **Horizontal Scaling**: Multi-instance deployment
- **Database Sharding**: Patient data partitioning
- **Microservices**: Modular architecture support
- **Load Balancing**: Multi-server deployment

## 🔐 Security

### Data Protection
- **Encryption**: All sensitive data encrypted at rest and in transit
- **Authentication**: Secure user authentication system
- **Authorization**: Role-based access control
- **Audit Logs**: Complete activity tracking
- **HIPAA Compliance**: Healthcare data protection standards

### Security Best Practices
- Regular security updates
- Penetration testing
- Secure coding practices
- Data backup and recovery
- Privacy by design

## 📞 Support & Community

### Getting Help
- **Documentation**: Comprehensive guides and API docs
- **Issue Tracker**: Report bugs and feature requests
- **Community Forum**: Discussion and knowledge sharing
- **Email Support**: Direct technical support

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Roadmap

### Phase 1 (Current)
- ✅ Core patient management
- ✅ Basic constitutional analysis
- ✅ Diet chart generation
- ✅ Food database integration

### Phase 2 (Next Release)
- 🔄 Advanced ML models
- 🔄 Mobile application
- 🔄 Multilingual support
- 🔄 Integration marketplace

### Phase 3 (Future)
- 📅 IoT device integration
- 📅 Telemedicine features
- 📅 Advanced analytics
- 📅 AI-powered insights

## 📈 Analytics & Insights

### Built-in Analytics
- **Patient Demographics**: Age, gender, constitution distribution
- **Treatment Outcomes**: Success rates and progress tracking
- **Popular Foods**: Most recommended foods by constitution
- **Seasonal Trends**: Dietary preferences by season
- **Consultation Patterns**: Peak hours and frequency analysis

### Custom Reports
- Generate custom reports based on specific criteria
- Export data for external analysis
- Automated report scheduling
- Data visualization dashboards

## 🌍 Localization

### Multi-language Support
- **Hindi**: हिंदी भाषा समर्थन
- **Sanskrit**: संस्कृत श्लोक और मंत्र
- **Regional Languages**: Tamil, Telugu, Bengali, Marathi
- **English**: Default language

### Cultural Adaptation
- Regional food databases
- Local measurement units
- Cultural dietary practices
- Traditional remedies integration

---

## 🙏 Acknowledgments

- **Ancient Ayurvedic Texts**: Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya
- **Modern Research**: Contemporary Ayurvedic research and clinical studies
- **Open Source Community**: Django, scikit-learn, and other open source projects
- **Healthcare Professionals**: Ayurvedic doctors and nutritionists for domain expertise

---

**NutriVeda** - Bridging Ancient Wisdom with Modern Technology for Optimal Health and Nutrition

*© 2024 NutriVeda Platform. All rights reserved.*
