from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Contact(models.Model):
    """Model to store contact information linked to a user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255,blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)
    postcode = models.CharField(max_length=20,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"


class Telephone(models.Model):
    """Model to store multiple telephone numbers per contact"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="telephones")  
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="telephones")
    number = models.CharField(max_length=20)

    class Meta:
        unique_together = ("user", "number")  

    def __str__(self):
        return f"{self.number} ({self.contact.name})"
