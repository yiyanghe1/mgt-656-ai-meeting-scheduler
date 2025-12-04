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


class AbTestEvent(models.Model):
    """Track which variant a visitor saw for the coffee-chatters A/B test."""
    VARIANT_CHOICES = [
        ('kudos', 'Kudos'),
        ('thanks', 'Thanks'),
    ]
    session_key = models.CharField(max_length=40, db_index=True)
    variant = models.CharField(max_length=10, choices=VARIANT_CHOICES)
    user_agent = models.CharField(max_length=255, blank=True)
    ip_address = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'abtest_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.session_key} -> {self.variant} @ {self.created_at}"


class AbTestClickEvent(models.Model):
    """Track button clicks for the coffee-chatters A/B test."""
    session_key = models.CharField(max_length=40, db_index=True)
    variant = models.CharField(max_length=10, choices=AbTestEvent.VARIANT_CHOICES)
    user_agent = models.CharField(max_length=255, blank=True)
    ip_address = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'abtest_click_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"CLICK {self.session_key} -> {self.variant} @ {self.created_at}"

