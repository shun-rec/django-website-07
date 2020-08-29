from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post

from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control" }),
            'body': forms.Textarea(attrs={'class': "form-control" }),
        }

class Index(ListView):
    model = Post
    

class Detail(DetailView):
    model = Post
    

class Create(CreateView):
    model = Post
    form_class = PostForm
    
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["title"] = "新規作成"
        return ctxt


class Update(UpdateView):
    model = Post
    form_class = PostForm
    
    def get_context_data(self):
        ctxt = super().get_context_data()
        ctxt["title"] = "更新"
        return ctxt
        

class Delete(DeleteView):
    model = Post
    success_url = reverse_lazy("index")