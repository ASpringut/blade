from django.forms import Form, CharField, PasswordInput, EmailField, DecimalField, ModelChoiceField, ValidationError
from inventory.models import Restaurant

class RegisterForm(Form):
    username = CharField(max_length=30)
    Password = CharField(widget=PasswordInput())
    Repeat_Password = CharField(widget= PasswordInput())
    Restaurant_Name = CharField()
    E_mail = EmailField(label='E-mail')
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        
        pass1 = cleaned_data.get('Password')
        pass2 = cleaned_data.get('Repeat_Password')
        
        #check that passwords match
        if pass1 and pass2:
            if pass1 != pass2:
                raise ValidationError("Passwords do not match.")
        
        rest = cleaned_data.get('Restaurant_Name')
        #check that restaurant does not already exist
        if rest:
            print(len(Restaurant.objects.filter(name=rest)))
            if len(Restaurant.objects.filter(name=rest))!=0:
                raise ValidationError("Restaurant already exists.")
    
        # Always return the full collection of cleaned data.
        return cleaned_data
        
class LoginForm(Form):
    username = CharField(max_length=30)
    Password = CharField(widget=PasswordInput())
    