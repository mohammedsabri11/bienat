
from django import  forms
from django.forms import ModelForm

from courses.models import Episode
from report.models import Score

from django.forms import ModelForm


class ScoreForm(ModelForm):
    student = forms.ModelChoiceField(
        queryset=None

        , label="الطالبة"
    )


    class Meta:
        model = Score
        include=(("student"),)
        fields = ('num_of_pages','memorizing','review','reading', 'student'
                  )
        labels = {"student":"الطالب",

                  "reading": "درجات التلاوة",
                  "review": "درجات المراجعة",
                  "memorizing":"درجات الحفظ",
                  "num_of_pages": "عدد الاوجة"
                  }

    def __init__(self, *args, **kwargs):
       # print(kwargs)
        #episoded = kwargs.pop('epis_list')
        students = kwargs.pop('student_list')
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = students
        #self.fields['episode'].queryset = episoded
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class EpisodeForm(forms.Form):
    episode = forms.ModelChoiceField(
      #queryset=Episode.objects.none()
        queryset=None

       , label=" رقم الحلقة"
    )

    class Meta:

        fields = ('episode',)



    def __init__(self, epis,*args, **kwargs):
        print(kwargs)
       # epised = kwargs.pop('epis')
        super(EpisodeForm, self).__init__(*args, **kwargs)
        # episoded = args['epis']
        print(epis)
        self.fields['episode'].queryset = epis
        for visible in self.visible_fields():
              visible.field.widget.attrs['class'] = 'form-control'

