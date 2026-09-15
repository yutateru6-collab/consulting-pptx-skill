# EDUCATION MODE — 英語を「説明する」ではなく「理解させる」授業スライド

このモードは `CLASSROOM.md` の上に追加する**学習設計レイヤー**である。英語授業、英文法、語彙、長文、英作文、試験解説など、生徒の理解・判断・再現を目的とするスライドでは適用する。

## 目的

良い授業スライドを「情報が整理された資料」ではなく、次の学習プロセスを画面上で成立させるものとして定義する。

1. 既有知識を呼び起こす
2. まず場面・対比・問題を見せる
3. 生徒自身に違いを発見させる
4. ルール・形を短く言語化する
5. 具体例を教師が解く
6. 生徒と一緒に解く
7. 生徒だけで解く
8. 少し後でもう一度思い出させる

「定義→箇条書き→まとめ」だけで終わるデッキを Education Mode とみなさない。

## 必読

Education Mode では、Classroom Mode の必読資料に加えて次を読む。

- `references/education-mode.md`
- `references/english-teaching-archetypes.md`
- **`references/classroom-layout-safety.md`** — 文字かぶり、自動折返し、可変高さテキストの縦積み事故を防ぐ
- Google Slides を出力する場合: `references/google-slides-output.md`

## 生成前ゲート: Education Storyboard

PPTX/Google Slidesを作る前に `education-storyboard.json` を作り、以下を明示する。

- audience / goal / time budget
- measurable learning objectives
- concepts and prerequisites
- likely misconceptions
- each slide's pedagogical role
- objective mapping
- concepts taught/checked
- reveal/build order
- teacher notes
- output target

テンプレート: `templates/education-storyboard.example.json`

検査:

```bash
python3 scripts/check_education_storyboard.py education-storyboard.json --json education-qa.json
```

**FAILが1件でもあればスライド制作へ進まない。** WARNは人間/エージェントが理由を確認し、意図的な例外か修正対象かを判断する。

## レイアウト安全ゲート — 文字を置いてから祈らない

英語授業では、主役英文・和訳・文法ラベルの縦位置を**固定Y座標で独立に置かない**。可変長テキストは上から下へ stack として配置し、次要素のY座標を直前要素の実効高さから計算する。

特に3カラムでは、各カラムの主役英文が28pt以上で原則2行以内に収まるかを先に確認する。2つ以上のカラムで3行以上になるなら、3カラムを維持せず2カラムまたは複数スライドへ再設計する。

PPTX生成後は必ず次を実行する。

```bash
python3 scripts/check_classroom_textflow.py deck.pptx --json textflow-qa.json
```

このcheckerは、**テキストボックス同士の矩形は重なっていないのに、上の英文が自動折返しで1行増えてボックス外へoverflowし、下の日本語へ侵入するケース**をHard FAILとして検出する。

Text-flow QAがFAILなら、フォントを小さくして通さず、次の順で直す。

1. 例文を短くする
2. 英文ボックスを広げる
3. 3カラム→2カラム
4. 和訳/補足を次クリック・次スライドへ送る
5. スライドを分割する

その後、従来どおり最終PPTXをPDF/PNGへ再レンダリングし、全ページを目視確認する。機械QA PASSだけで完成扱いにしない。

## PPTXとGoogle Slides

- PowerPoint: Classroom Modeの on-click build を使う。
- Google Slides: `references/google-slides-output.md` に従う。
- Google Slidesで段階表示を必要とする場合、API上のアニメーション作成に依存せず、原則 `duplicate-slides` 方式（同一スライドを段階ごとに複製して内容を追加）を使う。
- 「Google SlidesでPowerPointと同じアニメーションを実装・検証済み」と、実際に検証していない限り報告しない。

## 外部プロジェクトから取り入れた設計思想

この実装は、以下のMITライセンスの公開プロジェクトを参考にしつつ、このリポジトリの高校英語授業向け要件に合わせて再設計した。

- SlideSage — education mode / backward design / prerequisite sequencing / retrieval / worked examples
  - https://github.com/vedraut/slidesage
- powerpoint-skill — pedagogy audit / motivation-before-formalism / worked-example proximity / Socratic prompts
  - https://github.com/Noi1r/powerpoint-skill
- google-slides-generator — shared geometry / visual proof / Google read-back / editable-native philosophy
  - https://github.com/oimiragieo/google-slides-generator

外部リポジトリのテンプレートやコードをそのまま正典にせず、`CLASSROOM.md` と本リポジトリのHard Gatesを常に優先する。
