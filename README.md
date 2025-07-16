# Gutenbergブロック変換CLIアプリ README

## 概要

このアプリは、Markdown文書をWordPress Gutenbergブロック構文へ変換するPython製CLIツールです。ブロック構文の定義はYAMLファイルで管理し、仕様変更にも柔軟に対応できます。

---

## インストール

1. リポジトリをクローンまたはダウンロード
2. 必要なPythonパッケージをインストール

```bash
pip install -r requirements.txt
```

---

## 使い方

### 基本的な実行例

#### 1. ファイル指定で変換
```bash
python src/main.py -f articles/sample.md
```

#### 2. ディレクトリ内の全Markdownファイルを変換
```bash
python src/main.py -d articles/
```

#### 3. tkinterダイアログでファイル選択
```bash
python src/main.py --dialog
```

#### 4. ブロック定義ファイルの指定
```bash
python src/main.py -f articles/sample.md --block-def block-defs.yaml
```

---

## 変換結果

- 変換後のファイルは元ファイル名に「_gb」を付与し、元ファイルと同じディレクトリに保存されます。
  - 例: `sample.md` → `sample_gb.md`

---

## ブロック定義ファイル（YAML例）

`block-defs.yaml` で各Markdown要素のGutenbergブロック構文を定義します。

```yaml
heading:
  pattern: "<!-- wp:heading -->\n{content}\n<!-- /wp:heading -->"
paragraph:
  pattern: "<!-- wp:paragraph -->\n{content}\n<!-- /wp:paragraph -->"
table:
  pattern: "<!-- wp:table -->\n{content}\n<!-- /wp:table -->"
code:
  pattern: "<!-- wp:code -->\n{content}\n<!-- /wp:code -->"
math:
  pattern: "<!-- wp:math -->\n{content}\n<!-- /wp:math -->"
```

---

## テスト

テストは `src/tests/` ディレクトリに配置されています。

```bash
python -m unittest src/tests/test_converter.py
python -m unittest src/tests/test_block_def_loader.py
```

---

## 拡張・カスタマイズ

- ブロック構文の追加・変更は `block-defs.yaml` を編集するだけで可能です。
- 変換ロジックの拡張は `src/converter.py` を編集してください。

---

## ライセンス

MIT License
