import os

def save_converted_file(original_path, gb_text):
    dir_name = os.path.dirname(original_path)
    base = os.path.basename(original_path)
    name, ext = os.path.splitext(base)
    gb_name = f"{name}_gb{ext}"
    gb_path = os.path.join(dir_name, gb_name)
    with open(gb_path, 'w', encoding='utf-8') as f:
        f.write(gb_text)
