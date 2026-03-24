import os
import re

css_path = 'static/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# CSS Splitting
css_blocks = {
    'base.css': r'/\* --- Variables Generales --- \*/.*?/\* --- Navbar --- \*/',
    'navbar.css': r'/\* --- Navbar --- \*/.*?/\* --- Hero Section Premium --- \*/',
    'hero.css': r'/\* --- Hero Section Premium --- \*/.*?/\* --- About --- \*/',
    'sections.css': r'/\* --- About --- \*/.*?/\* --- Musica --- \*/',
    'music.css': r'/\* --- Musica --- \*/.*?/\* --- Lightbox / Modal --- \*/',
    'lightbox.css': r'/\* --- Lightbox / Modal --- \*/.*?/\* --- Footer --- \*/',
    'footer.css': r'/\* --- Footer --- \*/.*?/\* --- Responsive --- \*/',
    'responsive.css': r'/\* --- Responsive --- \*/.*?/\* --- View Modules \(Tabs\) --- \*/',
    'store.css': r'/\* --- View Modules \(Tabs\) --- \*/.*'
}

for filename, pattern in css_blocks.items():
    match = re.search(pattern, css_content, re.DOTALL)
    if match:
        content = match.group(0)
        # remove the overlapping end pattern except for the last one
        if filename != 'store.css':
            content = content[:content.rfind('/* ---')]
        with open(f'static/css/{filename}', 'w', encoding='utf-8') as out:
            out.write(content.strip() + '\n')

# Create style.css imports
imports = "\n".join([f"@import url('{f}');" for f in css_blocks.keys()])
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(imports + '\n')

html_path = 'templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# HTML Splitting
os.makedirs('templates/components', exist_ok=True)

patterns = {
    'navbar.html': r'<!-- Navegación Sticky -->.*?<!-- Main Content Wrapper -->',
    'hero.html': r'<!-- Hero Section -->.*?<!-- Biografía -->',
    'about.html': r'<!-- Biografía -->.*?<!-- Miembros -->',
    'members.html': r'<!-- Miembros -->.*?<!-- Tour -->',
    'tour.html': r'<!-- Tour -->.*?<!-- Música y Media -->',
    'music.html': r'<!-- Música y Media -->.*?</section>', # matches up to end of music section, right before </div> <!-- Fin Main Content -->
    'store.html': r'<!-- Store Content Wrapper -->.*?<!-- Fin Store Content -->',
    'footer.html': r'<!-- Contacto y Footer -->.*?</footer>',
    'scripts.html': r'<!-- Lightbox -->.*?</body>'
}

html_replacements = {}
for name, p in patterns.items():
    m = re.search(p, html_content, re.DOTALL)
    if m:
        c = m.group(0)
        
        # fix the overlapping for music
        if name == 'music.html':
            m2 = re.search(r'<!-- Música y Media -->.*?</section>', html_content, re.DOTALL)
            c = m2.group(0)
            
        with open(f'templates/components/{name}', 'w', encoding='utf-8') as out:
            out.write(c.strip() + '\n')
        html_replacements[name] = c

# Construct base.html
# It should have everything before Navbar, then a block, then closing.
head_part = re.search(r'<!DOCTYPE html>.*?<body>', html_content, re.DOTALL).group(0)

base_html = f"""{head_part}
    {{% include 'components/navbar.html' %}}
    
    {{% block content %}}{{% endblock %}}

    {{% include 'components/footer.html' %}}
    {{% include 'components/scripts.html' %}}
</html>
"""

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

# Construct index.html
index_html = """{% extends "base.html" %}
{% block content %}
    <!-- Main Content Wrapper -->
    <div id="main-content" class="view-module active">
        {% include 'components/hero.html' %}
        {% include 'components/about.html' %}
        {% include 'components/members.html' %}
        {% include 'components/tour.html' %}
        {% include 'components/music.html' %}
    </div> <!-- Fin Main Content -->

    {% include 'components/store.html' %}
{% endblock %}
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Split complete.")
