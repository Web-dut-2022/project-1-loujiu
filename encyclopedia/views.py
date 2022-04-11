import random
import markdown
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from . import util


class NewEntry(forms.Form):
    topic = forms.CharField(
        error_messages={
            'required': 'This title is required.'
        },
        widget=widgets.Textarea(attrs={'class': 'btn1'})
    )
    content = forms.CharField(
        error_messages={
            'required': 'This content is required.'
        },
        widget=widgets.Textarea(attrs={'class': 'btn2'}),
    )

    def clean_content(self):
        t = self.cleaned_data.get('topic')
        ans = util.get_entry(t)
        if ans:
            raise ValidationError("Entry with this name is already exists.")
        else:
            return t


class EditEntry(forms.Form):
    content = forms.CharField(
        error_messages={
            'required': 'This content is required.'
        },
        widget=widgets.Textarea(attrs={'class': 'btn2'}),
    )


def index(request):
    """
    结合一个给定的模板和一个给定的上下文字典
    并返回一个渲染后的HttpResponse对象。
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "encyclopedia",
        "topic": "All Pages"
    })


def sublist(subs):
    old_list = util.list_entries()
    new_list = [i for i in old_list if subs in i]
    return new_list


@csrf_exempt
def create_entry(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            topic = form.cleaned_data.get('topic')
            content = form.cleaned_data.get('content')
            util.save_entry(topic, content)
            return redirect("/wiki/" + topic)
        else:
            return render(request, "encyclopedia/new.html", {
                "form_obj": form
            })
    else:
        form = NewEntry()
        return render(request, "encyclopedia/new.html", {
            "form_obj": form
        })


def show_entry(request, topic):
    answer = util.get_entry(topic)
    if not answer:
        return render(request, "encyclopedia/entry.html", {
            "content": "Wikipedia does not have an article with this exact name.",
            "title": topic
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown.markdown(answer),
            "title": topic
        })


@csrf_exempt
def search(request):
    ctx = {}
    if request.method == "POST":
        topic = request.POST['q']
        answer = util.get_entry(topic)
        if answer:
            return redirect("/wiki/" + topic)
        else:
            new_list = sublist(topic)
            ctx["entries"] = new_list
            ctx["title"] = topic
            ctx["topic]"] = topic
            return render(request, "encyclopedia/index.html", ctx)


@csrf_exempt
def edit(request, topic):
    if request.method == "POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            util.save_entry(topic, content)
            return redirect("/wiki/" + topic)
        else:
            return render(request, "encyclopedia/edit.html", {
                "form_obj": form
            })
    else:
        form = EditEntry(initial={'content': util.get_entry(topic)})
        return render(request, "encyclopedia/edit.html", {
            "form_obj": form,
            "topic": topic
        })


def random_entry(request):
    entry_list = util.list_entries()
    topic = random.choice(entry_list)
    return redirect("/wiki/" + topic)
