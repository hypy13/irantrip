from django.db import models
from django import forms


class SummernoteWidget(forms.Textarea):
    class Media:
        js = (
            'admin/summernote.js',
        )


class SummernoteField(models.TextField):

    def __init__(self, *args, column_type='mediumtext', is_inline=False, **kwargs):
        # specifies column type choices are text | mediumtext | longtext
        # default is mediumtext
        self.is_inline = is_inline
        self.column_type = column_type
        super(SummernoteField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        print(self.is_inline)
        _class = "summernote" if self.is_inline else "summernote"
        kwargs['widget'] = SummernoteWidget(attrs={'class': _class})
        return super().formfield(**{
            'max_length': self.max_length,
            **({} if self.choices is not None else {'widget': forms.Textarea}),
            **kwargs,
        })

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return self.column_type
        elif connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql':
            return 'text'

        return super(SummernoteField, self).db_type(connection)
