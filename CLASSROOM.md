# Classroom PPTX Mode — 高校授業用の優先ルール

このForkでは、通常のコンサル型スライド規約に加えて、**教室で生徒がスクリーンを見て理解・参加できる授業PowerPoint**を作るための Classroom Mode を持つ。

## 優先順位

高校・中学の授業用スライドでは、ルールの優先順位を次のようにする。

1. `references/classroom-slide-rules.md`
2. ユーザーが今回指定した授業要件
3. `references/slide-rules.md`
4. 型カタログ・テンプレート

つまり、コンサル資料の一般ルールと授業上の見やすさが衝突した場合は、**授業上の見やすさを優先する**。

## Classroom Mode の標準フロー

1. 教材・教科書・問題集など一次資料を読む。
2. 1枚1役割で授業ストーリーを設計する。
3. 大きな文字で編集可能PPTXを作る。
4. クリック式の場合は、問題 → ヒント → 正解 → 理由の順で on-click 表示を作る。
5. `scripts/check_deck.py` を実行する。
6. `scripts/check_classroom_deck.py` を実行する。
7. **PPTXをPDF→PNGへレンダリングする。**
8. 全ページPNGとコンタクトシートを実際に見る。
9. `references/classroom-visual-qa-prompt.md` の観点で視覚レビューする。
10. 問題が1件でもあれば、生成元を修正して再生成 → 再レンダリングする。
11. 最終版のみ納品する。

## ローカルQA

```bash
pip install python-pptx pillow
python3 scripts/check_deck.py path/to/deck.pptx
python3 scripts/check_classroom_deck.py path/to/deck.pptx --json classroom-qa.json
```

LibreOffice と poppler-utils がある環境では：

```bash
bash scripts/render_classroom_deck.sh path/to/deck.pptx qa-output
```

これにより、PDF、全ページPNG、`contact-sheet.png` が生成される。

## GitHub Actions

`.github/workflows/classroom-pptx-qa.yml` を手動実行し、`qa-input/` に置いたPPTXを検査できる。Actionsは次を行う。

- 一般機械QA
- Classroom QA
- LibreOfficeでPDF化
- 144dpiで全ページPNG化
- コンタクトシート生成
- QA結果・PDF・PNGをArtifact保存

**Actionsの成功だけで完成扱いにしない。** ArtifactのPNGを人間またはVision対応レビューで必ず確認する。

## 改善を蓄積する

実際の授業デッキで新しい失敗パターンが見つかったら、`references/classroom-failure-log.md` に追加する。
再発防止できるものは、次のどちらかに昇格させる。

- 生成ルール → `references/classroom-slide-rules.md`
- 機械検出 → `scripts/check_classroom_deck.py`

「一度起きた失敗を、次回から仕組みで防ぐ」ことをこのForkの基本方針とする。
