# Repository instructions for agents

## 制作開始・完成判定の必須条件（2026-09-11追加）

**このリポジトリで制作・修正・再出力する前に、関連する全指示を最後まで読み、全要件の意味・適用範囲・実装先・検証方法を把握すること。一部だけ読み、残りを記憶や推測で補って作り始めることを禁止する。適用される必須要件をすべて実装し、最終成果物で検証する。違反・未確認が一件でも残るものを完成版として納品してはいけない。**

「読んだ」「理解した」「設定した」は合格の証拠ではない。読了、理解、実装、検証は別の状態である。この手順は本リポジトリ全体に適用するが、授業用とコンサル用の仕様を混同しない。以下の既存Classroomルールと検査スクリプトを弱めたり置き換えたりするものではない。

実行環境の上位指示と今回のユーザーの明示指定を尊重する。明示的に変更された条件だけを置き換え、それ以外を維持する。「早く」「簡単に」を検査省略や文字縮小の許可と解釈しない。依頼されていない仕様変更で通過させない。

### ゲートA：最新版の全文取得・読了

最初にこの `AGENTS.md`、`README.md`、`SKILL.md` を読む。授業用はこのファイル下部の「Files to read before producing a classroom deck」に従い、`CLASSROOM.md` と列挙された参照規則をすべて読む。フローチャート等の条件付き資料、実際に使用するテンプレート・検査手順、ユーザーから渡された教材も対象範囲で読む。

ツール出力が省略・truncated・続きありなら末尾まで続きを取得する。見出しだけ、検索断片だけ、前回の要約だけ、ファイルを保存しただけでは読了にならない。作業用にファイルパス、取得元、版またはSHA、読んだ範囲、末尾取得を記録する。相互参照は同じ版を全文読了済みなら再帰的に読み直さない。

必要な指示や教材が取得できない場合、未読部分を推測して制作しない。利用できた資料と不足を区別する。現在の資料・ソフト仕様の確認が指示されている場合、古い確認記録で代用しない。

### ゲートB：全指示を要件化してから設計

作業用の要件対応表に、要件ID、出典ファイル・節、適用判断と理由、解釈・合格条件、実装先・方法、最終版の検証方法、状態、証拠を記録する。長い思考過程ではなく仕様と検査事実を残す。

元の規範的な節・箇条書きから逆照合し、全適用要件の対応漏れを確認する。内容の忠実性、枚数、学習順、編集可能性、ノート、クリック、文字サイズ、枠、英文改行、図解、出力形式、全スライド確認、納品条件を含める。下記の数例だけを全指示の代わりにしない。

「何を守るか」「今回のどこに適用するか」「どこへ実装するか」「完成後に何を見れば違反を検出できるか」を具体化できない要件は理解済みとしない。曖昧さや衝突は指示の優先関係とモードで整理し、都合のよい規則だけ選ばない。

### ゲートC：実装・内容版の固定

ゲートA・Bの後で設計・生成する。過去のコードやテンプレートにも全要件を照合する。内容・スライドID・図形ID・ノート・クリック順・スタイルを同じ確定版へそろえる。設定した段階は「実装済み未検証」とする。

- 授業用の逐次クリック表示と初期状態の答え非表示を実装する。ノートにクリック順を書いただけで実装済みにしない。
- 通常文字の枠線なし、役割別文字サイズ、英文の意味単位の改行、編集可能なテキストを既存仕様どおり適用する。
- 小さくして収めず、既存規則の範囲で幅・配置・情報量・分割を見直す。必要な原文や答えを黙って削ってはいけない。
- フローチャートの意味ある境界線と、装飾目的の文字囲みを区別する。例外用の図形名や検査オプションで規則を回避しない。

### ゲートD：最終PPTX・画像・動作の検証

このファイルの既存「Non-negotiable completion rule」に定める全検査を実行する。一般QA、hard gate、英文バランス、レイアウト、全スライド個別画像確認、delivery gateのいずれも省略しない。

