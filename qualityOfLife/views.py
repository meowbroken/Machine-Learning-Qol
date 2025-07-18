from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models
import joblib
import os
from django.conf import settings
from .models import StudentInput
from .serializers import StudentInputSerializer


@api_view(['POST'])
def predict_quality_of_life(request):
    # prediction endpoint for quality of life based on student input
    serializer = StudentInputSerializer(data=request.data)
    if serializer.is_valid():
        temp_student = StudentInput(**serializer.validated_data)
        
        try:
            # load ML model and make prediction
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'qol_predictor.pkl')
            model = joblib.load(model_path)
            
            features = prepare_features(temp_student)
            prediction = model.predict([features])[0]
            
            return Response({
                'predicted_qol': round(prediction, 2),
                'input_data': serializer.validated_data,
                'success': True
            }, status=status.HTTP_200_OK)
            
        except FileNotFoundError:
            return Response({
                'error': 'ML model not found. Please train and save the model first.',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                'error': f'Prediction error: {str(e)}',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def prepare_features(student_input):
    # feature extraction from student input
    features = []
    
    # demographic features
    features.append(student_input.age)
    features.append(1 if student_input.gender == 'Male' else 0)
    features.append(student_input.year_level)
    
    # screen time features
    screen_time_mapping = {'<1h': 1, '1-3h': 2, '3-5h': 3, '5-7h': 4, '>7h': 5}
    features.append(screen_time_mapping.get(student_input.screen_time, 0))
    
    # duration before sleep
    duration_mapping = {'no_use' :1,'<15m': 2, '15-30m': 3, '30-60m': 4, '>60m': 5}
    features.append(duration_mapping.get(student_input.duration_before_sleep, 0))
    
    # likert scale features
    likert_mapping = {'Never': 1, 'Rarely': 2, 'Sometimes': 3, 'Often': 4, 'Always': 5}
    features.append(likert_mapping.get(student_input.unintentional_use, 0))
    features.append(likert_mapping.get(student_input.device_during_meals, 0))
    features.append(likert_mapping.get(student_input.device_while_studying, 0))
    
    # control features
    features.append(student_input.control_over_usage)
    features.append(student_input.num_social_platforms)
    
    # yes/no features
    features.append(1 if student_input.device_upon_waking else 0)
    features.append(1 if student_input.attempted_detox else 0)
    features.append(1 if student_input.aware_of_screen_time else 0)
    features.append(1 if student_input.sleep_disruption else 0)
    
    # for usage time
    usage_time_mapping = {'morning': 1, 'afternoon': 2, 'evening': 3, 'late_night': 4, 'throughout': 5}
    features.append(usage_time_mapping.get(student_input.usage_time, 0))
    
    # for main purpose
    features.append(len(student_input.main_purpose) if student_input.main_purpose else 0)
    
    return features


