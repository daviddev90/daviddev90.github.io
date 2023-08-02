
def add(file):
    category_main = file['category_main']
    category_sub = file['category_sub']
    file_name = file['file_name']
    tag_text = file['tag_text']
    ext = file['ext']
    file_title = file_name.replace('.' + ext, '')
    series_html = file['series_html']

    layout_text = "---\n" \
        "layout: single\n" \
        f'title: "[{category_sub}]{file_title}"\n' \
        f'categories: {category_main}\n' \
        f'tag: {tag_text}\n' \
        'toc: true\n' \
        'author_profile: false\n' \
        'typora-root-url: ../\n' \
        'sidebar:\n' \
        '  nav: "counts"\n' \
        '---\n' \
        '\n'
    layout_text += series_html
    return layout_text
