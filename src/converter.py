def convert_markdown_to_gutenberg(md_text, block_defs):
    lines = md_text.split('\n')
    result = []
    in_code_block = False
    code_lines = []
    code_lang = ''
    in_quote_block = False
    quote_lines = []
    in_list_block = False
    list_lines = []
    in_olist_block = False
    olist_lines = []
    title_set = False
    for line in lines:
        # Code Block Pro対応
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip()
                code_lines = []
            else:
                in_code_block = False
                code_content = '\n'.join(code_lines)
                pattern = block_defs.get('code', {}).get('pattern', '{content}')
                # Code Block Pro: 言語指定があればlanguage属性を付与
                if code_lang:
                    pattern = pattern.replace('<!-- wp:code -->', f'<!-- wp:code {{\"language\":\"{code_lang}\"}} -->')
                result.append(pattern.replace('{content}', code_content))
                code_lang = ''
        elif in_code_block:
            code_lines.append(line)
        # 箇条書き対応
        elif line.lstrip().startswith(('- ', '* ')):
            if not in_list_block:
                in_list_block = True
                list_lines = [line.lstrip()[2:]]
            else:
                list_lines.append(line.lstrip()[2:])
            # 他のブロック終了処理は不要
        elif in_list_block and not line.lstrip().startswith(('- ', '* ')):
            in_list_block = False
            pattern = block_defs.get('ulist', {'pattern': '<!-- wp:list -->\n{content}\n<!-- /wp:list -->'}).get('pattern', '{content}')
            list_content = '\n'.join([f'<li>{item}</li>' for item in list_lines])
            result.append(pattern.replace('{content}', list_content))
            list_lines = []
            # 通常行の処理に続く
            # 引用や見出し等の処理
            if line.startswith('# '):
                if not title_set:
                    result.insert(0, f'<!-- wp:title -->\n{line[2:]}\n<!-- /wp:title -->')
                    title_set = True
                else:
                    pattern = block_defs.get('heading', {}).get('pattern', '{content}')
                    result.append(pattern.replace('{content}', line[2:]))
            elif line.startswith('## '):
                pattern = block_defs.get('heading2', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[3:]))
            elif line.startswith('### '):
                pattern = block_defs.get('heading3', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[4:]))
            elif line.startswith('#### '):
                pattern = block_defs.get('heading4', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[5:]))
            elif line.startswith('##### '):
                pattern = block_defs.get('heading5', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[6:]))
            elif line.startswith('|'):
                pattern = block_defs.get('table', {}).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line))
            else:
                pattern = block_defs.get('paragraph', {}).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line))
        # 数字ヘッダの箇条書き対応
        elif line.lstrip().startswith(tuple(f'{i}. ' for i in range(1, 10))):
            if not in_olist_block:
                in_olist_block = True
                olist_lines = [line.lstrip().split('. ', 1)[1]]
            else:
                olist_lines.append(line.lstrip().split('. ', 1)[1])
        elif in_olist_block and not any(line.lstrip().startswith(f'{i}. ') for i in range(1, 10)):
            in_olist_block = False
            pattern = block_defs.get('olist', {'pattern': '<!-- wp:list {\"ordered\":true} -->\n{content}\n<!-- /wp:list -->'}).get('pattern', '{content}')
            olist_content = '\n'.join([f'<li>{item}</li>' for item in olist_lines])
            result.append(pattern.replace('{content}', olist_content))
            olist_lines = []
        # 引用対応
        elif line.startswith('> '):
            if not in_quote_block:
                in_quote_block = True
                quote_lines = [line[2:]]
            else:
                quote_lines.append(line[2:])
        elif in_quote_block and not line.startswith('> '):
            in_quote_block = False
            pattern = block_defs.get('quote', {}).get('pattern', '{content}')
            quote_content = '\n'.join(quote_lines)
            result.append(pattern.replace('{content}', quote_content))
            quote_lines = []
            # 通常行の処理に続く
            if line.startswith('# '):
                if not title_set:
                    result.insert(0, f'<!-- wp:title -->\n{line[2:]}\n<!-- /wp:title -->')
                    title_set = True
                else:
                    pattern = block_defs.get('heading', {}).get('pattern', '{content}')
                    result.append(pattern.replace('{content}', line[2:]))
            elif line.startswith('## '):
                pattern = block_defs.get('heading2', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[3:]))
            elif line.startswith('### '):
                pattern = block_defs.get('heading3', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[4:]))
            elif line.startswith('#### '):
                pattern = block_defs.get('heading4', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[5:]))
            elif line.startswith('##### '):
                pattern = block_defs.get('heading5', block_defs.get('heading', {})).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[6:]))
            elif line.startswith('|'):
                pattern = block_defs.get('table', {}).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line))
            else:
                pattern = block_defs.get('paragraph', {}).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line))
        elif line.startswith('# '):
            if not title_set:
                result.insert(0, f'<!-- wp:title -->\n{line[2:]}\n<!-- /wp:title -->')
                title_set = True
            else:
                pattern = block_defs.get('heading', {}).get('pattern', '{content}')
                result.append(pattern.replace('{content}', line[2:]))
        elif line.startswith('## '):
            pattern = block_defs.get('heading2', block_defs.get('heading', {})).get('pattern', '{content}')
            result.append(pattern.replace('{content}', line[3:]))
        elif line.startswith('### '):
            pattern = block_defs.get('heading3', block_defs.get('heading', {})).get('pattern', '{content}')
            result.append(pattern.replace('{content}', line[4:]))
        elif line.startswith('#### '):
            pattern = block_defs.get('heading4', block_defs.get('heading', {})).get('pattern', '{content}')
            result.append(pattern.replace('{content}', line[5:]))
        elif line.startswith('##### '):
            pattern = block_defs.get('heading5', block_defs.get('heading', {})).get('pattern', '{content}')
            result.append(pattern.replace('{content}', line[6:]))
        elif line.startswith('|'):
            pattern = block_defs.get('table', {}).get('pattern', '{content}')
            result.append(pattern.replace('{content}', line))
        else:
            pattern = block_defs.get('paragraph', {}).get('pattern', '{content}')
            result.append(pattern.replace('{content}', line))
    # 残りのブロックを出力
    if in_list_block and list_lines:
        pattern = block_defs.get('ulist', {'pattern': '<!-- wp:list -->\n{content}\n<!-- /wp:list -->'}).get('pattern', '{content}')
        list_content = '\n'.join([f'<li>{item}</li>' for item in list_lines])
        result.append(pattern.replace('{content}', list_content))
    if in_olist_block and olist_lines:
        pattern = block_defs.get('olist', {'pattern': '<!-- wp:list {\"ordered\":true} -->\n{content}\n<!-- /wp:list -->'}).get('pattern', '{content}')
        olist_content = '\n'.join([f'<li>{item}</li>' for item in olist_lines])
        result.append(pattern.replace('{content}', olist_content))
    if in_quote_block and quote_lines:
        pattern = block_defs.get('quote', {}).get('pattern', '{content}')
        quote_content = '\n'.join(quote_lines)
        result.append(pattern.replace('{content}', quote_content))
    return '\n'.join(result)