各要件の証拠を、最終PPTXの版またはハッシュ、実行したコマンドと結果、各スライド番号と確認画像に結びつける。状態は「未実装／実装済み未検証／合格／不合格／未確認／対象外」で区別する。未実施・証拠なし・旧版の検査結果を合格にしない。

静止画だけではクリック動作を検証できない。最終PPTXのtiming・対象図形・クリック順を点検し、PowerPoint実再生を行った範囲と内部設定だけを確認した範囲を区別する。代替レンダラーを実機確認と称さない。実機動作が未確認ならその制限を報告し、未実施の再生確認を合格扱いにしない。

**完成版として納品可能＝必読資料の全文読了 AND 全要件の理解・実装 AND 全適用要件の最終版検証合格 AND 違反・未確認0件。**

内容・図形・ノート・アニメーション・書体・変換環境を変更したら、依存する画像・PDF・検査結果を旧版として無効にする。影響範囲の内容・クリックを再確認し、最終PPTXから全スライドを再レンダリングして最終検査をやり直す。古い画像を新しいPPTXの証拠にしない。

不合格・未確認は修正して再検査する。解消できない場合、実際にできた範囲と不足を明示し、途中成果を完成品に見せかけない。対象デッキの検査がskippedのActions成功を合格証拠にしない。

### 記録と指示更新だけの作業

読了記録・要件対応表・検査画像・結果は作業用とし、依頼されていない監査スライドを生徒用デッキに追加しない。公開リポジトリへ作業記録を無断で追加しない。再開時は仕様・原稿・PPTX・画像・検査の版と未確認項目を確認する。

プロンプトだけの更新では、対象文書と依存規則、既存内容の保持、変更差分、参照先、保存結果を検証する。デッキ生成・レンダリング・クリック再生は対象外であり、実施済みと報告しない。

この追記は既存検査の必須適用を強化する制作手順である。新しい自動納品遮断機能を実装したこと、既存デッキを修正したこと、将来の違反ゼロの技術的保証を意味しない。

---

This fork adds a **strict classroom-production layer** on top of the upstream consulting PPTX skill.

When the requested output is a **lesson, classroom, school, student-facing, English-teaching, grammar, vocabulary, reading, quiz, exam-review, or teaching PowerPoint**, Classroom Mode is mandatory.

## Files to read before producing a classroom deck

Read in this order:

1. `CLASSROOM.md`
2. `references/classroom-hard-gates-v3.md`
3. `references/classroom-slide-rules.md`
4. `references/classroom-rendering-stability.md`
5. `references/classroom-english-line-balance.md`
6. `references/classroom-delivery-contract.md`
7. `references/classroom-visual-qa-v3.md`
8. `references/slide-rules.md`

If the user says **flowchart / フローチャート / decision tree / 判断フロー**, also read:

- `references/classroom-flowchart-rules.md`

Classroom rules override generic consulting-layout preferences whenever they conflict.

## Non-negotiable completion rule

**Never call a classroom deck complete only because the PPTX opens or because the XML is valid.**

A classroom PPTX may be delivered as a finished file only after all of the following are true:

1. Source material has been checked for content fidelity.
2. The draft has been normalized with `scripts/normalize_classroom_style.py` unless the user explicitly requested visible text borders.
3. `scripts/check_deck.py` exits 0.
4. `scripts/check_classroom_hard_gates.py` exits 0 in the correct profile.
5. `scripts/check_classroom_english_balance.py` exits 0 for English-teaching/classroom decks.
6. `scripts/check_classroom_deck.py` exits 0.
7. Every slide has been rendered to PNG.
8. Every PNG has been visually inspected at near-full size, not only as a contact sheet.
9. Every English sentence has been visually checked for unnatural 2-line wrapping, orphan lines, and poor left/right balance.
10. The visual review has no unresolved high- or medium-severity issue.
11. After any fix, the entire deck has been rendered again.
12. `scripts/check_classroom_delivery.py` passes using the final machine-QA JSON and final visual-QA JSON.

