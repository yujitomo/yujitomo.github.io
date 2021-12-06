---
layout: math-note-type
title:  "Blowing Up along Linear Subvarieties"
category: Notes
tag: "Algebraic Geometry"
author: Yujitomo
description: "線形部分多様体に沿った射影空間の爆発について"
---

## Main Theorem

このノートでは以下の構造定理を証明します:

> **Theorem**
>
> \\(k\\)を体, \\(V\to W\\)を有限次元\\(k\\)-線形空間の全射, \\(K\\)をその核とし,
> \\(B\\)を\\(\mathbb{P}(V)\\)の\\(\mathbb{P}(W)\\)に沿った爆発とする. このとき,
> \\[ B \cong \mathbb{P}\_{\mathbb{P}(K)}(\mathcal{O}\_{\mathbb{P}(K)}(1)\oplus (\mathcal{O}\_{\mathbb{P}(K)}\otimes W)) \\]
> となる.

証明は, コホモロジーの半連続性などの定理を用いることは避け,
射影束や爆発の普遍性 (cf. \[ Hartshorne, Theorem II.7.12 \],
[\[Stacks, Lemma 0806\]](https://stacks.math.columbia.edu/tag/0806) ) などを用いて幾何的に行います.

この定理を用いることで, グラスマン多様体と射影空間の直積を incidence varietyに沿って爆発してできる多様体の構造についても調べることができます.

この定理を示す過程で, オイラー完全列と呼ばれる以下の完全列の存在も証明します.

> **Theorem (Eular Exact Sequence)**
>
> \\(k\\)を体, \\(n\\)を自然数とする. このとき, \\(\mathbb{P}^n=\mathbb{P}^n_k\\)上には以下の完全列が存在する:
> \\[ 0 \to \Omega\_{\mathbb{P}^n}(1) \to \mathcal{O}\_{\mathbb{P}^n}^{n+1} \to \mathcal{O}\_{\mathbb{P}^n}(1) \to 0. \\]

Hartshorne氏による教科書「Algebraic Geometry」では,
次数つき加群を用いて計算することによりオイラー完全列の存在が証明されていましたが,
このノートでは, それとは異なる視点による証明を与えます.

オイラー完全列については変形理論を用いた別証明もありますが, それについては別のノートを作成しようと考えています.
