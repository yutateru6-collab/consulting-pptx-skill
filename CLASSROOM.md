# Classroom PPTX Mode — 高校授業用の優先ルール

> **制作開始前に [AGENTS.md](AGENTS.md) を全文読み、ゲートA・Bを実行する。関連指示をすべて末尾まで読み、全要件の意味・適用範囲・実装先・検証方法を把握するまでスライドや生成コードを作り始めない。**
>
> **納品前はAGENTS.mdのゲートC・Dと本書の既存検査を実行し、`PRESENTATION_MODES.md` で選んだ方式に適用される項目を判定する。最終PPTX・全スライド画像・必要な動作確認を証拠にし、適用項目に違反・未確認があれば完成扱いにしない。標準の `classroom-editable` では既存のクリック・枠線なし・英文改行・文字サイズの条件を省略しない。**

このForkは、通常のコンサル型スライド規約の上に、**教室で生徒がスクリーンを見て理解・参加できる授業PowerPoint**のための厳格な Classroom Mode を追加する。

制作開始前に [`PRESENTATION_MODES.md`](PRESENTATION_MODES.md) で `classroom-editable` と `source-image-click` を選ぶ。以下の「標準フロー」「標準デザイン」「既存機械ゲート」は編集可能文字の標準方式を記述する。画像再生成方式の明示的な例外と専用の検証条件はモード表と次節で確認する。

## 元画像を画像生成で再制作する専用ルート

ユーザーが**元の英文法まとめ画像を、文字を含めて画像生成で描き直し、再生成画像を分割して段階表示**することを明示した場合は、[`prompts/grammar-image-to-click-pptx.md`](prompts/grammar-image-to-click-pptx.md) と [`references/grammar-image-to-click-workflow.md`](references/grammar-image-to-click-workflow.md) を適用する。この依頼では文字の画像化、原画のノート罫線・手書きの囲み、原画に合わせたスライド比率を許す。通常の編集可能テキスト主体のClassroom Modeを選ぶ依頼にはこの例外を広げない。

元画像の文字列と最終画像の照合、可読性、スピーカーノート、本当のon-click画像オブジェクト、最終PPTXからの全ページ書き出しと目視は必須。従来の文字サイズ・英文バランスの機械チェックは画像内の文字を解析できないので、検査の適用可否と結果を記録し、原文台帳と全ページ目視で補う。検査で見ていない文字を「機械QA合格」と報告しない。

## Education Mode — 英語を「理解させる」授業では必須

英語授業、英文法、語彙、長文読解、英作文、リスニング、試験解説など、**生徒の理解・判断・再現を目的とするデッキ**では、通常のClassroom Modeに加えて `EDUCATION.md` を適用する。

`classroom-editable` で授業を新規設計する場合、スライドの見た目を設計する前に次のEducation preflightを実行する。原本内容のみを再構成する `source-image-click` では元画像の項目→スライド→クリックの対応表を作り、原本にないretrieval問題を必須化しない（詳細は `EDUCATION.md` とモード表）。

以下の1～4は `classroom-editable` で授業を新規設計する場合の手順。`source-image-click` / `source-only` では `EDUCATION.md` の原文忠実性に関する規則を読み、原文台帳とクリック対応表で構成を検証する。

1. `EDUCATION.md` を読む。
2. `references/education-mode.md` と `references/english-teaching-archetypes.md` を読む。
3. `templates/education-storyboard.example.json` を参考に `education-storyboard.json` を作り、学習目標・前提知識・典型誤答・各スライドの教育上の役割・確認問題を先に固定する。
4. `python3 scripts/check_education_storyboard.py education-storyboard.json --json education-qa.json` を実行し、**FAIL 0**にする。FAILが残ったままPPTX生成へ進まない。
5. Google Slidesも成果物に含める場合は、生成前に `references/google-slides-output.md` を読み、`googleSlidesBuildMode` を明示する。

Education Modeは既存のClassroom Hard Gatesを置き換えない。**`classroom-editable` では教育設計QAに通っても、文字サイズ・クリック表示・スピーカーノート・英文改行・borderless・レンダリング・全ページ目視・delivery gateは従来どおり必須**である。`source-image-click` は方式固有ゲートに従う。

## 優先順位

中高の授業用スライドでは次の順で適用する。

1. ユーザーが今回明示した授業要件と `PRESENTATION_MODES.md` で選んだ方式
2. `references/classroom-hard-gates-v3.md`（その方式に適用できる項目）
3. `references/classroom-slide-rules.md`（その方式に適用できる項目）
4. `references/classroom-rendering-stability.md`
5. `references/classroom-flowchart-rules.md`（フローチャート指定時）
6. `references/classroom-delivery-contract.md`
7. `references/classroom-visual-qa-v3.md`
8. `references/slide-rules.md`
9. 型カタログ・テンプレート

コンサル資料の一般ルールと授業上の見やすさが衝突した場合は、**授業上の見やすさを優先する**。

---

## Classroom Mode の標準フロー（`classroom-editable`）

