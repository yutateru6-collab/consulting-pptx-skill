# Education Mode — 学習設計ルール

主方式は [`../PRESENTATION_MODES.md`](../PRESENTATION_MODES.md) で選ぶ。以下の新規練習・retrievalを含む授業設計は主に `classroom-editable` に適用する。`source-image-click` / `content-image-click` で原本／入力内容を再構成する場合、説明順・学習上の正確さを保ちつつ未依頼の課題を追加しない。

対象: 中高生向け英語授業、英文法、語彙、長文、英作文、リスニング、試験解説。

このファイルは見た目ではなく、**何をどの順に理解させ、どこで生徒に思い出させるか**を定める。

## 1. Backward Design

作る順番は以下で固定する。

1. 授業後に生徒が「何をできる」必要があるか決める。
2. その到達を何の問題・発話・判断で確認するか決める。
3. その確認問題を解けるように、説明・例・練習を逆算して並べる。

スライド枚数やデザインから考え始めない。

## 2. 学習目標

目標は観察できる行動で書く。

良い例:

- 時間表現を根拠に現在完了と過去形を選べる。
- if節と主節の形から仮定法過去を見分けられる。
- 可算/不可算を意味と用法から説明できる。
- 長文の各段落から主張と根拠を対応付けられる。

避ける:

- 現在完了を理解する。
- 仮定法を知る。
- 語彙を学ぶ。

Bloomレベルは `remember / understand / apply / analyze / evaluate / create` のいずれかを指定し、確認問題も同じレベル以上にする。

## 3. 前提知識を先に置く

概念をDAGとして考える。

例:

```text
過去形の基本（assumed）
  ↓
「終わった過去」と「今とのつながり」
  ↓
現在完了 vs 過去形
  ↓
問題文からの時制判断
```

- 未習の前提を飛ばさない。
- 既習として扱うものは `assumed: true` と明示する。
- 4〜9概念/1授業程度を目安にする。増えすぎる場合は授業を分ける。

## 4. Motivation / Noticing before Formalism

新しい文法は、原則として「用語・公式」から始めない。

推奨順:

1. 場面・絵・日本語・短い問題
2. 2文の対比
3. 生徒への問い
4. 違いをハイライト
5. ルールを短く言語化

生徒がまだ困っていない段階で、定義だけを先に置かない。

## 5. 具体例は2枚以内

`rule / definition / concept` を提示したら、**2枚以内**に `example / worked-example / guided-practice` を置く。

抽象説明が3枚以上続く構成は原則再設計する。

## 6. Worked Example → We Do → You Do

applyレベルの文法・問題演習は以下を基本形とする。

### I do — Worked Example
教師が判断をすべて見せる。

```text
① 何を見る？
② 手がかりは？
③ どう考える？
④ 答えは？
```

### We do — Guided Practice
教師は答えではなく手がかりだけ出す。

### You do — Independent / Retrieval
説明を消し、生徒が自力で答える。

難易度を上げるより、**足場を少しずつ外す**。

## 7. Retrieval Practice

1回説明して終わらない。

- 新概念の後に一度思い出させる。
- 数枚後にもう一度戻す。
- 最後にexit ticketで再確認する。
- 選択肢を読むだけで答えが分かる認識問題だけでなく、理由・根拠・形を生徒から出させる。

少なくともデッキ全体に `retrieval` または `exit-ticket` を1枚入れる。

## 8. Interleaving / Contrast

混同しやすい項目は別々に長く教えるより、適切な段階で並べて比較する。

例:

- 現在完了 vs 過去形
- will vs be going to
- 動名詞 vs 現在分詞
- 不定詞 vs 動名詞
- 可算 vs 不可算
- Is ...? vs Does ...?

比較スライドでは、違いを色だけで表現せず、**判断軸を1つに固定**する。

## 9. Misconception-first

事前に典型誤答を1〜3個宣言する。

例:

- 「have + 過去分詞 = 昔のこと」とだけ覚える。
- be動詞と一般動詞を同時に使う。
- yesterday があるのに現在完了を選ぶ。

誤答を画面に出す場合は、ただ×を付けず「なぜそう考えたか」を扱う。

## 10. Cognitive Load

- 1枚1役割。
- 画面は生徒の現在の思考だけを支える。
- 教師が口頭で言える説明はノートへ。
- 同じ内容を英文・日本語・箇条書きで三重に重複させない。
- 新しい文法用語、例文、例外、練習を1枚に同時投入しない。
- 図解は装飾ではなく、時間・構造・因果・比較を見せるために使う。

## 11. Education Storyboardのrole

推奨role:

- `hook`
- `objective`
- `retrieval`
- `noticing`
- `rule`
- `definition`
- `concept`
- `example`
- `worked-example`
- `compare`
- `misconception`
- `guided-practice`
- `independent-practice`
- `recap`
- `exit-ticket`
- `quiz`

roleは見た目のテンプレ名ではなく、**その1枚で生徒に何をさせるか**を表す。

## 12. スピーカーノート

各内容スライドのnotesには、最低限次のいずれかを入れる。

- `explanation`
- `teacherPrompt`
- `expectedAnswer`
- `clickOrder`

画面に詳細を詰め込む代わりに教師の進行をノートへ移す。

## 13. 完成判定

Education Modeでは、既存Classroom QAに加えて以下を満たす。

```bash
python3 scripts/check_education_storyboard.py education-storyboard.json --json education-qa.json
```

- FAIL = 0
- 学習目標ごとに確認問題がある
- 前提知識の順序が崩れていない
- rule/definition後2枚以内に具体例がある
- 問題スライドの答えは初期非表示
- retrieval/exit-ticketがある
- 教師ノートがある

Education QAは**PPTXの見た目検査の代替ではない**。両方通す。
