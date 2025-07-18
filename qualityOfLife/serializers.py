from rest_framework import serializers
from .models import StudentInput


class StudentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInput
        fields = '__all__'
        read_only_fields = ('predicted_qol', 'created_at')

    def validate_age(self, value):
        if value < 12 or value > 35:
            raise serializers.ValidationError("Age must be between 12 and 35")
        return value

    def validate_year_level(self, value):
        valid_levels = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]
        if value not in valid_levels:
            raise serializers.ValidationError("Year level must be 7-12 (Grade 7-12) or 1-5 (1st-5th Year)")
        return value

    def validate(self, data):
        year_level = data.get('year_level')
        course = data.get('course', '').strip()
        
    
        if year_level in [7, 8, 9, 10, 11, 12]:
            if course.upper() != 'JHS':
                raise serializers.ValidationError({
                    'course': 'For Junior High School students, course should be "JHS"'
                })
        
        elif year_level in [1, 2, 3, 4, 5]:
            if course.upper() == 'JHS' or not course:
                raise serializers.ValidationError({
                    'course': 'For college students, specify track/program (e.g., "ICT", "BSCS")'
                })
        
        return data

    def validate_control_over_usage(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Control over usage must be between 1 and 10")
        return value

    def validate_num_social_platforms(self, value):
        if value < 0 or value > 20:
            raise serializers.ValidationError("Number of social platforms must be between 0 and 20")
        return value

    def validate_main_purpose(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Main purpose must be a list")
        
        valid_purposes = [choice[0] for choice in StudentInput.PURPOSE_CHOICES]
        for purpose in value:
            if purpose not in valid_purposes:
                raise serializers.ValidationError(f"Invalid purpose: {purpose}")
        
        return value