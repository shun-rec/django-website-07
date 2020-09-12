# django-website-07

## 完成版プロジェクト

<https://github.com/shun-rec/django-website-07>

## 事前準備

### 新規サーバーを立ち上げる

### 前回モデルを作ったプロジェクトをダウンロード

ターミナルを開いて、以下を実行。

```sh
git clone https://github.com/shun-rec/django-website-06
```

### マイグレートしてDBを作成

```sh
python manage.py migrate
```

### スーパーユーザーを作成

```sh
python manage.py createsuperuser
```

### django shellから以下を実行しカテゴリとタグを作成

#### django shellの起動

```sh
python manage.py shell
```

#### カテゴリとタグとサンプル投稿を作成

django shellで以下をコピーアンドペーストして実行してサンプルデータを作成。

※中身の詳しい解説は前回を見て下さい。

```py
from blog.models import *
cat = Category.objects.create(name="cat 1")
Category.objects.create(name="cat 2")
tag1 = Tag.objects.create(name="tag 1")
tag2 = Tag.objects.create(name="tag 2")
Tag.objects.create(name="tag 3")
post = Post()
post.title = "post 1"
post.body = "body 1"
post.category = cat
post.save()
post.tags.add(tag1)
post.tags.add(tag2)
post.save()
exit
```

## 記事一覧と個別ページを作ろう

### Viewの作成

`blog/views.py`

```py
# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView

# 一覧
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

# 個別
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post
```

### Templateの作成

#### Bootstrapを取り込んだベースTemplateを作成

Bootstrapについては[こちら](https://getbootstrap.com/docs/4.0/getting-started/introduction/)。  
CSSを自分で書かなくても簡単に見た目を整えられる「CSSフレームワーク」。

※フォルダがない場合は作成

`blog/templates/blog/base.html`

```html
<!doctype HTML>
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="/">匿名ブログ</a>
        </nav>
        <div class="container mt-4">
        {% block main %}
        <p>※コンテンツがありません。</p>
        {% endblock %}
        </div>
    </body>
</html>
```

#### 一覧（トップ）ページのTemplateを作成

※ListViewはこの名前でテンプレートを探すのでこの名前でないとダメ。

`blog/templates/blog/post_list.html`

```html
{% extends "blog/base.html" %}
{% block main %}
<h2>記事一覧</h2>
<ol>
    {% for post in object_list %}
    <li><a href="#">{{ post.title }}</a></li>
    {% endfor %}
</ol>
{% endblock %}
```

#### 個別（詳細）ページのTemplateを作成

※DetailViewはこの名前でテンプレートを探すのでこの名前でないとダメ

`blog/templates/blog/post_detail.html`

```html
{% extends "blog/base.html" %}
{% load l10n %}
{% block main %}
<h2>{{ object.title }}</h2>
<p><time>{{ object.updated|localize }}</time></p>
<div>
    {{ object.body }}
</div>
{% endblock %}
```

#### URLを設定

##### BlogアプリのURL設定

`blog/urls.py`

```py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('detail/<pk>/', views.Detail.as_view(), name="detail"),
]
```

##### 全体設定のURL設定

`pj_blog/urls.py`

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blog.urls")),
]
```

#### 一覧記事に記事へのリンクを設定

`blog/templates/blog/post_list.html`の6行目を以下に変更

```html
<li><a href="{% url 'detail' post.id %}">{{ post.title }}</a></li>
```

## 6-3 CreateViewで新規作成画面を作ろう

### CreateViewのひな形

```py
from django.views.generic.edit import CreateView

class Create(CreateView):
    model = Post
    fields = ["title", "body"]
```

### モデルの個別ページのURL設定

```py
from django.urls import reverse_lazy

class Post(models.Model):
    # 略
    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])
```


## 6-4 UpdateViewとDeleteViewで編集・削除画面を作ろう


### UpdateViewのひな形

```py
from django.views.generic.edit import UpdateView

class Update(UpdateView):
    model = Post
    fields = ["title", "body"]
```

### DeleteViewのひな形

```py
from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post
    success_url = "/"
```

## 6-5 CreateViewのフォームをカスタマイズしよう

```py
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control" }),
            'body': forms.Textarea(attrs={'class': "form-control" }),
        }
```
