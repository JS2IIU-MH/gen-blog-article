import argparse
import sys
from file_utils import save_converted_file
from converter import convert_markdown_to_gutenberg
from block_def_loader import load_block_defs


def main():
    parser = argparse.ArgumentParser(description="Markdown→Gutenbergブロック変換CLI")
    parser.add_argument('-f', '--file', help='変換するMarkdownファイル')
    parser.add_argument('-d', '--dir', help='変換するMarkdownファイルがあるディレクトリ')
    parser.add_argument('--block-def', default='./block-defs.yaml', help='ブロック定義ファイルパス')
    args = parser.parse_args()

    block_defs = load_block_defs(args.block_def)

    if args.file:
        files = [args.file]
    elif args.dir:
        import os
        files = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if f.endswith('.md')]
    else:
        print('ファイルまたはディレクトリを指定してください')
        sys.exit(1)

    for file_path in files:
        with open(file_path, encoding='utf-8') as f:
            md_text = f.read()
        gb_text = convert_markdown_to_gutenberg(md_text, block_defs)
        save_converted_file(file_path, gb_text)

if __name__ == "__main__":
    main()
