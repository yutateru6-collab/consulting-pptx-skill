# Classroom PPTX QA 運用ガイド

## 目的

一般的なPPTX機械検査では拾いにくい「授業で見た瞬間に分かる崩れ」を減らす。

代表例：

- タイトル最後の1文字だけ改行
- 群動詞など短いラベルの2行化
- 文字化け
- 文字サイズとボックスサイズの不釣り合い
- クリック順の破綻

## 手元で実行

```bash
python3 -m pip install python-pptx pillow
python3 scripts/check_deck.py mydeck.pptx
python3 scripts/check_classroom_deck.py mydeck.pptx --json qa/classroom.json
```

レンダリング：

```bash
# Ubuntu/Debian
sudo apt-get install libreoffice poppler-utils fonts-noto-cjk fonts-liberation
bash scripts/render_classroom_deck.sh mydeck.pptx qa/rendered
```

出力：

```text
qa/rendered/
├─ pdf/
│  └─ mydeck.pdf
├─ png/
│  ├─ slide-01.png
│  └─ ...
└─ contact-sheet.png
```

## GitHub Actions

1. `qa-input/` に確認したいPPTXを置く。
2. GitHubの **Actions → Classroom PPTX QA → Run workflow** を開く。
3. 特定ファイルだけなら `pptx_path` を入力する。
4. 完了後、Artifact `classroom-pptx-qa` を開く。
5. `contact-sheet.png` で全体を見たあと、`png/` の各ページを1枚ずつ確認する。

## 判定

- `scripts/check_deck.py` FAIL 0
- `scripts/check_classroom_deck.py` FAIL 0
- 全ページPNGの視覚QAで重大問題0

の3条件を満たして初めて完成。

## 今後の発展

- VisionモデルによるPNG自動レビュー
- self-hosted Windows runner + Microsoft PowerPointでの実機レンダリング
- 過去のFAIL画像を回帰テスト用fixtureにする
- タイトル・ラベルの実フォント幅計測を導入する
