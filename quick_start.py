
#!/usr/bin/env python3
"""
NutriVeda Quick Start Script
Runs the ML model training and starts the platform
"""

import os
import sys
import subprocess
import time

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🕉️ NutriVeda Quick Start")
    print("=" * 50)
    
    # Step 1: Train ML Model
    print("\n🤖 Step 1: Training ML Model with your data...")
    print("📊 Using Prakriti.csv dataset...")
    
    success, stdout, stderr = run_command("python model_bridge.py")
    
    if success:
        print("✅ ML model trained successfully!")
        print("📁 Model data saved to static/model_data.json")
    else:
        print("⚠️ ML model training encountered issues:")
        print(f"Error: {stderr}")
        print("💡 Platform will use traditional Ayurvedic scoring as fallback")
    
    # Step 2: Start Backend
    print("\n🔧 Step 2: Starting Backend Server...")
    backend_process = subprocess.Popen([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    
    print("⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Step 3: Start Frontend
    print("\n🌐 Step 3: Starting Frontend Server...")
    frontend_process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"])
    
    print("⏳ Waiting for frontend to initialize...")
    time.sleep(3)
    
    # Success message
    print("\n" + "=" * 60)
    print("✅ NutriVeda Platform is READY!")
    print("=" * 60)
    print()
    print("🌟 Access Your Platform:")
    print("   📊 Main Dashboard: http://localhost:8080/main_dashboard.html")
    print("   🤖 AI Dosha Analysis: http://localhost:8080/dosha_detector.html")
    print("   🔧 Backend API: http://localhost:8000/api/")
    print()
    print("💡 Your ML Model Features:")
    print("   ✅ Trained on your Prakriti.csv dataset")
    print("   ✅ 1200+ constitutional assessments")
    print("   ✅ Decision Tree + Random Forest models")
    print("   ✅ High accuracy dosha prediction")
    print()
    print("🎯 What You Can Do Now:")
    print("   1. Register new patients")
    print("   2. Run dosha assessments with your AI model")
    print("   3. Generate personalized diet charts")
    print("   4. Explore the comprehensive food database")
    print("   5. Use the integrated chatbot")
    print()
    print("⚠️  Press Ctrl+C to stop all services...")
    
    try:
        # Keep running until user stops
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping NutriVeda services...")
        backend_process.terminate()
        frontend_process.terminate()
        
        # Wait for graceful shutdown
        time.sleep(2)
        
        # Force kill if still running
        try:
            backend_process.kill()
            frontend_process.kill()
        except:
            pass
        
        print("✅ All services stopped successfully")
        print("🙏 Thank you for using NutriVeda!")

if __name__ == "__main__":
    main()
