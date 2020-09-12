# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView

# 自分で作ったPostモデルを取り込み
from .models import Post

# 一覧
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

# 個別
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post