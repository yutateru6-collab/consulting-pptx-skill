# Classroom Layout Safety — 文字かぶり・自動折返し事故を防ぐ正典

この規則は Classroom Mode / Education Mode の全スライドに適用する。目的は、PPTX上の図形座標が正常でも、PowerPoint・LibreOffice・Google Slides等で文字が自動折返しして下の要素へ侵入する事故を防ぐことである。

以下のテキストボックスの実効高さ・可変長文字のstack・AutoFit検査は [`../PRESENTATION_MODES.md`](../PRESENTATION_MODES.md) の `classroom-editable` 用。画像パーツの2方式は画像内の文字切れ・重なりを最終PNGで点検し、`content-image-click` はパーツの実画素とPPTX上の拡大有無も専用の検査で確認する。

## 1. 原則: 可変長テキストの下を固定Y座標で置かない

悪い実装:

```text
英文: y=3.0, h=0.8
和訳: y=3.85
```

英文が1行増えた瞬間に和訳と衝突する。

良い実装:

```text
englishHeight = measure/estimate(text, font, width)
translationY = englishY + max(englishBoxHeight, englishHeight) + SAFE_GAP
```

**次の要素のY座標は、直前要素の実効高さから計算する。** 可変長テキストを絶対座標で縦積みしない。

## 2. Text-flow first

各カラム・各説明ブロックは、上から下へ `stack` として配置する。

1. 見出し
2. 英文
3. 和訳 / 意味
4. 文法ラベル / 結論

各要素の間には **最低 0.14 inch（約10pt）** の安全余白を置く。主役英文の直下は **0.18 inch以上**を推奨する。

実装では `nextY = previousBottom + gap` を使い、`3.10`, `3.85`, `4.45` のような独立したマジックナンバーで縦位置を決めない。

## 3. 文字ボックスの必要高さを先に見積もる

AutoFitやshrinkで事故を隠さない。フォントサイズを固定したまま、幅と文字量から必要行数を予測し、必要高さを確保する。

保守的な目安:

```text
requiredHeightPt = predictedLines × fontPt × 1.18 + topMargin + bottomMargin + 4pt
```

- `predictedLines` は実フォント幅または保守的な文字幅推定で求める。
- 英文はPowerPoint側の自動折返しを過信せず、90〜94%程度の幅安全率をかける。
- 必要高さが取れないときは、文字を小さくせず、**短文化 → 幅を広げる → カラム数を減らす → スライドを分割**する。

## 4. 3カラムの使用条件

3カラムは情報密度が上がりやすい。英語授業で3カラムを使ってよいのは、各カラムの主役英文が次を満たす場合だけ。

- 28pt以上（推奨32pt以上）
- 原則2行以内
- 3行になる場合でも、その下の和訳・説明との安全余白を確保できる
- 英文・和訳・結論を合わせても縦方向に詰まらない

**2つ以上のカラムで主役英文が3行以上になるなら、3カラムを捨てて2カラムまたは複数スライドへ分割する。**

## 5. 行数予測後にレイアウトを選ぶ

レイアウトを先に固定して文章を押し込まない。

1. 文言を確定する
2. 指定フォント・指定幅で行数を予測する
3. 1/2/3カラムのどれが安全か選ぶ
4. 高さを計算して配置する
5. レンダリングして実画面で再確認する

「3カラムのテンプレートを選んだから3カラムのまま」は禁止。

## 6. Collision budget

独立したテキストブロック同士では、レンダリング後も次を満たすこと。

- 文字同士が接触しない
- 英文のディセンダ（g, p, y等）と下の日本語が視覚的に接触しない
- 最低0.14 inchの空白を残す
- 背景塗りの境界に文字が接触しない

ボックスの矩形が重なっていなくても、**文字がボックス外へoverflowして他要素へ侵入したらFAIL**。

## 7. 自動折返し事故のHard FAIL

次は納品拒否条件。

- predictedLinesに対してテキストボックスの高さが不足する
- 予測上、overflowした文字が次のテキストブロックへ0.14 inch以内まで侵入する
- 2行想定の英文が3行になり、和訳と接触する
- 文字を小さくして衝突を回避する
- `shrinkText` / AutoFitで見かけ上だけ収め、教室用最低文字サイズを割る
- レンダリング画像で一文字でも別のテキストと重なる

## 8. 生成時の推奨 helper

PptxGenJS等では、可変長の縦積みに共通helperを使う。

```js
function placeStack(items, startY, gap) {
  let y = startY;
  for (const item of items) {
    const h = estimateTextHeight(item.text, item.width, item.fontSize);
    place(item, { y, h });
    y += h + gap;
  }
  return y;
}
```

本番では推定値に安全係数を加える。`y` を各要素ごとに手入力しない。

## 9. QAは三段階

1. **生成前**: 行数・必要高さ・カラム密度を予測
2. **PPTX構造QA**: `scripts/check_classroom_textflow.py` でoverflowと次要素への侵入を検査
3. **最終レンダリングQA**: PDF/PNGを全ページ目視。構造QAを通っても見た目で接触していればFAIL

機械QAだけ、画像QAだけの片方で済ませない。

## 10. 典型的な修正優先順位

文字がぶつかる場合:

1. 例文を短くする（学習目標を壊さない範囲）
2. 英文ボックスを横に広げる
3. 3カラム→2カラム
4. 和訳/補足を次クリックまたは次スライドへ送る
5. スライドを分割する

**フォント縮小は最後の逃げ道にしない。Classroom Modeの文字サイズ下限を優先する。**
