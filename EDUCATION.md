# EDUCATION MODE — 英語を「説明する」ではなく「理解させる」授業スライド

このモードは `CLASSROOM.md` の上に追加する**学習設計レイヤー**である。英語授業、英文法、語彙、長文、英作文、試験解説など、生徒の理解・判断・再現を目的とするスライドでは適用する。

原画像の内容と画風を忠実にPowerPointへ移すことが明示された場合は、[`prompts/grammar-image-to-click-pptx.md`](prompts/grammar-image-to-click-pptx.md) と [`references/grammar-image-to-click-workflow.md`](references/grammar-image-to-click-workflow.md) を先に読む。原本にない確認問題を一般的な教材構成や機械チェックを通すためだけに足さない。画像内文字を例外的に許す範囲と検査方法は専用ルートに従い、通常のイラスト追加時の「重要文は画像に焼き込まない」という原則は維持する。

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
- イラスト・画像・SVG・アイコン・キャラを使う場合:
  - `ILLUSTRATION.md`
  - `skills/classroom-illustration/SKILL.md`
  - `references/illustration-mode.md`
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

## Illustration preflight — 絵を先に置かず、必要性を先に決める

イラスト・画像・SVG・アイコン・継続キャラを使う場合は、Education Storyboard の後、スライド生成の前に `illustration-plan.json` を作る。

テンプレート:

- `templates/illustration-plan.example.json`

各スライドで `use / omit` を明示し、`use` の場合だけ role・learningFunction・assetType・layout・bbox・textSafeZone・styleFamily・altText・source を定義する。

検査:

```bash
python3 scripts/check_illustration_plan.py illustration-plan.json --json illustration-plan-qa.json
```

**Illustration PlanにFAILがあるまま画像生成や素材探しへ進まない。**

原則:

- 全ページに均等に絵を入れない
- 「空いているから」は採用理由にしない
- 絵は cognitive anchor になるページだけに使う
- 文章を置いた後の余白へ絵をねじ込まず、先にvisual zoneを予約する
- 重要英文・和訳・正解・数値を画像へ焼き込まない
- 同一デッキでは画風と継続キャラを固定する

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

## Visual Asset QA — 画像が文字へ侵入しないかを別ゲートで確認

イラスト・画像・SVG等を含むPPTXでは、Text-flow QAに加えて次を実行する。

```bash
python3 scripts/check_classroom_visual_assets.py deck.pptx --json visual-assets-qa.json
```

このcheckerでは、通常イラストとネイティブ文字の重なり、画像と文字の安全距離、スライド外へのはみ出し、cropなし画像の縦横変形、画像過密を検査する。

`BG_` / `FULLBLEED_` / `DIAGRAM_BG_` で始まる画像は意図的な背景として扱えるが、背景上の文字コントラストや視認性は必ず最終PNGで確認する。

Visual Asset QAがFAILなら、文字を小さくせず、次の順で直す。

1. visual zoneを縮める/移動する
2. text zoneを広げる
3. レイアウトを左右反転する
4. イラストを次スライドへ分ける
5. 不要ならイラストを削る

## PPTXとGoogle Slides

- PowerPoint: Classroom Modeの on-click build を使う。
- Google Slides: `references/google-slides-output.md` に従う。
- Google Slidesで段階表示を必要とする場合、API上のアニメーション作成に依存せず、原則 `duplicate-slides` 方式（同一スライドを段階ごとに複製して内容を追加）を使う。
- 「Google SlidesでPowerPointと同じアニメーションを実装・検証済み」と、実際に検証していない限り報告しない。

## 外部プロジェクトから取り入れた設計思想

この実装は、以下の公開プロジェクトを参考にしつつ、このリポジトリの高校英語授業向け要件に合わせて再設計した。

- SlideSage — education mode / backward design / prerequisite sequencing / retrieval / worked examples
  - https://github.com/vedraut/slidesage
- powerpoint-skill — pedagogy audit / motivation-before-formalism / worked-example proximity / Socratic prompts
  - https://github.com/Noi1r/powerpoint-skill
- google-slides-generator — shared geometry / visual proof / Google read-back / editable-native philosophy
  - https://github.com/oimiragieo/google-slides-generator
- wshobson/agents / pptx-visual-assets — asset provenance / explicit bbox / aspect-ratio discipline / native labels
  - https://github.com/wshobson/agents
- lgwanai/ppt-skill — illustration search / educational visual categories / SVG recoloring
  - https://github.com/lgwanai/ppt-skill
- paper-engine-illustrations — cognitive anchors / shot-list planning / recurring-character consistency
  - https://github.com/AppajiDheeraj/paper-engine-illustrations

外部リポジトリのテンプレート・コード・素材をそのまま正典にせず、`CLASSROOM.md` と本リポジトリのHard Gatesを常に優先する。第三者素材を実際に取り込む場合は、その素材自身のライセンスと出典を個別に確認する。
