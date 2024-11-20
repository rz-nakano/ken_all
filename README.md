# 郵便番号データの利用

日本郵便が公表している郵便番号データを入力として使用する。

https://www.post.japanpost.jp/zipcode/dl/utf-zip.html


## ken_check.py

郵便番号から前方一致で都道府県を特定しようとする際、例外となる郵便番号を確認する。

```Shell
$ python ken_check.py ./utf_ken_all.csv
```
