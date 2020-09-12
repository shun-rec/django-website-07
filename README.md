# djangoチュートリアル #7

前回まででViewとTemplateとModelすべてを説明したので、DB上のデータをウェブサイトに表示するために必要な要素はすべて揃っています。  
それらを自分で組み合わせても1からウェブサイトを作ることも出来ます。  
しかし、ウェブサイトでよくあるパターンはdjangoの方ですでに用意されています。  
今回はよくあるパターンである一覧・個別・作成・編集・削除という機能をdjangoを最大限に活用して少ないコードで作っていきます。

## 完成版プロジェクト

<https://github.com/shun-rec/django-website-07>

## 事前準備

### 新規サーバーを立ち上げる

### 前回モデルを作ったプロジェクトをダウンロード

ターミナルを開いて、以下を実行。

```sh
git clone https://github.com/shun-rec/django-website-06
```

フォルダを移動

```sh
cd django-website-06
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

# ListViewは一覧を簡単に作るためのView
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

# DetailViewは詳細を簡単に作るためのView
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

### URLを設定

#### BlogアプリのURL設定

`blog/urls.py`

```py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    
    # <pk>にPostのIDを渡すと表示される。
    path('detail/<pk>/', views.Detail.as_view(), name="detail"),
]
```

#### 全体設定のURL設定

`pj_blog/urls.py`

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blog.urls")),
]
```

### 一覧記事に記事へのリンクを設定

`blog/templates/blog/post_list.html`の6行目を以下に変更

```html
<li><a href="{% url 'detail' post.id %}">{{ post.title }}</a></li>
```

### 動かしてみよう

最初に作ったサンプル投稿が一覧に表示されているはずです。  
一覧をクリックすると個別ページに移動します。

## ブログの新規投稿画面を作ろう

### Viewの作成

`blog/views.py`に以下を追記

```py
from django.views.generic.edit import CreateView

# CreateViewは新規作成画面を簡単に作るためのView
class Create(CreateView):
    model = Post
    
    # 編集対象にするフィールド
    fields = ["title", "body", "category", "tags"]
```

### Templateの作成

* `Post`用の投稿フォームが`{{ form.as_p }}`で自動的に生成されます。
* `{% csrf_token %}`はセキュリティ上form内に必ず必要な決り文句。

※CreateViewはこの名前でテンプレートを探すのでこの名前でないとダメ

`blog/templates/blog/post_form.html`

```html
{% extends "blog/base.html" %}

{% block main %}
<h2>新規投稿</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="投稿" class="btn btn-primary" />
</form>
{% endblock %}
```

### URLの設定

`blog/urls.py`のdetailのURL設定の下に以下を追加。

```py
path('create/', views.Create.as_view(), name="create"),
```

### トップページからリンクを貼る

`blog/templates/blog/post_list.html`

`</ol>`の次の行に以下を追記。

```html
<p><a href="{% url 'create' %}">新規投稿</a></p>
```

### モデルの個別ページのURL設定

デフォルトでは新規投稿したあとに、自動で投稿したばかりのページに移動します。  
なので、各投稿のURLを知らせる必要があります。

`blog/models.py`の`Post`モデルに、`import`と`get_absolute_url`メソッドを追記。

```py
from django.urls import reverse_lazy

class Post(models.Model):
    # 略
    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])
```

### 動ごかしてみよう

トップページから新規投稿ページを開いて、投稿を追加できればOKです。

## 投稿編集画面を作ろう

### Viewの作成

```py
from django.views.generic.edit import UpdateView

class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]
```

### Templateの作成

※UpdateViewはデフォルトでCreateViewと同じTemplateを使うので必要なし！

### URLの設定

`blog/urls.py`

`create`の次に以下を追記。

```py
    path('update/<pk>', views.Update.as_view(), name="update"),
```

### 個別ページからリンクを貼る

`blog/templates/blog/post_detail.html`

`{% endblock %}`の上に以下を追記。

```html
<p><a href="{% url 'update' object.pk %}">編集</a></p>
```

### 動かしてみよう

個別ページから編集ボタンを押して、その投稿を編集出来ればOKです。

## 投稿削除画面を作ろう

### Viewの作成

```py
from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post
    
    # 削除したあとに移動する先（トップページ）
    success_url = "/"
```

### Templateの作成

※DetailViewはこの名前でテンプレートを探すのでこの名前でないとダメ

`blog/templates/blog/post_confirm_delete.html`

```html
{% extends "blog/base.html" %}

{% block main %}
<h2>削除確認</h2>
<p>{{ object.title }}を本当に削除してもよろしいですか？</p>
<form method="post">
    {% csrf_token %}
    <input type="submit" value="削除" class="btn btn-danger" />
</form>
{% endblock %}
```

### URLの設定

`update`のURL設定の下に以下を追記。

`blog/urls.py`

```py
    path('delete/<pk>', views.Delete.as_view(), name="delete"),
```

### 動かしてみよう

個別ページから削除ページに移動できて、投稿が削除出来ればOKです。

## おわりに

今回作成した一覧・個別・作成・編集・削除はあらゆるものがカスタマイズ可能です。  
自分で一から作らずにdjangoがもともと用意している機能を最大限に使うようにしましょう。
