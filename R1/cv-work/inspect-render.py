from pathlib import Path
import fitz

root = Path(r'D:\Final-Lesson-Implementation\R1\cv-work')
out = root / 'prep-pages'
out.mkdir(exist_ok=True)
pdf = fitz.open(root / 'prep-qa.pdf')
print(f'Page count: {len(pdf)}')
for n, page in enumerate(pdf, 1):
    page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(out / f'page-{n:02d}.png')
    blocks = page.get_text('blocks')
    content = [b for b in blocks if b[1] < page.rect.height - 40]
    print(n, 'words', len(page.get_text().split()), 'last body y', round(max(b[3] for b in content), 1), 'heading', page.get_text().splitlines()[0])