1. 教材・教科書・問題集など一次資料を読む。
2. 何を生徒に理解させるかを1枚1役割で設計する。
3. フローチャート指定なら、最初に「判断の全体地図」を設計する。
4. 大きな文字で編集可能PPTXを作る。**文字を載せるためだけの四角い枠線は付けず、原則 borderless にする。**
5. `references/classroom-rendering-stability.md` を適用し、英文の不要改行・文字枠不足・AutoFit依存・内部余白不足を防ぐ。
6. スピーカーノートに教師用の詳しい説明・問い・想定回答・クリック順を入れる。
7. 原則、各内容スライドに on-click の段階表示を入れる。英文の強調のために英文自体を不自然に分割しない。
8. **`python3 scripts/normalize_classroom_style.py path/to/deck.pptx --in-place` を実行し、通常テキストの装飾的な四角枠を除去する。**
9. `scripts/check_deck.py` を実行する。
10. `scripts/check_classroom_hard_gates.py` を実行する。
11. `scripts/check_classroom_deck.py` を実行する。
12. **PPTXをPDF→PNGへレンダリングする。**
13. 全ページPNGを1枚ずつ原寸に近い状態で見て、英文・和訳を実際に読む。**不要な四角枠が残っていないかも確認する。**
14. コンタクトシートで全体の単調さ・色・構図の偏りも見る。
15. `references/classroom-visual-qa-v3.md` の基準で visual QA JSON を作る。
16. 問題が1件でもあれば、生成元を修正して**最終PPTXそのものから**全ページ再レンダリングする。
17. クリック動作について、PowerPoint実再生かPPTX内部設定確認のみかを制作記録に明記する。
18. `scripts/check_classroom_delivery.py` を通す。
19. 最終版のみ納品する。

**一般QA、Hard Gate QA、画像QAの全部を実行して結果と適用範囲を記録する。`classroom-editable` は全適用ゲートのPASSが完成条件。`source-image-click` は `PRESENTATION_MODES.md` の方式固有ゲートで完成を判定し、一般QAの画像内文字・16:9・ネイティブ文字等の対象外判定をPASSにしない。**

---

## Classroom Mode の標準デザイン（`classroom-editable`）

授業用PPTXでは、**文字の周囲に四角い外枠線を付けない形式をデフォルト**とする。

- タイトル、本文、英文、和訳、解説、答え、ヒントは、編集可能なテキストボックスで作るが外枠線は原則 `no line`。
- 色付き面を使う場合も、背景色だけで区切り、外周の線は付けない。
- 左右比較は、余白・見出し・薄い背景差で分ける。左右を大きな四角枠で囲わない。
- 重要語句は、文字色、太字、下線、短いアクセント線、矢印で強調する。
- 文字を囲う枠線を「教材っぽさ」「カードっぽさ」のために足さない。
- 枠線が必要なのは、表、フローチャートのノード境界、座標軸、ベン図、UI再現など、**線自体が意味を持つ場合だけ**。

このデフォルトは、ユーザーが明示的に「枠を付けて」「囲みを使って」と指定した場合のみ解除する。

### 境界線が意味を持つ例外の名前付け

機械QAと自動整形で、意味のある境界線を通常の装飾枠と区別するため、境界線を残す図形には次の接頭辞を使う。

- `FLOW_`：フローチャート・判断フロー
- `NODE_`：意味を持つノード境界
- `TABLE_`：表構造
- `AXIS_`：座標・軸
- `VENN_`：ベン図
- `DIAGRAM_`：境界線そのものが意味を持つ図解
- `UI_`：実物UI再現

**例外接頭辞を、通常の英文・和訳・本文の枠線を残すための抜け道として使わない。**

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
- **文字を載せるためだけの四角い外枠線が残っている**
- **左右比較や解説を大きな四角枠で囲っている**
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
- ノードに境界線が必要な場合は可。ただし、通常の英文・和訳・解説用テキストまで四角枠化しない。

---

## ローカルQA

```bash
pip install python-pptx pillow

# 生成時の取りこぼしを自動でborderless化する
python3 scripts/normalize_classroom_style.py path/to/deck.pptx --in-place

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

# borderlessポリシーの自己テスト
python3 scripts/test_classroom_style_policy.py
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

- Pythonスクリプトのコンパイル
- borderlessポリシーのsmoke test
- 一般機械QA
- Classroom Hard Gate QA
- Classroom詳細QA
- LibreOfficeでPDF化
- 全ページPNG化
- コンタクトシート生成
- QA結果・PDF・PNGをArtifact保存

を行う。

**ただし、PPTXが無く deck-QA step が skipped の緑チェックは「デッキを確認した」証拠ではない。**

また、Actionsのレンダリングが成功しても、英文の不要改行・枠線との接触・タイトル高さ不足・不要な四角い外枠線が画像に残っていればFAILである。

---

## 改善を蓄積する

実デッキで新しい失敗パターンが見つかったら、失敗を単に直して終わらせない。

- 生成ルール化できる → `references/classroom-hard-gates-v3.md` / `references/classroom-rendering-stability.md`
- フローチャート特有 → `references/classroom-flowchart-rules.md`
- 画像でしか拾えない → `references/classroom-visual-qa-v3.md`
- 機械検出できる → `scripts/check_classroom_hard_gates.py` / `scripts/check_classroom_deck.py`
- スタイル正規化できる → `scripts/normalize_classroom_style.py` / `scripts/classroom_style_policy.py`

**一度起きた失敗を次回から仕組みで防ぐ**ことをこのForkの基本方針とする。
