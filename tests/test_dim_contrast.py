import re
import sys
from pathlib import Path


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def linearize(c):
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(c1, c2):
    l1 = relative_luminance(c1)
    l2 = relative_luminance(c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def test_dim_contrast():
    html_path = Path('films/ai-oversold/index.html')
    text = html_path.read_text(encoding='utf-8')

    dim_match = re.search(r"DIM\s*=\s*'(#[0-9a-fA-F]{6})'", text)
    if not dim_match:
        print('找不到 DIM = \'#xxxxxx\'')
        sys.exit(1)
    dim = dim_match.group(1)

    ratio = contrast_ratio(dim, '#f5efe6')
    if ratio < 4.5:
        print(f'contrast {ratio:.2f} < 4.5 (DIM {dim} vs #f5efe6)')
        sys.exit(1)

    source_match = re.search(
        r"plain\(\s*[`'\"]來源｜[^,]*,\s*[^,]+,\s*[^,]+,\s*(\d+)",
        text,
    )
    if not source_match:
        print('找不到以 來源｜ 開頭的 plain( 呼叫')
        sys.exit(1)
    font_size = int(source_match.group(1))
    if font_size < 32:
        print(f'來源｜ plain 字級 {font_size} < 32')
        sys.exit(1)


if __name__ == '__main__':
    test_dim_contrast()
