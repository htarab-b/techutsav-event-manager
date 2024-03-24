from django.db import models

# Choices
Yes_No_Choices = (
    ("YES", "YES"),
    ("NO", "NO"),
    ("SPOT", "SPOT"),
)

# Create your models here.
class Participant(models.Model):
    Phone = models.CharField(max_length=15)
    Event = models.CharField(max_length=55)
    Teammate1 = models.CharField(max_length=55, null=True, blank=True)
    Teammate2 = models.CharField(max_length=55, null=True, blank=True)
    Teammate3 = models.CharField(max_length=55, null=True, blank=True)
    Teammate4 = models.CharField(max_length=55, null=True, blank=True)
    Teammate5 = models.CharField(max_length=55, null=True, blank=True)
    Teammate6 = models.CharField(max_length=55, null=True, blank=True)
    Teammate7 = models.CharField(max_length=55, null=True, blank=True)
    Teammate8 = models.CharField(max_length=55, null=True, blank=True)
    Teammate9 = models.CharField(max_length=55, null=True, blank=True)
    Teammate10 = models.CharField(max_length=55, null=True, blank=True)
    College = models.CharField(max_length=155)
    Degree = models.CharField(max_length=55)
    Year = models.CharField(max_length=25)
    Registered = models.CharField(max_length=5, choices=Yes_No_Choices, default="NO")
    def __str__(self):
        return self.Teammate1 + " - " + self.Event + " (" + self.Phone + ")"