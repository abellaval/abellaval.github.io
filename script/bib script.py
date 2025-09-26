import os


bib_dir = './bib/'
output_file = './bib.html'
sections = ['KLPT & IKO', 'SQIsign', 'Isogenies','Mathematics', 'Drinfeld Modules','Cryptography', 'Books', 'Theses', '"Science"']


def import_pdf(section_name, split=True) :

    # Import files
    dir = bib_dir + section_name
    print(f"dir = {dir}")
    pdf_files = [f for f in os.listdir(dir) if f.lower().endswith('.pdf')]

    # Titleless articles are put above the others
    if split :
        without_title = []
        with_title = []

        for filename in pdf_files:
            if filename[-5] == ']' : without_title.append(filename)
            else : with_title.append(filename)
            
        without_title.sort()
        with_title.sort()
        pdf_files = without_title + with_title
        print(pdf_files)

    # Convert to html
    list_items = []
    for filename in pdf_files:
        name = os.path.splitext(filename)[0]


        list_items.append(f'\t\t<li><a class="bib" href="{dir}/{filename}" target="_blank">{name}</a></li>')

    #list_items.sort()


    

    # Generate the html section
    html_section = f"""
    \n<!-- {section_name} -->
    <h2 class='bib'>— {section_name} —</h2>
    <ol>
{chr(10).join(list_items)}
    </ol>\n"""

    return html_section



html_head = f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Abel Laval</title>
        <link rel="icon" type="image/png" href="favicon.svg">
        <link rel="stylesheet" href="css/style.css">
        <meta charset="UTF-8">
    </head>

<body>
    <p class="bib">
        <a style="margin-right: 10px;"  href="index.html">home</a>
    </p>"""

html_coda = f"""</body>
</html>"""


# Head of the html page
html_page = html_head

# Add the sections
for section in sections :
    html_page += import_pdf(section)

# End of the html code
html_page += html_coda


# Write to bib.html
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_page)

print(f"{output_file[2:]} has been generated successfully.")