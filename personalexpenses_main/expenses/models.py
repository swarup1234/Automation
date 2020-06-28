from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class expense(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=4, default =0)
    paymentdate = models.DateTimeField(null=True, blank = True)
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # image = models.ImageField(upload_to='portfolio/images/')
    # url = models.URLField(blank=True)

    def __str__(self):
        return self.title