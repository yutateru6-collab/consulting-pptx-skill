# Classroom Delivery Contract — 完成版を名乗る条件

この契約は「完成したように見えるが、実際には未検証」という納品を防ぐ。

## Gate A — Source fidelity

- 教材・教科書・添付ファイルを読んだ。
- 英文・日本語訳・説明がソースと一致している。
- ソースにない内容を勝手に断定していない。

## Gate B — Build

- 16:9
- 編集可能PPTX
- フォント役割が統一
- スピーカーノートあり
- 必要なクリック演出あり

## Gate C — Machine QA

必須：

```bash
python3 scripts/check_deck.py deck.pptx
python3 scripts/check_classroom_deck.py deck.pptx --profile auto --json classroom-qa.json
```

両方 exit 0。

FAILが1件でもあれば完成版ではない。

## Gate D — Render

- PDF化
- 全ページPNG化
- ページ数一致
- contact-sheet生成

## Gate E — Visual QA

`references/classroom-visual-qa-v3.md` で全ページ確認し、`visual-qa.json` を作る。

条件：

- `overall_status = PASS`
- `reviewed_all_slides = true`
- `reviewed_contact_sheet = true`
- `unresolved_high = 0`
- `unresolved_medium = 0`

## Gate F — Re-render

初回QAで1件でも修正した場合：

- 全ページ再レンダリング
- 全ページ再確認
- `rerendered_after_fixes = true`

## Gate G — Delivery checker

```bash
python3 scripts/check_classroom_delivery.py \
  --machine classroom-qa.json \
  --visual visual-qa.json
```

PASSして初めて完成版。

## 報告ルール

最終回答では：

- スライド枚数
- クリック演出概要
- Machine QAのFAIL/WARN数
- Visual QA結果
- 再レンダリング有無
- 参照したForkのcommit SHA

を短く報告する。

## 禁止

- checkerを実行していないのに「PASS」
- PNGを見ていないのに「目視確認済み」
- Actionsでdeck stepがskippedなのに「Actionsで確認済み」
- FAILが残ったまま「完成版」
- LibreOfficeで見ただけなのにPowerPoint実機検証済みと書く
