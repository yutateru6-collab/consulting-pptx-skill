# 入力画像の説明パネルを再生成してPPTXに貼る手順

入力画像を元に教材PPTXを作る場合の納品条件。「これでパワポ」も含む。`SKILL.md` の「入力画像からPPTXを作る依頼」を先に読む。画像を参照のみ／無加工で使うというユーザーの明示指示は優先する。

## 実作業

1. 元画像を開き、**見出し・説明文・英文・図・表・矢印・枠が一緒になった説明領域**を選ぶ。四辺を `[left, top, right, bottom]` で記録し、元の画素から切り抜く。キャラクターや小物だけの切り抜きは説明パネルの代わりにならない。
2. **切り抜きファイルそのもの**を画像生成・編集ツールの参照に渡す。配色、レイアウト、文字の強弱、図表の位置関係を保ち、表示寸法の縦横2倍以上を目安に再生成する。
3. 元画像・切り抜き・再生成PNGを並べ、画像内の日本語・英文・記号を一行ずつ照合する。誤字、抜け、余計な文字、文法の誤りがあれば修正して再生成する。必要な訂正は制作メモに残す。
4. 再生成した**説明パネル全体**をPPTXの画像オブジェクトとして内容スライドに大きく貼る。説明部分を図形や文字で置換しない。画像外の追加文字は、元画像に似合うポップな日本語フォントを選び、投影して読める大きさにする。人物や小物の画像は補助として使ってよい。
5. manifestを作り、`python3 scripts/check_source_images.py deck.pptx image-manifest.json` を実行する。Pillowが未導入なら `python3 -m pip install Pillow`。検査は切り抜きの画素一致、再生成PNGの埋め込み、説明パネルが各内容スライドの面積の30%以上を占めること、表示枠に対する画像画素数を確認する。
6. 全スライドを画像化して、**説明パネル自体の文字が読めるか**、画像外の文字が元の雰囲気に合うかを目視する。機械検査と目視の双方を通るまで完成としない。

manifestのパスはmanifestファイルからの相対パス、または絶対パス。`source_crop_box` は右端・下端を含まない画素範囲。`content_slides` に表紙以外の全内容スライド番号（1始まり）を列挙する。各内容スライドに `role: "explanation_panel"` の画像が必要。`role: "illustration"` は補助画像であり、条件を満たさない。

```json
{
  "source_image": "input/reference.jpeg",
  "content_slides": [2, 3],
  "assets": [
    {
      "name": "basic_explanation",
      "role": "explanation_panel",
      "source_crop_box": [10, 160, 450, 555],
      "source_crop_file": "assets/source_crops/basic_explanation.png",
      "regenerated_png": "assets/regenerated/basic_explanation.png",
      "slides": [2]
    },
    {
      "name": "choice_flow",
      "role": "explanation_panel",
      "source_crop_box": [460, 160, 1110, 555],
      "source_crop_file": "assets/source_crops/choice_flow.png",
      "regenerated_png": "assets/regenerated/choice_flow.png",
      "slides": [3]
    }
  ]
}
```

機械検査は画像生成の過程、絵柄の一致、説明内容の正確さを証明できない。制作担当者が三者を並べて照合し、各内容スライドで説明パネルが主役になっていることを目視する。満たせないときは未完成と報告する。
