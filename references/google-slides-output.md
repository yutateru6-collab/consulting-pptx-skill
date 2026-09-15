# Google Slides Output — Classroom / Education Mode

Google Slidesを最終成果物に含める場合の出力規則。

## 1. 基本方針

Google Slidesは「PPTXのついでのコピー」ではなく、**編集可能性と実表示を別々に検証する出力ターゲット**として扱う。

- PPTXのQA結果だけでGoogle Slides版をPASSにしない。
- Google Slidesへ変換した後、ページ数・文字・配置を再確認する。
- Google Slides版で崩れた場合は、PPTX側が正しいことを理由に放置しない。

## 2. 推奨経路

### A. Google Drive / Slides connectorが使える環境

最終PPTXをGoogle Driveへアップロード・Google Slides化し、Google側のファイルを読み戻して確認する。

### B. CLI / CI

```bash
pip install -r requirements-google-slides.txt
python3 scripts/upload_pptx_to_google_slides.py deck.pptx \
  --title "Tense Lesson" \
  --expected-slides 10 \
  --json google-upload.json
```

認証はApplication Default Credentialsを使う。たとえばローカルでは `gcloud auth application-default login`、CIでは適切に権限を付与した認証情報を用いる。

## 3. Google Slidesの段階表示

Google Slides APIの公開 `batchUpdate` request群は、スライド・テキスト・図形・表・変形等の作成/更新を扱うが、PowerPointのon-click buildと同じアニメーション作成を前提にしない。

したがって授業用の段階提示は次の優先順位とする。

1. **`duplicate-slides`** — 推奨。1クリック状態ごとにほぼ同じスライドを複製し、次の要素を追加する。
2. `static` — 配布・復習用。段階表示を使わない。
3. `import-pptx` — PowerPointをGoogle Slidesへ変換する。変換後に動作・表示を再確認し、PowerPointと同等と仮定しない。

Education Storyboardでは `meta.googleSlidesBuildMode` に上記を指定する。

## 4. duplicate-slides の作り方

例: 1枚のPowerPointで4クリックある場合

```text
G5a 問題だけ
G5b + 手がかり
G5c + 正解
G5d + 理由
```

- タイトル位置・英文位置を動かさない。
- 追加される情報だけ増やす。
- スライド番号を生徒画面に出す場合、a/b/cの内部状態が見えないよう通常番号を維持する。
- 同じページの段階状態で背景や配色を変えない。

## 5. Drive変換

Google Drive APIはMicrosoft PowerPointをGoogle Slidesへインポート変換できる。`scripts/upload_pptx_to_google_slides.py` は、PPTX MIME typeでメディアを送り、作成先MIME typeをGoogle Slidesにして変換する。

スクリプトは変換後にGoogle Slides APIでページ数を読み戻し、`--expected-slides` が与えられた場合は一致を確認する。

## 6. Google版QA

最低限:

- スライド数一致
- タイトル欠落なし
- 英文欠落なし
- 日本語文字化けなし
- 図形/画像の大きな欠落なし
- 重要英文の不自然な改行なし
- 文字の重なりなし
- duplicate-slidesなら各段階で位置がジャンプしない

可能ならGoogle Slidesのサムネイル/書き出し画像を取得し、PPTX版とは別に全ページ目視する。

## 7. 公式仕様の確認先

- Drive import/upload: https://developers.google.com/workspace/drive/api/guides/manage-uploads
- Slides API overview: https://developers.google.com/workspace/slides/api/guides/overview
- Slides batchUpdate: https://developers.google.com/workspace/slides/api/reference/rest/v1/presentations/batchUpdate

API仕様は変わり得るため、実装変更時は公式ドキュメントを再確認する。
