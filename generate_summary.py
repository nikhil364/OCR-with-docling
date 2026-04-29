import json
from pathlib import Path

OUTPUT_DIR = Path("ocr_output")
SUMMARY_DIR = Path("ocr_output_summaries")
SUMMARY_DIR.mkdir(exist_ok=True)

def generate_summary_for_pdf(pdf_folder: Path):
    full_text_file = pdf_folder / "full_text.json"
    if not full_text_file.exists():
        return

    with open(full_text_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    pdf_name = pdf_folder.name
    summary_file = SUMMARY_DIR / f"{pdf_name}.html"

    html_content = f"<html><head><title>{pdf_name} Summary</title></head><body>"
    html_content += f"<h1>{pdf_name}</h1>"
    html_content += f"<p>Metadata: {data.get('metadata', {})}</p>"

    # Add each page image and text
    page_num = 1
    while True:
        page_image = pdf_folder / f"page_{page_num}.png"
        page_json = pdf_folder / f"page_{page_num}.json"
        if not page_image.exists() and not page_json.exists():
            break

        html_content += f"<h2>Page {page_num}</h2>"
        if page_image.exists():
            html_content += f'<img src="{page_image}" style="max-width:600px;"><br>'
        if page_json.exists():
            with open(page_json, "r", encoding="utf-8") as pf:
                page_data = json.load(pf)
                html_content += f"<pre>{page_data.get('text','')}</pre>"

        page_num += 1

    html_content += f'<p>Full text JSON: {full_text_file}</p>'
    html_content += "</body></html>"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated summary: {summary_file}")

def generate_all_summaries():
    for pdf_folder in OUTPUT_DIR.rglob("*"):
        if pdf_folder.is_dir() and (pdf_folder / "full_text.json").exists():
            generate_summary_for_pdf(pdf_folder)

if __name__ == "__main__":
    generate_all_summaries()