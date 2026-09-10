# Classroom PPTX Mode — 高校授業用の優先ルール

このForkは、通常のコンサル型スライド規約の上に、**教室で生徒がスクリーンを見て理解・参加できる授業PowerPoint**のための厳格な Classroom Mode を追加する。

## 優先順位

中高の授業用スライドでは次の順で適用する。

1. `references/classroom-hard-gates-v3.md`
2. `references/classroom-slide-rules.md`
3. ユーザーが今回指定した授業要件
4. `references/classroom-rendering-stability.md`
5. `references/classroom-flowchart-rules.md`（フローチャート指定時）
6. `references/classroom-delivery-contract.md`
7. `references/classroom-visual-qa-v3.md`
8. `references/slide-rules.md`
9. 型カタログ・テンプレート

コンサル資料の一般ルールと授業上の見やすさが衝突した場合は、**授業上の見やすさを優先する**。

---

## Classroom Mode の標準フロー

1. 教材・教科書・問題集など一次資料を読む。
2. 何を生徒に理解させるかを1枚1役割で設計する。
3. フローチャート指定なら、最初に「判断の全体地図」を設計する。
4. 大きな文字で編集可能PPTXを作る。
5. `references/classroom-rendering-stability.md` を適用し、英文の不要改行・文字枠不足・AutoFit依存・内部余白不足を防ぐ。
6. スピーカーノートに教師用の詳しい説明・問い・想定回答・クリック順を入れる。
7. 原則、各内容スライドに on-click の段階表示を入れる。英文の強調のために英文自体を不自然に分割しない。
8. `scripts/check_deck.py` を実行する。
9. `scripts/check_classroom_hard_gates.py` を実行する。
10. `scripts/check_classroom_deck.py` を実行する。
11. **PPTXをPDF→PNGへレンダリングする。**
12. 全ページPNGを1枚ずつ原寸に近い状態で見て、英文・和訳を実際に読む。
13. コンタクトシートで全体の単調さ・色・構図の偏りも見る。
14. `references/classroom-visual-qa-v3.md` の基準で visual QA JSON を作る。
15. 問題が1件でもあれば、生成元を修正して**最終PPTXそのものから**全ページ再レンダリングする。
16. クリック動作について、PowerPoint実再生かPPTX内部設定確認のみかを制作記録に明記する。
17. `scripts/check_classroom_delivery.py` を通す。
18. 最終版のみ納品する。

**一般QA、Hard Gate QA、画像QAの全部が必要。どれか1つでも未実行なら完成ではない。**

---

## 絶対に納品してはいけない状態

次のどれか1つでもあれば、完成版として納品しない。

- 表紙タイトルが54pt未満
- 通常タイトルが38pt未満
- 通常本文が24pt未満
- 短いラベルが22pt未満
- 重要英文が28pt未満
- タイトルや英文が他の要素と重なる
- 日本語の語が不自然に途中で割れる
- 英文が強調語の都合で不自然な段落・改行に分割される
- 主語だけ、助動詞だけ等が不自然に1行へ孤立する
- 1行用の高さしかないタイトル枠に2行タイトルを押し込む
- AutoFit・自動縮小頼みで表示環境により改行数が変わる
- テキスト枠の内部余白が不足し、英文・和訳が枠線へ接触する
- `??` / `�` / `□` 等の文字化け
- 文字がボックスから切れる
- 授業用なのにスピーカーノートがほぼ無い
- クリック式が必要なのに clickEffect が0
- 問題スライドで答えが最初から見える
- フローチャート指定なのに、実態が角丸カードの羅列
- 修正後の再レンダリングをしていない
- 代替レンダラーだけの確認を「PowerPoint実機確認済み」と報告する
- 静止画だけの確認を「クリック再生確認済み」と報告する
- いずれかの checker が FAIL を返している

文字が入らない場合は、**小さくするのではなく、削る・広げる・組み替える・分ける**。

---

## フローチャート指定時

ユーザーが「フローチャートっぽく」「判断フロー」「decision tree」等を指定したら、`references/classroom-flowchart-rules.md` を必ず読む。

原則：

- まず1本の判断軸を作る。
- 分岐は質問または条件として書く。
- 矢印には方向と意味を持たせる。
- 同じ全体地図を再利用し、今説明している枝をハイライトする。
- 「四角い箱を横に並べて線を引いただけ」はフローチャートとみなさない。
- 連続するカードグリッドでフロー感を代用しない。

---

## ローカルQA

```bash
pip install python-pptx pillow

python3 scripts/check_deck.py path/to/deck.pptx

# 最上位の拒否条件。ファイル名や表紙から flowchart を自動推定できる
python3 scripts/check_classroom_hard_gates.py \
  path/to/deck.pptx \
  --profile auto \
  --json hard-gates.json

# 既存の詳細Classroom QA
python3 scripts/check_classroom_deck.py \
  path/to/deck.pptx \
  --json classroom-qa.json

# フローチャート指定を明示する場合
python3 scripts/check_classroom_hard_gates.py \
  path/to/deck.pptx \
  --profile flowchart \
  --json hard-gates.json
```

LibreOffice と poppler-utils がある環境では：

```bash
bash scripts/render_classroom_deck.sh path/to/deck.pptx qa-output
```

これによりPDF、全ページPNG、`contact-sheet.png` が生成される。

視覚確認後、`visual-qa.json` を作成して：

```bash
python3 scripts/check_classroom_delivery.py \
  --machine hard-gates.json \
  --visual visual-qa.json
```

まで通す。

**LibreOffice等でのレンダリングは静止画QAであり、Microsoft PowerPoint実機の表示・スライドショー再生確認とは区別して記録する。**

---

## GitHub Actions

`.github/workflows/classroom-pptx-qa.yml` を使い、`qa-input/` に置いたPPTXを検査できる。

Actionsは：

- 一般機械QA
- Classroom Hard Gate QA
- Classroom詳細QA
- LibreOfficeでPDF化
- 全ページPNG化
- コンタクトシート生成
- QA結果・PDF・PNGをArtifact保存

を行う。

**ただし、PPTXが無く deck-QA step が skipped の緑チェックは「デッキを確認した」証拠ではない。**

また、Actionsのレンダリングが成功しても、英文の不要改行・枠線との接触・タイトル高さ不足が画像に残っていればFAILである。

---

## 改善を蓄積する

実デッキで新しい失敗パターンが見つかったら、失敗を単に直して終わらせない。

- 生成ルール化できる → `references/classroom-hard-gates-v3.md` / `references/classroom-rendering-stability.md`
- フローチャート特有 → `references/classroom-flowchart-rules.md`
- 画像でしか拾えない → `references/classroom-visual-qa-v3.md`
- 機械検出できる → `scripts/check_classroom_hard_gates.py` / `scripts/check_classroom_deck.py`

**一度起きた失敗を次回から仕組みで防ぐ**ことをこのForkの基本方針とする。
