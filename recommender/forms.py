from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=64)
    password = forms.CharField(label='password', widget=forms.PasswordInput)


RATING_CHOICES = [(i, i) for i in range(1, 6)]

class RecommendForm(forms.Form):
    #p1 = forms.CharField(label='product1')
    r1 = forms.ChoiceField(label='product1', choices=RATING_CHOICES)
    #p2 = forms.CharField(label='product2')
    r2 = forms.ChoiceField(label='product2', choices=RATING_CHOICES)
    #p3 = forms.CharField(label='product3')
    r3 = forms.ChoiceField(label='product3', choices=RATING_CHOICES)
    #p4 = forms.CharField(label='product4')
    r4 = forms.ChoiceField(label='product4', choices=RATING_CHOICES)
    #p5 = forms.CharField(label='product5')
    r5 = forms.ChoiceField(label='product5', choices=RATING_CHOICES)
