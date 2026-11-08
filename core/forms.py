from django import forms

from .models import GalleryAlbum, HomeHero


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        return [super().clean(item, initial) for item in data if item]


class HomeHeroAdminForm(forms.ModelForm):
    upload_slides = MultipleFileField(
        required=False,
        label="Upload hero images",
        help_text="Select one or more images at once. New uploads are appended to existing slides.",
    )

    class Meta:
        model = HomeHero
        fields = ("title", "body", "button_text", "button_url", "is_published")


class GalleryAlbumAdminForm(forms.ModelForm):
    upload_images = MultipleFileField(
        required=False,
        label="Upload images",
        help_text="Select one or more photos at once (hold Ctrl or Shift to pick multiple).",
    )

    class Meta:
        model = GalleryAlbum
        fields = ("title", "event_date", "slug", "is_published")


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": " ", "autocomplete": "name"}),
        label="Your Name",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": " ", "autocomplete": "email"}),
        label="Your Email",
    )
    phone = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": " ", "autocomplete": "tel", "type": "tel"}
        ),
        label="Phone",
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": " "}),
        label="Subject",
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": " ", "style": "height: 100px"}
        ),
        label="Message",
    )
