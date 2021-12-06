---
layout: math-note-type
title:  "Separating Tangent Vectors"
category: Notes
tag: "Algebraic Geometry"
author: Yujitomo
description: "接ベクトルを分離する線形系に関するノートです."
---

## Introduction

基礎体\\(k\\)は代数閉であるとします.
このノートの主な考察対象は, 代数多様体\\(X\\)上の直線束\\(L\\)と線形系\\(V\subset H^0(X,L)\\)です.
\\(V\\)が基点なしであること, 点を分離すること, 接ベクトルを分離すること,
に対して, それぞれ加群論的, 幾何学的な意味づけを与えます.
特に, 接ベクトルを分離することについて調べる際,
\\(V\subset H^0(X,L)\\)というデータから\\(\mathcal{P}^1(L)\\)という層
(詳細は[PDFファイル](/assets/TeX Files/Separating Tangent Vectors/Separating Tangent Vectors.pdf)を参照)
を構成し, 層\\(\mathcal{P}^1(L)\\)の性質について簡単に調べるのですが,
この層\\(\mathcal{P}^1(L)\\)は他の場面でもいろいろと役に立ちます
(例えば[\[Strange Curves\]](/notes/2021/12/01/StrangeCurves.html)などを参照).


## Main Theorem

このノートの主なテーマは, 基点なしであること, 点を分離すること, 接ベクトルを分離すること, を次のように言い換えることです:

> **Theorem**
>
> \\(X\\)を\\(k\\)上の代数多様体,
> \\(L\\)を\\(X\\)上の直線束, \\(V\subset H^0(X,L)\\)を線形系とする.
> 1. 以下は同値である:
>     1. \\(V\\)は基点がない.
>     2. \\(V\subset H^0(X,L)\\)に対応する射\\(V\_X\to L\\)は全射である.
>        ただし\\(V\_X\\)は\\(V\\)の\\(X\to \mathrm{Spec}(k)\\)でのpull-backを表す.
>     3. \\(V\subset H^0(X,L)\\)の引き起こす有理写像\\(X\dashrightarrow \mathbb{P}(V)\\)は不確定点を持たない (すなわち, 射である).
>
> 2. 以下は同値である：
>     1. \\(V\\)は点を分離する.
>     2. \\(V\subset H^0(X,L)\\)に対応する射\\(p:V\_X\to L\\)を
>        二つの射影\\(\mathrm{pr}\_1,\mathrm{pr}\_2:X\times\_kX\rightrightarrows X\\)でpull-backしたのちに
>        足し合わせることで得られる射
>        \\[\mathrm{pr}\_1^* p + \mathrm{pr}\_2^* p : V\_{X\times\_kX}\to \mathrm{pr}\_1^* L\oplus \mathrm{pr}\_2^* L \\]
>        は対角集合\\(\Delta\subset X\times\_kX\\)の補集合上で全射である.
>     3. \\(V\subset H^0(X,L)\\)の引き起こす有理写像\\(X\dashrightarrow \mathbb{P}(V)\\)は射であり, さらに単射である.
> 3. 以下は同値である：
>     1. \\(V\\)は接ベクトルを分離する.
>     2. \\(V\subset H^0(X,L)\\)に対応する射\\(p:V\_X\to L\\)が引き起こす射
>        \\[ V\_X \to \mathcal{P}^1(L)\\]
>        は全射である.
>     3. \\(V\subset H^0(X,L)\\)の引き起こす有理写像\\( X\dashrightarrow \mathbb{P}(V) \\)は射であり, さらに不分岐である.

証明ではEular完全列を用います (cf.
[\[Blowing Up along Linear Subvarieties\]](/notes/2021/12/01/BlowingUpAlongLinearSubvariety.html) )

また, このノートでは, 代数多様体の間の不分岐な単射が埋め込みであることを確認することによって, 以下の定理も証明します:

> **Theorem**
>
> \\(X\\)を\\(k\\)上の代数多様体,
> \\(L\\)を\\(X\\)上の直線束, \\(V\subset H^0(X,L)\\)を基点のない線形系とする.
> このとき, 線形系\\(V\subset H^0(X,L)\\)が点と接ベクトルを分離することと,
> \\(V\subset H^0(X,L)\\)の引き起こす射\\(X\dashrightarrow \mathbb{P}(V)\\)が埋め込みであることは同値である.
