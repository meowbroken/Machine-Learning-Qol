from django.db import models


class StudentInput(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    SCREEN_TIME_CHOICES = [
        ('<1h', 'Less than 1 hour'),
        ('1-3h', '1–3 hours'),
        ('3-5h', '3–5 hours'),
        ('5-7h', '5–7 hours'),
        ('>7h', 'More than 7 hours'),
    ]
    DURATION_CHOICES = [
        ('no_use', "I don't use a device before sleeping"),
        ('<15m', 'Less than 15 minutes'),
        ('15-30m', '15–30 minutes'),
        ('30-60m', '30–60 minutes'),
        ('>60m', 'More than 1 hour'),
    ]
    LIKERT_CHOICES = [
        ('Never', 'Never'),
        ('Rarely', 'Rarely'),
        ('Sometimes', 'Sometimes'),
        ('Often', 'Often'),
        ('Always', 'Always'),
    ]
    USAGE_TIMES = [
        ('morning (6am - 12pm)', 'Morning'),
        ('afternoon (12pm - 6pm)', 'Afternoon'),
        ('evening(6pm - 10pm)', 'Evening'),
        ('late_night(10pm - 3am)', 'Late Night'),
        ('throughout', 'Throughout the day'),
    ]

    PURPOSE_CHOICES = [
        ('Social Media', 'Social Media'),
        ('Messaging and Communication', 'Messaging and Communication'),
        ('Schoolwork / Studying', 'Schoolwork / Studying'),
        ('Streaming', 'Streaming'),
        ('Gaming', 'Gaming'),
        ('Reading / Research', 'Reading / Research'),
        ('Online Shopping', 'Online Shopping'),
        ('Work-related tasks', 'Work-related tasks'),
    ]

    YEAR_LEVEL_CHOICES = [
        (7, 'Grade 7'),
        (8, 'Grade 8'),
        (9, 'Grade 9'),
        (10, 'Grade 10'),
        (11, 'Grade 11'),
        (12, 'Grade 12'),
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
        (5, '5th Year'),
    ]

    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    course = models.CharField(max_length=100, help_text="For JHS students: 'JHS'. For college: Track/Program (e.g., 'ICT', 'BSCS')")
    year_level = models.PositiveSmallIntegerField(choices=YEAR_LEVEL_CHOICES)

    screen_time = models.CharField(max_length=10, choices=SCREEN_TIME_CHOICES)
    duration_before_sleep = models.CharField(max_length=10, choices=DURATION_CHOICES)
    main_purpose = models.JSONField()  # Store list of PURPOSE_CHOICES
    unintentional_use = models.CharField(max_length=10, choices=LIKERT_CHOICES)
    device_during_meals = models.CharField(max_length=10, choices=LIKERT_CHOICES)
    control_over_usage = models.PositiveSmallIntegerField()
    device_while_studying = models.CharField(max_length=10, choices=LIKERT_CHOICES)
    device_upon_waking = models.BooleanField()
    num_social_platforms = models.PositiveSmallIntegerField()
    attempted_detox = models.BooleanField()
    aware_of_screen_time = models.BooleanField()
    usage_time = models.CharField(max_length=25, choices=USAGE_TIMES)
    sleep_disruption = models.BooleanField()

    predicted_qol = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

