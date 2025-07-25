import os


pdf_dir = './../bib'
output_file = './../bib.html'


pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]



list_items = []
for filename in pdf_files:
    name = os.path.splitext(filename)[0]
    list_items.append(f'\t<li><a class="bib" href="{pdf_dir}/{filename}" target="_blank">{name}</a></li>')


html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
\t<title>Abel Laval</title>
\t<link rel="icon" type="image/png" href="img/favicon.png">
\t<link rel="stylesheet" href="css/style.css">
\t<meta charset="UTF-8">
</head>\n

<body>
    <p class="bib">
        <a style="margin-right: 10px;"  href="index.html">home</a>
    </p>
    <h2>Articles</h2>
    <ol>
    {chr(10).join(list_items)}
    </ol>
</body>
</html>
"""

# Write to bib.html
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_page)

print(f"{output_file} has been generated successfully.")