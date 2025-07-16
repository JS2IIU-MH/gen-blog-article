# Gutenbergブロック変換CLIアプリ README

## 概要

このアプリは、Markdown文書をWordPress Gutenbergブロック構文へ変換するPython製CLIツールです。ブロック構文の定義はYAMLファイルで管理し、仕様変更にも柔軟に対応できます。

## インストール

1. リポジトリをクローンまたはダウンロード
2. 必要なPythonパッケージをインストール

```bash
pip install -r requirements.txt
```

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

#### 3. ブロック定義ファイルの指定

```bash
python src/main.py -f articles/sample.md --block-def block-defs.yaml
```

## 変換結果

- 変換後のファイルは元ファイル名に「_gb」を付与し、元ファイルと同じディレクトリに保存されます。
  - 例: `sample.md` → `sample_gb.md`

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

## 対応Markdown要素一覧

| Markdown記法例 | 変換後のGutenbergブロック |
| --- | --- |
| `# タイトル` | `<!-- wp:title -->...<!-- /wp:title -->`（記事タイトル） |
| `## 見出し2` | `<!-- wp:heading {"level":2} -->...<!-- /wp:heading -->` |
| `### 見出し3` | `<!-- wp:heading {"level":3} -->...<!-- /wp:heading -->` |
| `#### 見出し4` | `<!-- wp:heading {"level":4} -->...<!-- /wp:heading -->` |
| `##### 見出し5` | `<!-- wp:heading {"level":5} -->...<!-- /wp:heading -->` |
| `> 引用文` | `<!-- wp:quote -->...<!-- /wp:quote -->` |
| `- 箇条書き`<br>`* 箇条書き` | `<!-- wp:list -->...<!-- /wp:list -->`（ulist） |
| `1. 番号付き` | `<!-- wp:list {"ordered":true} -->...<!-- /wp:list -->`（olist） |
| <code>```python<br>print("hi")<br>```</code> | `<!-- wp:code {"language":"python"} -->...<!-- /wp:code -->`（Code Block Pro対応） |
| `| テーブル |` | `<!-- wp:table -->...<!-- /wp:table -->` |
| 数式（例: `$...$`や`$$...$$`） | `<!-- wp:math -->...<!-- /wp:math -->` |
| 通常のテキスト | `<!-- wp:paragraph -->...<!-- /wp:paragraph -->` |

## テスト

テストは `src/tests/` ディレクトリに配置されています。

```bash
python -m unittest src/tests/test_converter.py
python -m unittest src/tests/test_block_def_loader.py
```

## 拡張・カスタマイズ

このアプリは柔軟な拡張・カスタマイズが可能です。以下に主なファイルごとに、どのような変更を加えることで機能追加や仕様変更ができるかを具体例とともに説明します。

### 1. `block-defs.yaml`（ブロック定義ファイル）

- **役割**: Markdown要素とGutenbergブロックの対応ルールを定義します。
- **カスタマイズ例**:
  - **新しいブロックの追加**: 例えば「アラート」ブロックを追加したい場合、
    ```yaml
    alert:
      pattern: "<!-- wp:alert -->\n{content}\n<!-- /wp:alert -->"
    ```
    と追記し、`converter.py`で`alert`に対応する変換処理を追加します。
  - **既存ブロックの書式変更**: 例えば段落ブロックのHTMLコメントをカスタマイズしたい場合、`paragraph`の`pattern`を書き換えます。

### 2. `src/converter.py`（変換ロジック）

- **役割**: MarkdownテキストをGutenbergブロック構文へ変換します。
- **カスタマイズ例**:
  - **新しいMarkdown構文への対応**: 例：`!!! note` で始まる行を「アラート」ブロックに変換したい場合、
    ```python
    elif line.startswith('!!! note'):
        pattern = block_defs.get('alert', {}).get('pattern', '{content}')
        result.append(pattern.replace('{content}', line[9:].strip()))
    ```
    のように分岐を追加します。
  - **既存変換ルールの強化**: 例：リストやテーブルの変換ロジックをより厳密にしたい場合、該当部分の処理を詳細化します。

### 3. `src/file_utils.py`（ファイル入出力ユーティリティ）

- **役割**: ファイルの読み書きやファイル名生成などを担当します。
- **カスタマイズ例**:
  - **出力ファイル名のルール変更**: 例：`_gb`ではなく`_gutenberg`を付与したい場合、
    ```python
    gb_name = f"{name}_gutenberg{ext}"
    ```
    のように修正します。
  - **出力先ディレクトリの変更**: 変換後ファイルを別ディレクトリに保存したい場合、`gb_path`の生成ロジックを変更します。

### 4. `src/main.py`（CLIエントリポイント）

- **役割**: コマンドライン引数の解析や全体の処理フローを制御します。
- **カスタマイズ例**:
  - **新しいオプションの追加**: 例：変換後に自動でファイルを開く`--open`オプションを追加したい場合、`argparse`の設定と処理フローに該当ロジックを追加します。
  - **バッチ処理やログ出力の追加**: 複数ディレクトリ対応や詳細なログ出力など、全体の制御を拡張できます。

### 5. テストコード（`src/tests/`）

- **役割**: 変換ロジックやユーティリティの動作確認・自動テスト。
- **カスタマイズ例**:
  - **新しい変換仕様のテスト追加**: 例：アラートブロック変換のテストを追加する場合、
    ```python
    def test_alert(self):
        block_defs = {'alert': {'pattern': '<!-- wp:alert -->\n{content}\n<!-- /wp:alert -->'}}
        md = '!!! note 重要なお知らせ'
        result = convert_markdown_to_gutenberg(md, block_defs)
        self.assertIn('<!-- wp:alert -->', result)
    ```
    のようにテストケースを追加します。
