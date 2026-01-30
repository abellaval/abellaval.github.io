import os
from pathlib import Path
import hashlib
import shutil


# Loading bibliography
def load_categories(bib_dir, output_file, sections) :
    """
    Load bib for a specific category : math, philo, econ...
    """

    show_sha2_digest = False

    # Gets bib size and hash
    def get_directory_size(bib_dir) :
        return sum(f.stat().st_size for f in Path(bib_dir).rglob('*.pdf') if f.is_file())
    bib_size = get_directory_size(bib_dir)
    bib_size = int(bib_size/(1024**2))


    # Compute SHA2 digest of the bib
    def hash_bib(path) :
        sha = hashlib.sha256()

        for pdf in sorted(Path(path).glob("*.pdf")) :
            with pdf.open("rb") as f:
                for chunk in iter(lambda: f.read(8192), b"") :
                    sha.update(chunk)
        return sha.hexdigest()
    bib_digest = hash_bib(bib_dir)


    # Actually get the bib
    def import_pdf(section_name, split=True) :
        # Import files
        dir = bib_dir + section_name
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
            #print(pdf_files)

        # Convert to html
        list_items = []
        for filename in pdf_files:
            name = os.path.splitext(filename)[0]

            list_items.append(f'\t\t<li><a class="bib" href="{dir}/{filename}" target="_blank">{name}</a></li>')

        # Generate the html section
        html_section = f"""
        \n<!-- {section_name} -->
        <h2 class='bib'>— {section_name} —</h2>
        <ol>
    {chr(10).join(list_items)}
        </ol>\n"""

        return html_section


    # HTML head
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

    # HTML coda
    if show_sha2_digest :
        html_coda = f"""<p style="margin-top: 3%;">
            size     : ~{bib_size} MB <br>
            SHA256 : {bib_digest} <br>
            <a class="bib" href="math.zip" download>download</a>
        </p>
    </body>
        </html>"""
    else :
        html_coda = f"""\n\n<!-- Download -->
    <p style="margin-top: 3%;">
		size     : ~{bib_size} MB <br>
        <a class="bib" href="math.zip" download>download</a>
	</p>
</body>
    </html>"""


    # Head of the html page
    html_page = html_head

    # Add the sections
    for section in sections :
        html_page += import_pdf(section)

    # Add the byte-size and hash

    # End of the html code
    html_page += html_coda


    # Write to bib.html
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_page)

    print(f"---> {output_file[2:]} has been successfully generated.")




def create_bib_archive(bib_dir) :
    archive_name = bib_dir.replace('./bib/','').replace('/','')

    shutil.make_archive(
        base_name=bib_dir + archive_name,
        format="zip",
        root_dir='.',
        base_dir=bib_dir
    )
    return 0


# One bib page per topic
categories = [
    ['./bib/math/','./bib.html', ['KLPT & IKO','SQIsign', 'Isogenies', 'Mathematics','Drinfeld Modules','Cryptography','Lattices','Books','Theses','Misc']],
    ['./bib/philo/', './bib2.html', ['Philosophy of mind','Metaphysics']]
]

for category in categories :
    bib_dir, output_file, sections = category
    load_categories(bib_dir, output_file, sections)
 
    # create_bib_archive(bib_dir)



