// NutriVeda - Comprehensive Ayurvedic Nutrition Platform
// Angular Application with complete functionality

angular.module('nutrivedaApp', [])
.controller('MainController', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {

    // Initialize scope variables
    $scope.activeTab = 'dashboard';
    $scope.patients = [];
    $scope.dietCharts = [];
    $scope.todayAppointments = 5;
    $scope.showNewPatientForm = false;
    $scope.showNewDietChart = false;
    $scope.newPatient = {};
    $scope.generatedChart = null;

    // Food Database (Sample Data - In production, this would come from backend)
    $scope.foodDatabase = [
            {
                id: 1,
            name: "Basmati Rice",
            category: "Grains",
            calories: 205,
            serving: "100g cooked",
            protein: 4.3,
            carbs: 45,
            fat: 0.4,
            virya: "Cold",
            digestion: "Easy",
            rasa: "Sweet",
            vata: "↓",
            pitta: "↓",
            kapha: "↑"
        },
        {
            id: 2,
            name: "Moong Dal",
            category: "Proteins",
            calories: 347,
            serving: "100g raw",
            protein: 24,
            carbs: 63,
            fat: 1.2,
            virya: "Cold",
            digestion: "Easy",
            rasa: "Sweet",
            vata: "↓",
            pitta: "↓",
            kapha: "="
        },
        {
            id: 3,
            name: "Ghee",
            category: "Dairy",
            calories: 900,
            serving: "100g",
            protein: 0,
            carbs: 0,
            fat: 100,
            virya: "Cold",
            digestion: "Easy",
            rasa: "Sweet",
            vata: "↓",
            pitta: "↓",
            kapha: "↑"
        },
        {
            id: 4,
            name: "Spinach",
            category: "Vegetables",
            calories: 23,
            serving: "100g raw",
            protein: 2.9,
            carbs: 3.6,
            fat: 0.4,
            virya: "Cold",
            digestion: "Easy",
            rasa: "Bitter",
            vata: "↑",
            pitta: "↓",
            kapha: "↓"
        },
        {
            id: 5,
            name: "Ginger",
            category: "Spices",
            calories: 80,
            serving: "100g",
            protein: 1.8,
            carbs: 18,
            fat: 0.8,
            virya: "Hot",
            digestion: "Easy",
            rasa: "Pungent",
            vata: "↓",
            pitta: "↑",
            kapha: "↓"
        },
        {
            id: 6,
            name: "Turmeric",
            category: "Spices",
            calories: 354,
            serving: "100g",
            protein: 7.8,
            carbs: 65,
            fat: 9.9,
            virya: "Hot",
            digestion: "Easy",
            rasa: "Bitter",
            vata: "↓",
            pitta: "↑",
            kapha: "↓"
        },
        {
            id: 7,
            name: "Apple",
            category: "Fruits",
            calories: 52,
            serving: "100g",
            protein: 0.3,
            carbs: 14,
            fat: 0.2,
            virya: "Cold",
            digestion: "Easy",
            rasa: "Sweet",
            vata: "↓",
            pitta: "↓",
            kapha: "↑"
        },
        {
            id: 8,
            name: "Almonds",
            category: "Proteins",
            calories: 579,
            serving: "100g",
            protein: 21,
            carbs: 22,
            fat: 50,
            virya: "Hot",
            digestion: "Hard",
            rasa: "Sweet",
            vata: "↓",
            pitta: "↑",
            kapha: "↑"
        }
    ];

    // Sample Patients Data
    $scope.patients = [
        {
            id: 1001,
            name: "Raj Kumar",
            age: 35,
            gender: "Male",
            prakriti: "Vata",
            diet: "Vegetarian",
            lastVisit: "2025-09-05",
            height: 175,
            weight: 70,
            mealFrequency: 3,
            waterIntake: 3,
            bowelMovement: "Regular"
        },
        {
            id: 1002,
            name: "Priya Sharma",
            age: 28,
            gender: "Female",
            prakriti: "Pitta",
            diet: "Vegetarian",
            lastVisit: "2025-09-08",
            height: 165,
            weight: 58,
            mealFrequency: 4,
            waterIntake: 3.5,
            bowelMovement: "Regular"
        }
    ];

    // Recent Activities
    $scope.recentActivities = [
        { description: "New patient registered: Raj Kumar", time: "2 hours ago" },
        { description: "Diet chart created for Priya Sharma", time: "5 hours ago" },
        { description: "Dosha assessment completed", time: "1 day ago" },
        { description: "Food database updated", time: "2 days ago" }
    ];

    // Functions
    $scope.setActiveTab = function(tab) {
        $scope.activeTab = tab;
        if (tab === 'dosha') {
            $timeout(function() {
                loadDoshaDetector();
            }, 100);
        }
    };

    $scope.addPatient = function() {
        if ($scope.newPatient.name) {
            // Send patient data to backend API
            $http.post('http://localhost:8000/api/patients/', $scope.newPatient)
                .then(function(response) {
                    if (response.data.success) {
                        // Reload patients from backend to ensure sync
                        $scope.loadData();

                        // Add to recent activities
                        $scope.recentActivities.unshift({
                            description: "New patient registered: " + $scope.newPatient.name,
                            time: "Just now"
                        });

                        // Reset form
                        $scope.newPatient = {};
                        $scope.showNewPatientForm = false;
                        
                        // Show success message
                        alert("Patient registered successfully!");
                    } else {
                        alert("Failed to register patient: " + response.data.error);
                    }
                })
                .catch(function(error) {
                    console.error('Error adding patient:', error);
                    alert("Failed to register patient. Please try again.");
                });
        } else {
            alert("Please fill in the patient name.");
        }
    };

    $scope.generateNewDietChart = function() {
        $scope.showNewDietChart = true;
        $scope.targetCalories = 2000;
        $scope.chartDuration = 30;
        $scope.dietChartGoal = "Maintenance";
    };

    $scope.createDietChartForPatient = function() {
        // Debug: Log available patients and selected ID
        console.log('Available patients:', $scope.patients);
        console.log('Selected patient ID:', $scope.selectedPatientId);
        
        // Find the selected patient
        $scope.selectedPatientForChart = $scope.patients.find(p => p.id == $scope.selectedPatientId);
        
        console.log('Found patient:', $scope.selectedPatientForChart);
        
        if ($scope.selectedPatientForChart) {
            // Create diet chart data for backend
            const dietChartData = {
                patient_id: $scope.selectedPatientId,
                goal: $scope.dietChartGoal,
                target_calories: $scope.targetCalories,
                duration: $scope.chartDuration,
                activity_level: $scope.activityLevel || 'Moderate'
            };

            // Send to backend
            console.log('Sending diet chart data:', dietChartData);
            $http.post('http://localhost:8000/api/diet-charts/', dietChartData)
                .then(function(response) {
                    console.log('Diet chart response:', response.data);
                    if (response.data.success) {
                        $scope.generatedChart = response.data.data.chart_data;
                        
                        // Add to diet charts
                        $scope.dietCharts.push(angular.copy(response.data.data));

                        // Add to recent activities
                        $scope.recentActivities.unshift({
                            description: "Diet chart created for " + $scope.selectedPatientForChart.name,
                            time: "Just now"
                        });

                        // Reset form
                        $scope.showNewDietChart = false;
                        $scope.selectedPatientId = null;
                        $scope.selectedPatientForChart = null;

                        // Show success message
                        alert("Diet chart generated successfully!");
                    } else {
                        alert("Error generating diet chart: " + response.data.error);
                    }
                })
                .catch(function(error) {
                    console.error('Error creating diet chart:', error);
                    console.error('Error details:', error.data);
                    alert("Failed to generate diet chart. Please try again. Error: " + (error.data ? error.data.error : error.message));
                });
        } else {
            alert("Please select a patient first!");
        }
    };
    $scope.deletePatient = function(patient) {
        if (confirm("Are you sure you want to delete " + patient.name + "?")) {
            var index = $scope.patients.indexOf(patient);
            $scope.patients.splice(index, 1);
            
            // Add to recent activities
            $scope.recentActivities.unshift({
                description: "Patient deleted: " + patient.name,
                time: "Just now"
            });
        }
    };

    $scope.deleteDietChart = function(chart) {
        if (confirm("Are you sure you want to delete this diet chart?")) {
            // Call backend API to delete the chart
            $http({
                method: 'DELETE',
                url: 'http://localhost:8000/api/diet-charts/',
                data: { chart_id: chart.id },
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(function(response) {
                if (response.data.success) {
                    // Remove from local array
                    var index = $scope.dietCharts.indexOf(chart);
                    $scope.dietCharts.splice(index, 1);
                    
                    // Add to recent activities
                    $scope.recentActivities.unshift({
                        description: "Diet chart deleted for " + chart.patientName,
                        time: "Just now"
                    });
                    
                    alert("Diet chart deleted successfully!");
                } else {
                    alert("Error deleting diet chart: " + response.data.error);
                }
            })
            .catch(function(error) {
                console.error('Error deleting diet chart:', error);
                alert("Failed to delete diet chart. Please try again.");
            });
        }
    };

    $scope.searchFood = function() {
        if ($scope.foodSearchTerm) {
            $scope.filteredFoods = $scope.foodDatabase.filter(function(food) {
                return food.name.toLowerCase().includes($scope.foodSearchTerm.toLowerCase()) ||
                       food.category.toLowerCase().includes($scope.foodSearchTerm.toLowerCase());
            });
        } else {
            $scope.filteredFoods = $scope.foodDatabase;
        }
        // Reset pagination when searching
        $scope.currentPage = 1;
        $scope.displayedFoods = [];
        $scope.loadMoreFoods();
    };

    // Pagination functions
    $scope.loadMoreFoods = function() {
        var startIndex = ($scope.currentPage - 1) * $scope.itemsPerPage;
        var endIndex = startIndex + $scope.itemsPerPage;
        var newItems = $scope.filteredFoods.slice(startIndex, endIndex);
        
        if ($scope.currentPage === 1) {
            $scope.displayedFoods = newItems;
        } else {
            $scope.displayedFoods = $scope.displayedFoods.concat(newItems);
        }
        
        $scope.currentPage++;
    };

    $scope.hasMoreFoods = function() {
        var totalDisplayed = $scope.displayedFoods.length;
        var totalFiltered = $scope.filteredFoods.length;
        return totalDisplayed < totalFiltered;
    };

    $scope.resetFoodDisplay = function() {
        $scope.currentPage = 1;
        $scope.displayedFoods = [];
        $scope.loadMoreFoods();
    };

    $scope.filterByCategory = function(category) {
        $scope.selectedFoodCategory = category;
        if (category === '') {
            $scope.filteredFoods = $scope.foodDatabase;
        } else {
            $scope.filteredFoods = $scope.foodDatabase.filter(function(food) {
                return food.category === category;
            });
        }
        $scope.resetFoodDisplay();
    };

    // BMI Calculation Functions
    $scope.calculateBMI = function() {
        if ($scope.newPatient.height && $scope.newPatient.weight) {
            var heightInMeters = $scope.newPatient.height / 100;
            var bmi = $scope.newPatient.weight / (heightInMeters * heightInMeters);
            $scope.newPatient.bmi = Math.round(bmi * 10) / 10; // Round to 1 decimal place
            
            // Add BMI category
            var bmiCategory = $scope.getBMICategory($scope.newPatient.bmi);
            $scope.newPatient.bmiCategory = bmiCategory.text;
        } else {
            $scope.newPatient.bmi = null;
            $scope.newPatient.bmiCategory = null;
        }
    };

    $scope.getBMICategory = function(bmi) {
        if (bmi < 18.5) return {text: 'Underweight', class: 'text-info'};
        if (bmi >= 18.5 && bmi < 25) return {text: 'Normal', class: 'text-success'};
        if (bmi >= 25 && bmi < 30) return {text: 'Overweight', class: 'text-warning'};
        return {text: 'Obese', class: 'text-danger'};
    };

    // Watch for changes in height or weight
    $scope.$watch('newPatient.height', function() {
        $scope.calculateBMI();
    });

    $scope.$watch('newPatient.weight', function() {
        $scope.calculateBMI();
    });

    // Load food database with filters
    $scope.loadFoodDatabase = function(category, search) {
        var url = 'http://localhost:8000/api/food-database/';
        var params = {};
        
        if (category) params.category = category;
        if (search) params.search = search;
        
        if (Object.keys(params).length > 0) {
            url += '?' + Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&');
        }
        
        $http.get(url)
            .then(function(response) {
                if (response.data.success && response.data.data) {
                    $scope.foodDatabase = response.data.data;
                    $scope.filteredFoods = $scope.foodDatabase;
                    console.log('Loaded ' + response.data.total + ' food items');
                }
            })
            .catch(function(error) {
                console.error('Error loading food database:', error);
            });
    };

    // Initialize filtered foods and pagination
    $scope.filteredFoods = $scope.foodDatabase;
    $scope.displayedFoods = [];
    $scope.currentPage = 1;
    $scope.itemsPerPage = 20;
    $scope.totalItems = 0;
    $scope.selectedFoodCategory = '';

    // Load data from backend
    $scope.loadData = function() {
        // Load patients from backend
        $http.get('http://localhost:8000/api/patients/')
            .then(function(response) {
                if (response.data.success && response.data.data) {
                    $scope.patients = response.data.data;
                }
            })
            .catch(function(error) {
                console.error('Error loading patients:', error);
            });

        // Load diet charts from backend
        $http.get('http://localhost:8000/api/diet-charts/')
            .then(function(response) {
                if (response.data.success && response.data.data) {
                    $scope.dietCharts = response.data.data;
                }
            })
            .catch(function(error) {
                console.error('Error loading diet charts:', error);
            });

        // Load food database from backend
        $http.get('http://localhost:8000/api/food-database/')
            .then(function(response) {
                if (response.data.success && response.data.data) {
                    $scope.foodDatabase = response.data.data;
                    $scope.filteredFoods = $scope.foodDatabase;
                    $scope.totalItems = response.data.total;
                    $scope.loadMoreFoods(); // Load first batch
                    console.log('Loaded ' + response.data.total + ' food items from backend');
                }
            })
            .catch(function(error) {
                console.error('Error loading food database:', error);
                // Keep using sample data if backend fails
                $scope.loadMoreFoods();
            });
    };

    // Initialize data
    $scope.loadData();
    
    // Chart.js integration for diet charts
    $scope.charts = {};

    $scope.initializeCharts = function() {
        if (!$scope.generatedChart) return;

        // Clean up existing charts
        $scope.cleanupCharts();

        // Macronutrient Chart (Doughnut)
        const nutrientCtx = document.getElementById('nutrientChart');
        if (nutrientCtx) {
            $scope.charts.nutrientChart = new Chart(nutrientCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Protein', 'Carbs', 'Fat'],
                    datasets: [{
                        data: [15, 65, 20],
                        backgroundColor: ['#FF6B35', '#25A18E', '#004E64'],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        title: {
                            display: true,
                            text: 'Macronutrient Distribution'
                        }
                    }
                }
            });
        }

        // Rasa Distribution Chart (Radar)
        const rasaCtx = document.getElementById('rasaChart');
        if (rasaCtx) {
            $scope.charts.rasaChart = new Chart(rasaCtx, {
                type: 'radar',
                data: {
                    labels: ['Sweet', 'Sour', 'Salty', 'Pungent', 'Bitter', 'Astringent'],
                    datasets: [{
                        label: 'Rasa Distribution',
                        data: [40, 10, 5, 15, 20, 10],
                        backgroundColor: 'rgba(255, 107, 53, 0.2)',
                        borderColor: '#FF6B35',
                        borderWidth: 2,
                        pointBackgroundColor: '#FF6B35'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 50
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Six Tastes Balance'
                        }
                    }
                }
            });
        }

        // Dosha Balance Chart (Bar)
        const doshaCtx = document.getElementById('doshaChart');
        if (doshaCtx) {
            $scope.charts.doshaChart = new Chart(doshaCtx, {
                type: 'bar',
                data: {
                    labels: ['Vata', 'Pitta', 'Kapha'],
                    datasets: [{
                        label: 'Dosha Balance',
                        data: [50, 30, 50],
                        backgroundColor: ['#667eea', '#ff6b6b', '#28a745'],
                        borderWidth: 1,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Dosha Balance'
                        }
                    }
                }
            });
        }
    };

    $scope.cleanupCharts = function() {
        Object.keys($scope.charts).forEach(key => {
            if ($scope.charts[key]) {
                $scope.charts[key].destroy();
                delete $scope.charts[key];
            }
        });
    };

    $scope.exportChartData = function() {
        if ($scope.generatedChart) {
            const dataStr = JSON.stringify($scope.generatedChart, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'diet-chart-' + $scope.generatedChart.patientName + '.json';
            link.click();
            URL.revokeObjectURL(url);
        }
    };

    // Initialize charts when diet chart is generated
    $scope.$watch('generatedChart', function(newVal) {
        if (newVal) {
            $timeout(function() {
                $scope.initializeCharts();
            }, 100);
        }
    });

    // Additional functions for diet chart management
    $scope.downloadPDF = function() {
        if ($scope.generatedChart) {
            // Simple PDF generation - in production, use a proper PDF library
            const printWindow = window.open('', '_blank');
            const content = `
                <html>
                    <head><title>Diet Chart - ${$scope.generatedChart.patientName}</title></head>
                    <body>
                        <h1>Diet Chart for ${$scope.generatedChart.patientName}</h1>
                        <p>Goal: ${$scope.generatedChart.goal}</p>
                        <p>Calories: ${$scope.generatedChart.calories}</p>
                        <p>Duration: ${$scope.generatedChart.duration} days</p>
                        <p>Generated on: ${new Date().toLocaleDateString()}</p>
                    </body>
                </html>
            `;
            printWindow.document.write(content);
            printWindow.document.close();
            printWindow.print();
        }
    };

    $scope.shareChart = function() {
        if ($scope.generatedChart) {
            const shareText = `Check out this personalized diet chart for ${$scope.generatedChart.patientName} created with NutriVeda!`;
            if (navigator.share) {
                navigator.share({
                    title: 'Diet Chart',
                    text: shareText,
                    url: window.location.href
                });
            } else {
                // Fallback to clipboard
                navigator.clipboard.writeText(shareText + ' ' + window.location.href);
                alert('Chart details copied to clipboard!');
            }
        }
    };

    $scope.viewChart = function(chart) {
        $scope.generatedChart = chart;
        $scope.setActiveTab('diet-charts');
    };

    $scope.duplicateChart = function(chart) {
        if (confirm('Create a copy of this diet chart?')) {
            const newChart = angular.copy(chart);
            newChart.id = Date.now(); // Simple ID generation
            newChart.createdDate = new Date().toISOString().split('T')[0];
            $scope.dietCharts.push(newChart);
            
            // Add to recent activities
            $scope.recentActivities.unshift({
                description: "Diet chart duplicated for " + chart.patientName,
                time: "Just now"
            });
            
            alert('Diet chart duplicated successfully!');
        }
    };

    $scope.editChart = function(chart) {
        // Set the chart as the current generated chart for editing
        $scope.generatedChart = chart;
        $scope.showNewDietChart = true;
        $scope.setActiveTab('diet-charts');
        
        // Pre-fill form with existing data
        $scope.selectedPatientId = chart.patientId;
        $scope.dietChartGoal = chart.goal;
        $scope.targetCalories = chart.calories;
        $scope.chartDuration = chart.duration;
    };

    // Patient management functions
    $scope.viewPatient = function(patient) {
        alert(`Patient Details:\nName: ${patient.name}\nAge: ${patient.age}\nGender: ${patient.gender}\nPrakriti: ${patient.prakriti}\nDiet: ${patient.diet}\nLast Visit: ${patient.lastVisit}`);
    };

    $scope.createDietChart = function(patient) {
        $scope.selectedPatientId = patient.id;
        $scope.setActiveTab('diet-charts');
        $scope.generateNewDietChart();
    };

    $scope.editPatient = function(patient) {
        // Pre-fill the new patient form with existing data for editing
        $scope.newPatient = angular.copy(patient);
        $scope.showNewPatientForm = true;
        $scope.setActiveTab('patients');
        
        // Calculate BMI for existing patient data
        $scope.calculateBMI();
    };

    // Dosha analysis functions
    $scope.viewAssessment = function(assessment) {
        alert(`Dosha Assessment:\nPatient: ${assessment.patientName}\nVata: ${assessment.vataScore}\nPitta: ${assessment.pittaScore}\nKapha: ${assessment.kaphaScore}\nDominant Dosha: ${assessment.dominantDosha}`);
    };

    $scope.generateDietFromDosha = function(assessment) {
        // Create a diet chart based on dosha assessment
        $scope.selectedPatientId = assessment.patientId;
        $scope.dietChartGoal = "Dosha Balance";
        $scope.setActiveTab('diet-charts');
        $scope.generateNewDietChart();
        
        // Add to recent activities
        $scope.recentActivities.unshift({
            description: "Diet chart generated from dosha assessment for " + assessment.patientName,
            time: "Just now"
        });
    };

}]);

// Load Dosha Detector
function loadDoshaDetector() {
    // This function loads the dosha detector functionality
    console.log("Dosha Detector loaded");
}
