from django import forms
from .models import UserAdmin,HomeInfo,ContentCreator,Types,Style,TargetAudience
from django.contrib.auth.forms import UserCreationForm

from django.forms import formset_factory

class DateInput(forms.DateInput):
    input_type = 'date'

class AdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'style': 'max-width: 20em'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'style': 'max-width: 20em'})
    class Meta:
        model = UserAdmin
        fields =('fname','lname','username','email','birthdate','gender','is_admin','is_staff','password1','password2')

        widgets={
                'fname':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'lname':forms.TextInput(attrs={'class':'form-control','style':'max-width: 20em',"id":"","placeholder":""}),
                'email':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'username':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"placeholder":""}),
                'birthdate':DateInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":"29/09/1996"}),
                'gender': forms.Select(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'is_admin': forms.CheckboxInput(attrs={'class':'form-check-input ','style':' margin-left:20px',"id":"","placeholder":""}),
                'is_staff': forms.CheckboxInput(attrs={'class':'form-check-input ','style':' margin-left:20px',"id":"","placeholder":""}),
          }  
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'   
        
   

class HomeInfoForm(forms.ModelForm):
    class Meta:
        model = HomeInfo
        fields = ('title','image','description','title_ar_field','description_ar_field','background')

        
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
            'description':forms.Textarea(attrs={'class':'form-control','style':'width:70%'}),
            'title_ar_field':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
            'description_ar_field':forms.Textarea(attrs={'class':'form-control','style':'width:70%'}),
            'image':forms.FileInput(attrs={'class':'form-control','style':'width:70%'}),
            'background':forms.FileInput(attrs={'class':'form-control','style':'width:70%'}),


    }




class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','name':'password'}))




class ContentCreatorForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Content Subject'}))
    purpose = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Content Purpose'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Content Message'}))
    word_count = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Content Word Counts'}))
    target_audience = forms.ModelChoiceField(
        queryset=TargetAudience.objects.all(),
        empty_label='select target audience',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    style = forms.ModelChoiceField(
        queryset=Style.objects.all(),
        empty_label='select a style',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    types = forms.ModelChoiceField(
        queryset=Types.objects.all(),
        empty_label='select a type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ContentCreator
        fields = ('subject', 'purpose', 'message', 'word_count', 'target_audience', 'style', 'types')