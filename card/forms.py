from django import forms

class selectclass(forms.Form):
    CHOICE=(  
        ('1', '1 A'),
        ('2', '1 B'),
        ('3', '1 C'),

        ('4', '2 A'),
        ('5', '2 B'),
        ('6', '2 C'),

        ('7', '3 A'),
        ('8', '3 B'),
        ('9', '3 C'),

        ('10', '4 A'),
        ('11', '4 B'),
        ('12', '4 C'),

        ('13', '5 A'),
        ('14', '5 B'),
        ('15', '5 C'),

        ('16', '6 A'),
        ('17', '6 B'),
        ('18', '6 C'),

        ('19', '7 A'),
        ('20', '7 B'),
        ('21', '7 C'),

        ('22', '8 A'),
        ('23', '8 B'),
        ('24', '8 C')
        )

    Class = forms.ChoiceField(required=False,choices=CHOICE,
        widget=forms.Select())

class selectclass2(forms.Form):
    CHOICE=(  
        ('25', '1'),
        ('26', '2'),
        ('27', '3'),
        ('28', '4'),
        ('29', '5'),
        ('30', '6'),
        ('31', '7'),
        ('32', '8'),
                )

    Class = forms.ChoiceField(required=False,choices=CHOICE,
        widget=forms.Select())