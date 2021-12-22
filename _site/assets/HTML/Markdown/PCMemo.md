

## Overall

- 問題のパッケージはインストールされているか??
- 「brew doctor」「jekyll doctor」などと打ってwarningが出てないか??
- 完全素人でないなら、公式の解説を読みこむ方が早いこともある


## Around Web Creating

- Chromeでコンソールを表示させるには, 右上の縦方向の三点のメニューマーク → その他のツール → デベロッパーツール.
- コンソールを注意深く見ること.
- CSSやJavaScriptで困ったときは、「どれが有効になっているのか」をコンソールで確認すること。
- とにかくコンソールと睨めっこせよ!!!!
- [Web関係の辞書的なサイト](https://developer.mozilla.org/ja/docs/Web)


### Web Designing

- 使う色の種類を増やさない方が見栄えする、似た系統の色3色以内？とか本屋で立ち読みした気がする。
- 可読性の高い背景色を使うべき。とか言いながらこのホームページの可読性は高くない方だが...
- [デザイナーじゃなくても知っておきたい色と配色の基本](https://baigie.me/officialblog/2021/01/27/color_theory/)


### HTML

- 構文チェッカー: [これ](http://www.htmllint.net/html-lint/htmllint.html)とか[これ](https://validator.w3.org/)とかがある。
- [Webページの基本構造](https://shu-naka-blog.com/html/tag01/)
  - ↑ CSSで装飾しまくって頑張るゲームではない!!!! ということがちょっとわかる.
- HTMLでソースコードを表示させるときはcodeタグで囲む. ただし特殊文字はエスケープしなければいけない.
- [主なエスケープ文字一覧](https://techacademy.jp/magazine/12553).
- pタグ内で改行するときはbrタグで、ソースを載せるときはcodeタグ。
- spanタグなどのinline系のタグの中で改行を打つと、それをJavaScriptなどでいじったときに変な挙動をすることがあるので注意。
- [KaTeX: Supported Functions](https://katex.org/docs/supported.html)
- 見出しタグ (h1,h2,...) にidを付与して、aタグのhrefでそこに飛ぼうとしてもうまくいかない場合がある (なぜ？)


### CSS

- 重複している設定に関しては、基本的にはより詳細なタグに対する設定が優先される。
  - → [点数計算の方法](https://nelog.jp/specificity-calculator)
  - ただし、重複していない設定に関してはこの点数計算は関係ない！全部覆いかぶさるように有効になっていく。
- paddingとmarginの基本的な違いはハコの内側か外側かだが、
それ以上に根本的に異なる性質として、[marginは「相殺」する](https://web-manabu.com/html-css32/)
(この性質のおかげで、文章の縦方向の余白はmarginで調節した方が統一的な余白の入り方になってくれる)。
- [displayプロパティについて](http://www.htmq.com/style/display.shtml)
- [list-style一覧](http://www.htmq.com/style/list-style-type.shtml)



### Java Script

- [jQuery 動かねーよクソがってなったらこれを確認](https://dezanari.com/jquery-not-work/)
- JavaScriptのコメントアウトはCSSのコメントアウトとおなじ
- 対象にしているオブジェクトのid名は.attr("id")で所得できる.
- 装飾が効かないとき, 改行が変に変換されてemptyに対して装飾を施している可能性がある.



### SCSS

- SCSSというのがある. コンパイルしてCSSファイルを作成する何らからしい
  - → 解説：[SCSS（SASS）とCSSの違いについて](https://blog.maromaro.co.jp/archives/8010)
  - → 解説：[【これからScssを使う人へ】Scssの使い方と便利さをさらっと紹介するぞ](https://qiita.com/mame_hashbill/items/e5f01d0f2523de6a13e5).
- 拡張子は「.scss」だが, HTMLファイル内に読み込む時はコンパイル後のCSSファイルなので, HTMLファイル内では「.css」と書かなければエラーが出る.
- SCSSでは自分でclearfixのclassを書かなくてもincludeできる.
  - → [ここ参照](https://qiita.com/naoyeah/items/e03b01a98a762b78d265)
  - と聞いたけどなんかパッケージみたいな感じ？よくわからなかったので私はmixinを書いてincludeしてます。



### Liquid

- Liquidのコメントアウトはcomment - endcommentで囲む感じ。
- [Liquidで配列を作る方法](https://qiita.com/momonoki1990/items/13f97a23436c142e4c9a)
- [assignとcaptureの違い](https://im-sosleepy.com/webproduction/assign_capture/)
- [Liquid Cheat Sheet](https://www.shopify.com/partners/shopify-cheat-sheet)
- appendやconcatでエラーを吐いたら、「辞書」型を「配列」型と間違えている可能性がある
  - → [Liquidの型について](https://docs.microsoft.com/ja-jp/powerapps/maker/portals/liquid/liquid-types)。
とくに、Jekyllで使う、タグ一覧を所得する「page.tags」などは「辞書型」なので、そのままではappendやconcatを使用できない。
- [Shopify](https://web-guided.com/1240/#:%7E:text=%E3%80%8Cliquid%E3%80%8D%E3%81%A8%E3%81%AF%E3%80%81Shopify,%E3%81%84%E3%81%9F%E8%A8%98%E8%BF%B0%E3%82%92%E3%81%97%E3%81%BE%E3%81%99%E3%80%82)というのがある. 新しくページを作る時にはテーマ選びの参考にしてもいいかもしれない.
- [for文でリストの逆順にforを回すときは最後にreversedを入れると良い](https://templates.supply/sort-jekyll-collection-by-reverse-order-and-limit-results/)
- [postsをalphabeticallyにソートする方法](https://stackoverflow.com/questions/8991995/using-liquid-to-sort-posts-alphabetically) postなどは辞書型なのでたんにsort_naturalするわけにはいかない。注意。


### Jekyll

[Jekyll](http://jekyllrb-ja.github.io/)は静的なwebサイトの作成ツール。
alg-dさんに教えていただきました. ありがとうございます. ~~このページもJekyllで編集できるように移行中です.~~
← 構造的な部分は移行しました. 微調整はまだですが.

- [GitHub Pagesでもサポートをしている.](https://docs.github.com/ja/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)
- Jekyllが何なのかについての解説は[このページの解説](https://www.codegrid.net/articles/jekyll-1/)が初見のときはわかりやすかった.
- [公式が使い方の詳しい解説をしている.](https://jekylltips-ja.github.io/) これを見るとだいぶ使えるようになるかも.
- [jekyllブログを始めたらまず最初に設定したいポイント](https://oshou.github.io/jekyll-blog-point/)
- 環境を設定したければ「sudo JEKYLL_ENV=\*\*\* jekyll \*\*\*」のようにする。sudoは先頭。たとえば「sudo JEKYLL_ENV=production jekyll b」など (←よく使うのでコピペ用に)


### React

- Reactというものがある。
- [Reactで静的サイトを作る話](https://nulab.com/ja/blog/typetalk/how-to-make-website-with-react-static/)


### その他

- [CMSを自作してオリジナル動的ホームページをフルスクラッチ開発してみよう！](https://denkenmusic.com/cms%E3%82%92%E8%87%AA%E4%BD%9C%E3%81%97%E3%81%A6%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB%E5%8B%95%E7%9A%84%E3%83%9B%E3%83%BC%E3%83%A0%E3%83%9A%E3%83%BC%E3%82%B8%E3%82%92%E3%83%95%E3%83%AB/)


## Terminal

- 困ったらUseful LinksのPC関係の部分を見る
- ターミナルで空白のファイルを扱うときは「"hoge hoge"」のように囲む
- Homebrew関係のコマンド (pythonやrubyも含む) で困ったらとりあえず一回「brew doctor」してみる.
  - → 「Unexpected static libraries:」とか
「gettext files detected at a system prefix. ~~ Consider removing these files:」
が出てきたら, 「rm -rf (そのpath)」をやる.
(「config」関係のwarningの解消のしかたがわかりません. 有名問題だそうですが...)
- 「Operation not permitted」や「Permission denied」に遭遇したら → とりあえず「sudo」つけてもう一回試す.
- 権限の確認は「ls -la」. 以下は変更のやり方 ([参考ページはここ](https://dara-blog.com/about-rails-error01))：
  - ファイルhogeの権限を「root」から「username」に変えたいなら → 「sudo chown username hoge」
  - フォルダhoge以下の権限を「root」から「username」に変えたいなら → 「sudo chown -R username hoge」
  - 確認事項：ターミナルはフルディスクアクセス許可されているか?? (システム環境設定→セキュリティとプライバシー→左側から「フルディスクアクセス」を選択)
  - 困ったら：[ここを参照](https://w3g.jp/apple/sip-disable/)　/　[ここも参考になる](https://dara-blog.com/about-rails-error01)




## Python

- [pythonのglobalの動作にちょっと驚いた](https://qiita.com/studio_haneya/items/dc072d4329fcacfaac2a) ← 私も驚いたのでリンクをメモしておく



## C++

- [正規分布の累積密度関数はerfという関数を使って表せる](https://cpprefjp.github.io/reference/cmath/erf.html)

### Finance

- [国内の株式指標](https://www.nikkei.com/markets/kabu/japanidx/) ← 日経平均の平均配当利回りとかが見れる。計算する上でのrの値とかに突っ込むと良いのかも？
- Black-SholesモデルとかをいじるときのTはT=1で1年を表すと考えれば良いと思う。1ヶ月は0.0833年
- [日経平均のボラティリティ](https://indexes.nikkei.co.jp/nkave/index/profile?idx=nk225vi)と[日経平均オプションの価格](https://svc.qri.jp/jpx/nkopm/)


## Ruby

- 「`require': cannot load such file -- hoge」に遭遇したら
  - → hogeがインストールされてないかもしれないから 「sudo bundle add hoge」をやる

Gemfileの書き方　/　 WEBrickを使うためのメモ

## Others

- YAMLのコメントアウトはシャープ
- [GitHubっぽいアイコン](https://primer.style/octicons/)
