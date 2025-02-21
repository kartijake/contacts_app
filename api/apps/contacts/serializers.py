from rest_framework import serializers
from .models import Contact, Telephone
import re
class TelephoneSerializer(serializers.ModelSerializer):
    """Serializer for telephone numbers"""

    class Meta:
        model = Telephone
        fields = ["number"]

    def validate_number(self, value):
        """Ensure the telephone number is numeric and correctly formatted"""
        request = self.context.get("request")
        contact = self.context.get("contact")  
        user = request.user if request else None

        if not re.match(r"^[0-9\-\+\(\) ]+$", value):
            raise serializers.ValidationError("Invalid telephone number format. Allowed characters: digits, +, -, (, ), and spaces.")

        # Ensure length is reasonable
        if len(value) < 7 or len(value) > 15:
            raise serializers.ValidationError("Telephone number must be between 7 and 15 characters long.")

        if not user or not contact:
            return value 


        return value

class ContactSerializer(serializers.ModelSerializer):
    """Serializer for contact creation"""
    
    telephones = TelephoneSerializer(many=True)  

    class Meta:
        model = Contact
        fields = ["id","name", "address_line_1", "address_line_2", "city", "country", "postcode", "telephones"]
    
    def validate_telephones(self, value):
        """Ensure no duplicate numbers in the request, but allow existing ones linked to the contact"""
        request = self.context.get("request")
        print("init")
        if not request:
            return value

        user = request.user
        contact = self.instance  # Get the existing contact if updating

        numbers_in_request = [entry["number"] for entry in value]

        # Check for duplicate numbers in the same request
        if len(numbers_in_request) != len(set(numbers_in_request)):
            raise serializers.ValidationError("Duplicate telephone numbers are not allowed in the same request.")

        # Check if numbers already exist in another contact for this user
        existing_numbers = Telephone.objects.filter(user=user, number__in=numbers_in_request)
        for phone in existing_numbers:
            if phone.contact != contact:  # Allow numbers already linked to this contact
                raise serializers.ValidationError(f"The number {phone.number} is already linked to another contact.")

        return value
    
    def create(self, validated_data):
        """Create a contact and related telephone numbers"""
        telephones_data = validated_data.pop("telephones")
        user = self.context["request"].user  # Get user from request
        contact = Contact.objects.create(user=user, **validated_data)

        for phone_data in telephones_data:
            Telephone.objects.create(user=user, contact=contact, **phone_data)

        return contact
    

    
    def update(self, instance, validated_data):
        """Handle updates for contacts and their telephone numbers"""
        telephones_data = validated_data.pop("telephones", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


        user = instance.user
        existing_numbers = set(instance.telephones.values_list("number", flat=True))
        new_numbers = []
        for phone_data in telephones_data:
            number = phone_data["number"]
            if number in existing_numbers:
                continue  
            new_numbers.append(Telephone(user=user, contact=instance, number=number))

        Telephone.objects.bulk_create(new_numbers)

        return instance
    