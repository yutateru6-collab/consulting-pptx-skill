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
