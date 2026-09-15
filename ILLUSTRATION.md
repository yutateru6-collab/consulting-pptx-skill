# ILLUSTRATION MODE — 授業スライドにイラストを自然に入れる

このモードは Classroom Mode / Education Mode に追加する**視覚設計レイヤー**である。目的は「空いている場所に絵を置く」ことではなく、**理解を助けるページだけに、意味のあるイラストを、文字と競合しない位置へ置く**こと。

## 発動条件

次のいずれかに当てはまるとき適用する。

- ユーザーが「イラスト」「挿絵」「画像」「キャラ」「マスコット」「SVG」「アイコン」「visual」を求めた
- 英語の場面・状態・対比・時系列・抽象概念を、絵にすると理解が明確に上がる
- Education Storyboard の中に visual anchor が必要なページがある

**全ページへ均等に絵を配らない。** 絵がなくても理解できるページは `omit` を選ぶ。

## 必読

- `skills/classroom-illustration/SKILL.md`
- `references/illustration-mode.md`
- `references/classroom-layout-safety.md`

## 生成前ゲート: Illustration Plan

Education Storyboard の後、レイアウトを作る前に `illustration-plan.json` を作る。

テンプレート:

- `templates/illustration-plan.example.json`

各スライドで最低限、次を決める。

- `decision`: `use` / `omit`
- `role`: scene / comparison / concept-metaphor / timeline-context / process / mascot-cue / icon-support / diagram-support
- `learningFunction`: concretize / contrast / sequence / orient / motivate / signal / retrieve
- `layout`
- `bbox`: イラスト専用領域
- `textSafeZone`: 文字専用領域
- `styleFamily`
- `altText`
- `source` / rights
- 画像生成する場合は `prompt`
- 継続キャラを使う場合は `recurringCharacter.reference`

検査:

```bash
python3 scripts/check_illustration_plan.py illustration-plan.json --json illustration-plan-qa.json
```

**FAILが1件でもあれば画像生成・スライド配置へ進まない。**

## 最重要ルール

1. **Decoration-first禁止** — 「寂しいから」「余白があるから」は採用理由にならない。
2. **Seat-first** — イラストは後からねじ込まず、文章を配置する前に専用の席を確保する。
3. **Text-safe** — 主役英文・和訳・説明・選択肢の上にイラストを重ねない。
4. **One hero visual** — 原則1スライド1主役イラスト。小アイコンは例外。
5. **Style lock** — 同一デッキで画風を揺らさない。例外は理由を明示する。
6. **No baked essential text** — 学習上必要な英文・和訳・数値・凡例は画像へ焼き込まず、編集可能なPowerPoint/Google Slides要素で置く。
7. **Preserve aspect ratio** — 画像を縦横に引き伸ばさない。fit または意図した crop-to-fill を使う。
8. **Character consistency** — 継続キャラはモデルシート/参照画像を固定し、毎回別人にしない。
9. **Provenance** — 外部素材はURL/提供元/利用条件が不明なら使わない。
10. **Render truth** — 座標上安全でも、最終PNGで文字と絵が接触したらFAIL。

## 英語授業で優先する使い方

- **時制・進行・完了**: 場面や状態の違いを scene / comparison で見せる
- **現在完了 vs 過去形**: 「過去の出来事」対「今につながる状態」の視覚対比
- **可算/不可算**: 個体として数える物と量として捉える物の対比
- **前置詞**: 空間関係を1枚の簡潔な場面で見せる
- **仮定法**: reality / imagined world の左右対比
- **語彙**: 単語の意味をそのまま絵にするより、文脈場面で使う
- **長文**: 全段落に絵を付けず、構造転換・因果・対比などの認知アンカーだけに使う

## 自然に見える標準レイアウト

- `text-left-visual-right` — 本文55〜60%、絵35〜40%
- `visual-left-text-right` — 絵35〜40%、本文55〜60%
- `paired-scenes` — 2場面の比較。左右の構図・サイズを揃える
- `scene-plus-takeaway` — 大きめの場面 + 短い結論。説明文を詰め込まない
- `margin-mascot` — キャラは外側余白に置き、本文へ侵入しない
- `micro-icon-support` — ラベル理解を補助する小アイコン。主役にしない

3カラムの高密度説明ページでは、大きいイラストを追加しない。まず2カラム化・分割を検討する。

## PPTX生成後のVisual Asset QA

イラスト・写真・SVG等を含むPPTXでは次を実行する。

```bash
python3 scripts/check_classroom_visual_assets.py deck.pptx --json visual-assets-qa.json
```

このcheckerは少なくとも以下を検査する。

- 画像がスライド外へ出ていないか
- 通常イラストが文字領域へ重なっていないか
- 文字との安全距離が不足していないか
- cropなし画像を不自然に縦横変形していないか
- 1枚に大きな画像を置きすぎていないか

`BG_` / `FULLBLEED_` / `DIAGRAM_BG_` で始まる画像は意図的な背景として扱えるが、**文字とのコントラストは機械判定だけで完成扱いにしない**。最終PNGを必ず目視する。

## 外部プロジェクトから取り入れた設計思想

この実装は、公開されている以下のプロジェクトの考え方を参考にしつつ、高校英語授業向けに再設計している。

- `wshobson/agents` / `pptx-visual-assets` — asset provenance、明示bbox、縦横比、画像とテキストの役割分離
- `lgwanai/ppt-skill` — ローカルイラスト検索、教育カテゴリ、SVGのテーマ色調整
- `AppajiDheeraj/paper-engine-illustrations` — cognitive anchor、shot list、継続キャラ、装飾だけの絵を避ける考え方

外部コードや素材をそのままコピーすることを前提にしない。素材を取り込む場合は、その素材自身のライセンスと出典を個別に確認する。
