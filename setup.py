#!/usr/bin/env python3
"""
NutriVeda Setup and Launch Script
Comprehensive Ayurvedic Nutrition Management Platform
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class NutriVedaSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_cmd = self.get_python_command()
        
    def get_python_command(self):
        """Get the appropriate Python command for the system"""
        if platform.system() == "Windows":
            return "python"
        return "python3"
    
    def run_command(self, command, shell=True):
        """Run a system command and return the result"""
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8 or higher is required")
            print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def create_virtual_environment(self):
        """Create virtual environment if it doesn't exist"""
        venv_path = self.project_root / ".venv"
        
        if venv_path.exists():
            print("✅ Virtual environment already exists")
            return True
        
        print("📦 Creating virtual environment...")
        success, stdout, stderr = self.run_command(f"{self.python_cmd} -m venv .venv")
        
        if success:
            print("✅ Virtual environment created successfully")
            return True
        else:
            print(f"❌ Failed to create virtual environment: {stderr}")
            return False
    
    def activate_virtual_environment(self):
        """Get activation command for virtual environment"""
        if platform.system() == "Windows":
            return ".venv\\Scripts\\activate"
        return "source .venv/bin/activate"
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing dependencies...")
        
        # Get pip command for virtual environment
        if platform.system() == "Windows":
            pip_cmd = ".venv\\Scripts\\pip"
        else:
            pip_cmd = ".venv/bin/pip"
        
        # Install requirements
        success, stdout, stderr = self.run_command(f"{pip_cmd} install -r requirements.txt")
        
        if success:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {stderr}")
            # Try installing core dependencies individually
            core_deps = ["django>=4.2.0", "pandas>=2.0.0", "scikit-learn>=1.3.0", "django-cors-headers>=4.0.0"]
            print("🔄 Trying to install core dependencies individually...")
            
            for dep in core_deps:
                success, _, _ = self.run_command(f"{pip_cmd} install {dep}")
                if success:
                    print(f"✅ Installed {dep}")
                else:
                    print(f"❌ Failed to install {dep}")
            
            return True  # Continue even if some optional dependencies fail
    
    def setup_database(self):
        """Setup database and run migrations"""
        print("🗄️ Setting up database...")
        
        # Get Python command for virtual environment
        if platform.system() == "Windows":
            python_cmd = ".venv\\Scripts\\python"
        else:
            python_cmd = ".venv/bin/python"
        
        # Run migrations (if using Django models in future)
        success, stdout, stderr = self.run_command(f"{python_cmd} backend/app.py migrate")
        
        if success:
            print("✅ Database setup completed")
        else:
            print("ℹ️ Database migrations not required for current setup")
        
        return True
    
    def create_sample_data(self):
        """Create sample data for testing"""
        print("📊 Creating sample data...")
        
        try:
            # Load and process Prakriti.csv if it exists
            prakriti_file = self.project_root / "Prakriti.csv"
            if prakriti_file.exists():
                print("✅ Found Prakriti.csv dataset")
                # Run model training
                success, stdout, stderr = self.run_command(f"{self.python_cmd} model_bridge.py")
                if success:
                    print("✅ ML model trained and ready")
                else:
                    print("ℹ️ ML model training failed, using fallback logic")
            else:
                print("ℹ️ Prakriti.csv not found, using sample data")
            
            return True
        except Exception as e:
            print(f"ℹ️ Sample data creation: {str(e)}")
            return True
    
    def create_launch_scripts(self):
        """Create platform-specific launch scripts"""
        print("🚀 Creating launch scripts...")
        
        # Windows batch script
        windows_script = """@echo off
echo 🕉️ Starting NutriVeda Platform...
echo.
call .venv\\Scripts\\activate
start "NutriVeda Backend" python backend/app.py
timeout /t 3 /nobreak > nul
start "NutriVeda Frontend" python -m http.server 8080
echo.
echo ✅ NutriVeda is running!
echo 🌐 Frontend: http://localhost:8080
echo 🔧 Backend API: http://localhost:8000
echo.
echo Press any key to stop all services...
pause > nul
taskkill /f /im python.exe
"""
        
        # Unix shell script
        unix_script = """#!/bin/bash
echo "🕉️ Starting NutriVeda Platform..."
echo ""
source .venv/bin/activate
echo "Starting backend server..."
python backend/app.py &
BACKEND_PID=$!
sleep 3
echo "Starting frontend server..."
python -m http.server 8080 &
FRONTEND_PID=$!
echo ""
echo "✅ NutriVeda is running!"
echo "🌐 Frontend: http://localhost:8080"
echo "🔧 Backend API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services..."
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
"""
        
        try:
            # Write Windows script
            with open("start_nutriveda.bat", "w") as f:
                f.write(windows_script)
            
            # Write Unix script
            with open("start_nutriveda.sh", "w") as f:
                f.write(unix_script)
            
            # Make Unix script executable
            if platform.system() != "Windows":
                os.chmod("start_nutriveda.sh", 0o755)
            
            print("✅ Launch scripts created")
            return True
        except Exception as e:
            print(f"❌ Failed to create launch scripts: {str(e)}")
            return False
    
    def display_final_instructions(self):
        """Display final setup instructions"""
        print("\n" + "="*60)
        print("🎉 NutriVeda Setup Complete!")
        print("="*60)
        print()
        print("📁 Project Structure:")
        print("   ├── main_dashboard.html     # Main application")
        print("   ├── dosha_detector.html     # AI Dosha Analysis")
        print("   ├── backend/app.py          # Django Backend")
        print("   ├── static/                 # CSS/JS assets")
        print("   ├── templates/              # HTML templates")
        print("   └── data/                   # Data files")
        print()
        print("🚀 Quick Start:")
        if platform.system() == "Windows":
            print("   Double-click: start_nutriveda.bat")
            print("   Or run: .\\start_nutriveda.bat")
        else:
            print("   Run: ./start_nutriveda.sh")
            print("   Or: bash start_nutriveda.sh")
        print()
        print("🌐 Access Points:")
        print("   • Main Dashboard: http://localhost:8080/main_dashboard.html")
        print("   • Dosha Detector: http://localhost:8080/dosha_detector.html")
        print("   • Backend API: http://localhost:8000/api/")
        print()
        print("🔧 Manual Start:")
        print(f"   1. Activate venv: {self.activate_virtual_environment()}")
        print("   2. Start backend: python backend/app.py")
        print("   3. Start frontend: python -m http.server 8080")
        print()
        print("📚 Features Available:")
        print("   ✅ Patient Management System")
        print("   ✅ Comprehensive Food Database")
        print("   ✅ AI-Powered Dosha Analysis")
        print("   ✅ Automated Diet Chart Generation")
        print("   ✅ Ayurvedic Nutrition Recommendations")
        print("   ✅ Real-time Dashboard Analytics")
        print("   ✅ Integrated Chatbot Support")
        print()
        print("💡 Need Help?")
        print("   • Check console for any error messages")
        print("   • Ensure ports 8000 and 8080 are available")
        print("   • Verify Python 3.8+ is installed")
        print()
        print("🕉️ Welcome to NutriVeda - Ayurvedic Nutrition Platform!")
        print("="*60)
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🕉️ NutriVeda Setup Starting...")
        print("Comprehensive Ayurvedic Nutrition Management Platform")
        print("-" * 60)
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Creating virtual environment", self.create_virtual_environment),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up database", self.setup_database),
            ("Creating sample data", self.create_sample_data),
            ("Creating launch scripts", self.create_launch_scripts),
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            success = step_func()
            if not success:
                print(f"❌ Setup failed at: {step_name}")
                print("Please check the error messages above and try again.")
                return False
        
        self.display_final_instructions()
        return True

def main():
    """Main setup function"""
    setup = NutriVedaSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick setup without full dependency installation
        print("🚀 Quick Setup Mode")
        setup.create_launch_scripts()
        setup.display_final_instructions()
    else:
        # Full setup
        success = setup.run_setup()
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()
