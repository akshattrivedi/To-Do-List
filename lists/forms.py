from django import forms


def widget(placeholder):
    return {"class": "u-full-width", "placeholder": placeholder}


def formContent(widget, label="", max_length=128):
    return {"widget": widget, "label": label, "max_length": max_length}


class TodoForm(forms.Form):
    description = forms.CharField(
        **formContent(widget=forms.TextInput(attrs=widget("Enter TODO Task")))
    )