If any of these steps cannot be executed, **do not describe the file as “完成版”, “確認済み”, “PASS”, or equivalent**. State that it is unverified and continue fixing with the tools that are available.

## Default classroom contract

Unless the user explicitly says otherwise:

- Every content slide must include substantive speaker notes.
- Classroom slides are click-driven: content is revealed in teaching order.
- Exercise/quiz slides must not show the answer at initial display.
- Cover title is at least 54pt; normal titles are at least 38pt.
- Normal body text is at least 24pt; short labels are at least 22pt.
- Important English text is at least 28pt and visually dominant.
- Body text is never shrunk to rescue a crowded layout.
- Rendered appearance is authoritative over PPTX coordinates.
- **Text containers are borderless by default.** Titles, body text, English examples, Japanese translations, explanations, answers, hints, and ordinary comparison blocks use `no line`.
- A pale fill may be used for grouping, but do not add an outline around it by default.
- Decorative “text + rectangle border” cards are not part of the default classroom visual language.
- English sentences stay on one line when they comfortably fit. If they need two lines, break at a semantic boundary and avoid a visibly short orphan line.
- A two-line English example is suspicious when one line is much shorter than the other; do not accept it only because the text technically fits.
- Never shrink English merely to force one line; widen/reflow/rebreak the layout first.

For generated classroom PPTX, run:

```bash
python3 scripts/normalize_classroom_style.py path/to/deck.pptx --in-place
python3 scripts/check_classroom_english_balance.py path/to/deck.pptx --json english-balance.json
```

before final visual acceptance. The balance checker catches explicit orphan/function-word breaks and warns about likely ragged automatic wraps, but rendered PNG review remains mandatory.

If a visible border is semantically necessary, name the shape with one of these prefixes so the exception is explicit and auditable:

- `FLOW_`
- `NODE_`
- `TABLE_`
- `AXIS_`
- `VENN_`
- `DIAGRAM_`
- `UI_`

Do not use those prefixes merely to bypass the borderless policy.

Use `--allow-static` only when the user explicitly asks for no click animation.
Use `--notes-optional` only when the user explicitly says speaker notes are unnecessary.

## English line-balance acceptance rule

For English-teaching decks, inspect each rendered English example as typography, not only as text content.

Reject or revise when:

- a sentence that could comfortably fit on one line is broken into two lines,
- a two-line sentence leaves only one or two words on either line,
- the short line is roughly less than 40% of the long line without a strong semantic reason,
- a line ends after a function word such as `to`, `the`, `of`, `would`, `could`, or `might`,
- a subject or auxiliary cluster such as `If I` / `I would` is stranded,
- left/right comparison examples have obviously mismatched vertical rhythm.

Prefer semantic boundaries over mechanically equal character counts. If meaning and visual balance conflict, preserve meaning first and redesign the box/layout rather than forcing an awkward break.

## Flowchart requests

For any flowchart/decision-tree request, use `--profile flowchart` or allow `--profile auto` to infer it from the filename/cover. A flowchart request is not satisfied by a row or grid of rounded cards connected by decorative lines. The deck must have a persistent decision spine, explicit branch conditions, directional arrows, and branch zooms.

Node boundaries may be visible when the boundary itself communicates the decision structure. Ordinary English/Japanese explanatory text around the flowchart remains borderless.

## GitHub Actions reporting rule

A green workflow is **not** evidence that a deck passed if the actual deck-QA step was skipped because no PPTX was present.

Never say “GitHub Actions checked the deck” unless the workflow logs show that the specific PPTX went through:

- general machine QA,
- classroom hard-gate QA,
- English line-balance QA,
- classroom layout QA,
- rendering,
- artifact generation.

If Actions cannot access a local/user-uploaded PPTX, run the same scripts locally and clearly say that this was the local equivalent, not Actions.
