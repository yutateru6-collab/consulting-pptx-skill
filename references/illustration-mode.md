# Illustration Mode — 授業用イラスト設計ルール

この文書は Classroom / Education スライドにイラスト・画像・SVG・アイコンを追加するときの正典である。

## 1. まず「必要か」を判定する

イラストは次のどれかを改善するときだけ使う。

- **concretize**: 抽象概念を具体的な場面にする
- **contrast**: 2つの意味・状態・選択を比べる
- **sequence**: 時間・手順・変化を追わせる
- **orient**: どこを見ればよいか視線を導く
- **motivate**: 導入場面で問題意識を作る
- **signal**: 重要ポイントを短く視覚合図する
- **retrieve**: 生徒が思い出すための手がかりを与える

「空いている」「かわいい」「映える」だけなら `omit`。

## 2. Cognitive Anchor Rule

各セクションで最も理解が切り替わる箇所を優先して視覚化する。全ページを同じ密度でイラスト化しない。

優先順位の高い例:

1. 初めて意味が変わる場面
2. 誤解しやすい対比
3. 時間・状態・因果の変化
4. ルールの適用場面
5. 学習者が誤答しやすいポイント

## 3. 英語授業向けVisual Role

### `scene`
例文の意味を一目で理解するための場面。時制、進行形、語彙、前置詞に向く。

### `comparison`
A/Bを同じ画面条件で比較する。現在形 vs 現在進行形、過去形 vs 現在完了など。

### `timeline-context`
時間軸そのものが主役ではなく、場面+時間関係を示す補助イラスト。

### `concept-metaphor`
抽象文法を記憶しやすい物理的な比喩へ変換する。意味を歪める比喩は使わない。

### `process`
読み方・判断・変形の順序を視覚化する。

### `mascot-cue`
継続キャラが「考える」「比較する」「注意する」等の意味ある行動を行う。立っているだけは禁止。

### `icon-support`
短いラベルを補助する小アイコン。アイコンだけで意味を伝えない。

### `diagram-support`
図解の理解を補助する挿絵。必須ラベルはネイティブテキストで置く。

## 4. 標準レイアウト

### text-left-visual-right
- text zone: x=0.05〜0.58 程度
- visual zone: x=0.64〜0.95 程度
- 主役英文はtext zone内で最大幅を確保する

### visual-left-text-right
- visual zone: x=0.05〜0.38 程度
- text zone: x=0.43〜0.95 程度
- 導入場面や語彙場面に向く

### paired-scenes
- 左右の画像サイズ・視点・余白を揃える
- 「片方だけ大きい」「片方だけ詳細」にならない
- 比較ラベルは画像へ焼き込まず上部にネイティブ文字で置く

### scene-plus-takeaway
- 絵を広めに使う代わりに説明文を減らす
- 画面下の結論は1文程度
- 詳細説明はスピーカーノートへ

### margin-mascot
- キャラは外側余白に置く
- 本文幅を削りすぎない
- 1スライド内でキャラの占有面積は目安25%以下

### micro-icon-support
- 小アイコンはラベルに近接させる
- 1枚に大量の異なるアイコンを散らさない

## 5. 画像生成プロンプトの原則

画像生成を使う場合、プロンプトには最低限以下を含める。

- educational purpose / core idea
- scene or action
- style family
- aspect ratio / composition
- background requirement
- text-free unless text is explicitly nonessential
- space direction: `leave clean negative space on the left/right for slide text`
- recurring character reference if applicable

重要英文・和訳・答え・文法ラベルを画像生成に書かせない。生成画像内の文字は誤字・編集不能・表示崩れの原因になる。

## 6. Style Lock

デッキ全体で以下を固定する。

- line style / rendering style
- character proportions
- saturation level
- outline thickness
- shadow treatment
- background treatment

推奨styleFamily例:

- `clean-flat-education`
- `soft-editorial`
- `simple-anime-classroom`
- `hand-drawn-explainer`
- `minimal-vector`

同じデッキで `photorealistic` と `cute-flat` と `manga` を混在させない。例外が必要なら `styleExceptionReason` をIllustration Planへ書く。

## 7. Character Consistency

継続キャラを使う場合:

- 1枚のmaster/model sheetをsingle source of truthにする
- reference path / IDをIllustration Planへ記録する
- 顔・髪/毛・服・色・体型・主要アクセサリを固定する
- 変えるのはポーズ、表情、カメラ角度、場面小物に限定する
- キャラの存在より「何をしているか」を優先する

## 8. Asset Source / Rights

外部素材を使う場合、最低限次を記録する。

- provider
- source URL
- license / usage rights
- local path
- alt text

利用条件が不明なら完成素材として使わない。

画像生成物でも、生成元・生成日・使用モデル/ツールを制作記録に残せるなら残す。

## 9. Text-safe Placement

通常イラストは `textSafeZone` と交差させない。

- 画像と文字の間は最低0.12 inch、推奨0.18 inch以上
- 主役英文の横では0.18 inch以上を優先
- 画像の細かい突起やキャラの手足まで文字へ接触させない
- 文字が画像の上に乗るデザインはClassroom Modeでは原則避ける

背景/全面画像を使う場合だけ例外。ただし背景画像は `BG_` / `FULLBLEED_` / `DIAGRAM_BG_` など明示名にし、コントラストを画像QAで確認する。

## 10. Density Rule

- 原則1枚1 hero visual
- 小アイコンはhero visualに数えないが、増やしすぎない
- 3カラム + 3長文 + 大イラストは不可
- 2つ以上の長い英文を見せるページは、まず英文スペースを優先する
- イラストを入れるために28pt未満へ英語を縮めない

6枚以上のデッキでほぼ全ページにhero visualがある場合、`visual wallpaper`化していないか再検討する。

## 11. Essential Information Rule

画像の中だけに存在してはいけないもの:

- 正解
- 問題文
- 重要英文
- 和訳
- 数値
- 軸ラベル
- 凡例
- 文法の定義
- 授業進行に必要な指示

これらはPowerPoint/Google Slidesのネイティブ要素で置く。

## 12. Render QA

構造上安全でも、最終PNGで以下があればFAIL。

- キャラの一部が英文へかぶる
- 画像が主役英文より目立つ
- 絵の背景色で文字コントラストが落ちる
- 画風が別ページだけ急に変わる
- cropで重要な人物/物体が切れる
- 画像が低解像度で投影時に粗い
- 装飾が多く、何を見ればよいか分からない

## 13. 参考にした公開実装

- `wshobson/agents` の `pptx-visual-assets`: provenance、bbox、aspect ratio、native labels
- `lgwanai/ppt-skill`: illustration search、教育カテゴリ、SVG色調整
- `AppajiDheeraj/paper-engine-illustrations`: cognitive anchors、visual shot list、recurring-character consistency

本リポジトリではこれらをそのままコピーせず、Classroom / Education Hard Gatesに合う形で独自に再構成する。
