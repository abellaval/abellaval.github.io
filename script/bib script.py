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

        # Replace keywords in filenames by characters that are not allowed in filenames
        character_replacements = {'[slash]':'/', '[interrogation]':'?',
                                  '[phi]':'φ'}
        

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
            # Replacing special characters
            for key in character_replacements :
                name = name.replace(key, character_replacements[key])

            # Detect where exponents are in titles and replace them
            def replace_sub_supscripts(name) :
                types = [{'tag' : '^',
                          'items' : {'0':'⁰', '1':'¹', '2':'²', '3':'³', '4':'⁴', '5':'⁵', '6':'⁶', '7':'⁷', '8':'⁸', '9':'⁹',
                                     '/':'ᐟ', '(':'⁽', ')':'⁾', '+':'⁺',
                                     'o':'ᵒ'}},
                          {'tag' : '_',
                          'items' : {'0':'₀', '1':'₁', '2':'₂', '3':'₃', '4':'₄', '5':'₅', '6':'₆', '7':'₇', '8':'₈', '9':'₉', 'p':'ₚ'}}
                          ]

                def replace_symbols(s, type) :
                    items = type['items']
                    for key in items :
                        s = s.replace(key, items[key])
                    return s

                def detect(name, type) :
                    tag = type['tag']

                    list_strings = []
                    for i in range(len(name)) :
                        if name[i:i+2] == tag+'{' :
                            list_strings.append(['',i,i+2])
                            for k in range(i+2, len(name)) :
                                list_strings[-1][2] += 1    # Count number of letters in the string
                                if name[k] == '}' : break
                                list_strings[-1][0] += name[k]
                    return list_strings

                for type in types :
                    list_strings = detect(name, type)
                    if list_strings == [] : continue    # If there is nothing to replace (most papers)
                    for s in list_strings :
                        # We cut the title where the exponent/subscript is and insert the replaced exponent where the encoding was
                        # s[0] : what has to be replaced (str)
                        # s[1] : index of the exponent in name (int)
                        # s[2] : index where the exponent stops (int)
                        name = name[:s[1]] + replace_symbols(s[0],type) + name[s[2]:]

                return name


            # Add exponents and subscripts
            name = replace_sub_supscripts(name)

            list_items.append(f'\t\t<li><a class="bib" href="{dir}/{filename}" target="_blank">{name}</a></li>')

        # Generate the html section if there are articles in it
        if pdf_files != [] :
            html_section = f"""
            \n<!-- {section_name} -->
            <h2 class='bib'>— {section_name} —</h2>
            <ol>
        {chr(10).join(list_items)}
            </ol>\n"""
        else :
            html_section = ""

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
        <a class="bib" href="math.zip" download>download</a> (coming soon)
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
    ['./bib/math/','./bib.html', ['KLPT & IKO','SQIsign', 'Isogenies', 'Mathematics', 'Ibukiyama', 'Drinfeld Modules','Cryptography','Lattices','Books', 'Syllabus', 'Theses','Misc','Poetry']],
    ['./bib/philo/', './bibb.html', ['Metaphysics', 'Ethics', 'Philosophy of mind']],
    ['./bib/eco/', './bibbb.html', ['Macroeconomy', 'Finance', 'Pseudoscience', 'Books', 'Reports', 'Theses']]
]

for category in categories :
    bib_dir, output_file, sections = category
    load_categories(bib_dir, output_file, sections)
 
    # create_bib_archive(bib_dir)



