from django.db import models


class UserDetails(models.Model):
    """
    Model to store user registration and authentication details.
    """
    userID = models.AutoField(primary_key=True, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    google_account = models.CharField(max_length=255)
    first_auth_ts = models.DateTimeField(auto_now_add=True)
    last_auth_ts = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_details'
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.google_account})"

