from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div
from crispy_forms.bootstrap import FormActions, StrictButton

from django.core.urlresolvers import reverse_lazy

from .models import Post, Comment
from core.models import ACCESSIBILITY_TYPES

CONTENT_TYPE = (
    ('text/html','HTML'),
    ('text/x-markdown','Markdown'),
    ('text/plain','Text'),
)

class CreateCommentForm(forms.ModelForm):

    comment = forms.CharField(
        label = "",
        widget = forms.Textarea(attrs={'rows':5}),
    )

    def __init__(self, *args, **kwargs):
        super(CreateCommentForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'comment',
            FormActions(
                StrictButton("Add Comment", css_class="btn-primary", type="submit"),
            )
        )

    class Meta:
        model = Comment
        fields = ['comment']

class CreatePostForm(forms.ModelForm):

    title = forms.CharField(
        label = "Title",
        max_length=255
    )

    description = forms.CharField(
        label = "Description",
        max_length=255
    )

    content_type = forms.ChoiceField(
        choices = CONTENT_TYPE,
        widget = forms.RadioSelect()
    )

    content = forms.CharField(
        widget = forms.Textarea()
    )

    visibility = forms.ChoiceField(
        choices = ACCESSIBILITY_TYPES
    )

    def __init__(self, *args, **kwargs):
        super(CreatePostForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method= "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.form_action = 'create_post'

        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                'content_type',
                'content',
                'visibility',
            ),
            FormActions (
                StrictButton('Create Post', css_class="btn-primary", type="submit"),
                css_class = 'col-sm-offset-2',
            )
        )

    class Meta:
        model = Post
        fields = ['title','description','content_type','content','visibility']
