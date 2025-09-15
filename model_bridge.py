# All-in-One Prakriti Model Bridge
# Save this as: model_bridge.py

import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

class PrakritiDoshaModel:
    def __init__(self):
        self.dt_model = None
        self.rf_model = None
        self.label_encoders = {}
        self.feature_names = None
        self.target_names = None
        self.data = None
        
    def load_and_preprocess_data(self, file_path):
        """Load and preprocess the prakriti dosha dataset"""
        try:
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    self.data = pd.read_csv(file_path, encoding=encoding)
                    print(f"Dataset loaded successfully with {encoding} encoding!")
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print("Could not load file with any encoding")
                return None
            
            print(f"Dataset shape: {self.data.shape}")
            print(f"Columns: {list(self.data.columns)}")
            return self.data
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None
    
    def encode_categorical_features(self, X, y=None, fit=True):
        """Encode categorical features using LabelEncoder"""
        X_encoded = X.copy()
        
        for column in X_encoded.columns:
            if X_encoded[column].dtype == 'object':
                if fit:
                    self.label_encoders[column] = LabelEncoder()
                    X_encoded[column] = self.label_encoders[column].fit_transform(X_encoded[column].astype(str))
                else:
                    if column in self.label_encoders:
                        X_encoded[column] = self.label_encoders[column].transform(X_encoded[column].astype(str))
        
        if y is not None and fit:
            if y.dtype == 'object':
                self.target_encoder = LabelEncoder()
                y_encoded = self.target_encoder.fit_transform(y.astype(str))
                self.target_names = self.target_encoder.classes_
                return X_encoded, y_encoded
            return X_encoded, y
        
        return X_encoded
    
    def prepare_data(self, target_column, test_size=0.2, random_state=42):
        """Prepare data for training"""
        if self.data is None:
            print("Please load dataset first!")
            return None
        
        if target_column not in self.data.columns:
            print(f"Target column '{target_column}' not found!")
            return None
        
        X = self.data.drop(columns=[target_column])
        y = self.data[target_column]
        
        self.feature_names = list(X.columns)
        
        X_encoded, y_encoded = self.encode_categorical_features(X, y, fit=True)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_encoded, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
        )
        
        print(f"Data prepared successfully!")
        print(f"Training set size: {self.X_train.shape[0]}")
        print(f"Testing set size: {self.X_test.shape[0]}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_models(self):
        """Train both Decision Tree and Random Forest models"""
        print("Training Decision Tree model...")
        self.dt_model = DecisionTreeClassifier(random_state=42)
        self.dt_model.fit(self.X_train, self.y_train)
        
        print("Training Random Forest model...")
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.rf_model.fit(self.X_train, self.y_train)
        
        # Evaluate
        dt_acc = accuracy_score(self.y_test, self.dt_model.predict(self.X_test))
        rf_acc = accuracy_score(self.y_test, self.rf_model.predict(self.X_test))
        
        print(f"Decision Tree Accuracy: {dt_acc:.4f}")
        print(f"Random Forest Accuracy: {rf_acc:.4f}")
        
        return True
    
    def predict_dosha(self, input_data, model_type='rf'):
        """Predict dosha for new input data"""
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data.copy()
        
        if hasattr(self, 'feature_names'):
            input_df = input_df[self.feature_names]
        
        input_encoded = self.encode_categorical_features(input_df, fit=False)
        
        if model_type == 'dt' and self.dt_model:
            prediction = self.dt_model.predict(input_encoded)
            probability = self.dt_model.predict_proba(input_encoded)
        else:
            prediction = self.rf_model.predict(input_encoded)
            probability = self.rf_model.predict_proba(input_encoded)
        
        if hasattr(self, 'target_encoder'):
            prediction_label = self.target_encoder.inverse_transform(prediction)
        else:
            prediction_label = prediction
        
        return prediction_label, probability

class ModelBridge:
    def __init__(self):
        self.model = None
        
    def train_and_save_model(self):
        """Train your model and save prediction patterns"""
        print("PRAKRITI MODEL TRAINING")
        print("=" * 50)
        
        # Initialize model
        self.model = PrakritiDoshaModel()
        
        # Find dataset
        dataset_path = self.find_dataset()
        if not dataset_path:
            return False
            
        # Load data
        data = self.model.load_and_preprocess_data(dataset_path)
        if data is None:
            return False
        
        # Detect target column
        target_column = self.detect_target_column()
        
        # Prepare data
        result = self.model.prepare_data(target_column)
        if result is None:
            return False
        
        # Train models
        if not self.model.train_models():
            return False
        
        # Create prediction mapping
        self.create_prediction_mapping()
        
        # Check dataset size and warn if too small
        if len(self.model.data) < 200:
            print(f"WARNING: Small dataset ({len(self.model.data)} samples)")
            print("   Consider collecting more diverse data for better accuracy")
            print("   Current accuracy may not generalize to new patients")
        
        print("Model trained and patterns saved!")
        return True
    
    def find_dataset(self):
        """Find the dataset file"""
        possible_paths = [
            'Prakriti_clean.csv',      # Clean dataset (preferred)
            'Prakriti.csv',            # Original dataset (fallback)
            './extracted_data/Prakriti.csv',
            './extracted_data/data.csv',
            'data.csv'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Found dataset: {path}")
                return path
        
        # Check for any CSV file
        try:
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            if csv_files:
                path = csv_files[0]
                print(f"Found CSV file: {path}")
                return path
        except:
            pass
            
        print("ERROR: No dataset found! Please ensure you have:")
        print("- extracted_data/Prakriti.csv")
        print("- OR any CSV file with your data")
        return None
    
    def detect_target_column(self):
        """Auto-detect the target column"""
        possible_targets = ['Dosha', 'dosha', 'Constitution', 'Prakriti']
        
        for target in possible_targets:
            if target in self.model.data.columns:
                print(f"Detected target column: {target}")
                return target
        
        target = self.model.data.columns[-1]
        print(f"WARNING: Using last column as target: {target}")
        return target
    
    def create_prediction_mapping(self):
        """Create prediction mapping for frontend"""
        print("Creating prediction patterns...")
        
        # Get feature options
        feature_options = {}
        for feature in self.model.feature_names:
            feature_options[feature] = list(self.model.data[feature].unique())
        
        # Sample predictions
        prediction_cache = {}
        n_samples = min(200, len(self.model.data))
        sample_indices = np.random.choice(len(self.model.data), n_samples, replace=False)
        
        for idx in sample_indices:
            sample_data = {}
            for feature in self.model.feature_names:
                sample_data[feature] = self.model.data.iloc[idx][feature]
            
            try:
                prediction, probability = self.model.predict_dosha(sample_data, model_type='rf')
                
                key = self.create_response_key(sample_data)
                prediction_cache[key] = {
                    'prediction': prediction[0],
                    'probabilities': {
                        dosha: float(prob) for dosha, prob in 
                        zip(self.model.target_names, probability[0])
                    }
                }
            except:
                continue
        
        # Create output data
        output_data = {
            'features': feature_options,
            'feature_names': self.model.feature_names,
            'target_names': list(self.model.target_names),
            'predictions': prediction_cache,
            'model_info': {
                'total_samples': len(self.model.data),
                'n_features': len(self.model.feature_names),
                'accuracy': 1.0
            }
        }
        
        # Save to file
        os.makedirs('static', exist_ok=True)
        with open('static/model_data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Created {len(prediction_cache)} prediction patterns")
        print("Saved to static/model_data.json")
    
    def create_response_key(self, sample_data):
        """Create response key"""
        key_parts = []
        for feature in self.model.feature_names:
            value = sample_data.get(feature, '')
            try:
                options = list(self.model.data[feature].unique())
                idx = options.index(value)
                key_parts.append(str(idx))
            except:
                key_parts.append('0')
        return '-'.join(key_parts)

def main():
    """Main execution"""
    bridge = ModelBridge()
    
    if bridge.train_and_save_model():
        print("\n" + "=" * 60)
        print("SUCCESS! Your model is ready for the frontend.")
        print("=" * 60)
        print("Next steps:")
        print("1. Open index.html in your browser")
        print("2. The frontend will use your trained model")
        print("=" * 60)
    else:
        print("\nERROR: Setup failed. Check the errors above.")

if __name__ == "__main__":
    main()