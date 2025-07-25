# googleSTEP
## コードの説明

今回、私は主に「後置記法」の考え方に基づきコードを作成しました。（大学でちらっとやったことがあったので）（本当はカッコの中身を再帰していく方針でも実装したかったのですが、コードが煩雑になり課題３でデバッグできなくなってしまったので諦めました…）


私たちが普段慣れ親しんでいる `1+2` のような数字の間に演算子を挿入する記法は、**中置記法**と呼ばれています。

今回は、この中置記法の順序に並んでいるtokens列を、演算子を数字の後に挿入する**後置記法**（さっきの例なら`1 2 +`になります）に変換し、その状態で計算を行うようにしました。

後置記法の最大のメリットとしては、カッコがなくても演算の優先順位を気にすることなく計算ができることです。
例えば`3*(2+4)`の時、後置記法になおすと`3 2 4 + *`となり、カッコがなくても計算内容を保存することができています。
また実際に計算を行うフェーズでも、高知記法だと直前の数字２つと直前の演算子1つがわかっていればいいので、コードが非常にシンプルになります。

しかし、中置記法から後置記法に変換する際には、やはり演算子同士の優先順位を気にする必要があります。
今回は基本的に以下の場合わけを行い処理を進めました。（私の経験則的な部分が多いので、ちょっと説明不足が目立つかもしれないです、、）
以下での「出力」がコードでのoutput,スタックがstackに対応しています。

>今回処理するにあたり、演算子の結合の強さは
```+,- << *,/ << -n,absなど << ()```
であることを用いています。

1\. 数字ならそのまま出力

2\. 左カッコならstackに積む

3\. 右カッコならstackの演算子を左カッコが出てくるまで出力

4\. 演算子なら、現在の演算子(token)とstackの一番上(top)の演算優先度を考慮し処理
- token = top　ならtop出力しtokenをstackに
    - 今回扱う演算子は左結合なので、この処理でいいみたいです
- token > top なら tokenをstackに積み戻す
- token < top なら、stackの中身が左カッコまたは空になるまで演算子を出力

（ここの処理は少し煩雑になってしまいました、、積より優先度が高い演算子や、右結合の演算子が追加された場合対応できなくなってしまいます）

5\. 単項間演算子の場合は、stackに積む


## 課題1
最初は単純にevaluate関数の中でループを２回回す構成にし、おそらくうまくいきました。
課題３をやる際に構造を大きく変え、後置で評価することにしました。

## 課題2
四則演算はどのパターンでも対応できるようになったと思います。

## 課題３
まず最初は、カッコが見つかったらカッコ・積と商・和と差を行い、再帰処理を行うようなプログラムを考えました。しかしindexの管理が煩雑になってしまい、２重カッコがある際に一番外側の右カッコが削除されないという問題が発生しました。
そこで方針を大きく変え、中置記法という普通の記法を、演算子を数字の後ろ側に置く後置記法に書き換えて計算することを考えました。(evaluate_2)
こちらの方針では計算の際に２重ループなどを回す必要がなくなり、またモジュール化の観点からしてもいいコードになったと思います。

## 課題4
absのみ実装しました。
課題3までは2項間演算子のみを考えていましたが、課題4をやるにつき単項間演算子について考慮する必要があります。単項間は掛け算・割り算よりももっとも結びつきが強いと定義し、それにつき change_to_postfix と evaluate_postfix の場合わけを増やしました。
