# 'category_main': category_main,
# 'category_sub': category_sub,
# 'file_name': file_name,
# '_post_convention_name': _post_convention_name,
# 'tag_text': tag_text,
# 'temp_path': temp_path + _post_convention_name,
# 'full_path': root_path + '/' + file_name,
# 'ext': file_name.split('.')[-1]
import os
import base64


def convert_ipynb(data):
    notebook = data['notebook']
    file = data['file']

    category_main = file['category_main']
    category_sub = file['category_sub']
    file_name = file['file_name']
    tag_text = file['tag_text']
    ext = file['ext']
    series_html = file['series_html']
    _post_convention_name = file['_post_convention_name']

    file_title = file_name.replace('.' + ext, '')

    markdown_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "layout: single\n",
            f'title: "[{category_sub}]{file_title}"\n',
            f"categories: {category_main}\n",
            f"tag: {tag_text}\n",
            "toc: true\n",
            "author_profile: false\n",
            "typora-root-url: ../\n",
            "sidebar:\n",
            '  nav: "counts"\n',
            '---\n',
        ]
    }

    notebook['cells'].insert(0, markdown_cell)

    md_text = ''
    for i in range(len(notebook['cells'])):
        cell = notebook['cells'][i]
        cell_type = cell['cell_type']

        if i == 1:
            md_text += series_html

        if cell_type == 'markdown':
            for j in range(len(notebook['cells'][i]['source'])):
                md_text += notebook['cells'][i]['source'][j]

            md_text += '\n \n'

        if cell_type == 'code':

            md_text += '\n``` python\n'
            sources = cell['source']

            for j in range(len(sources)):
                md_text += sources[j]

            md_text += '\n```\n'

            output_len = len(cell['outputs'])

            if output_len > 0:
                for j in range(output_len):
                    output = cell['outputs'][j]
                    output_type = output['output_type']

                    if output_type == 'stream':
                        texts = output['text']
                        md_text += '\n<div class="op_wrap">'
                        for text in texts:
                            if text.find('Users/shindongwon') == -1:
                                md_text += '<op>' + text + '</op><br>'
                        md_text += '</div>\n'

                    elif output_type == 'execute_result':
                        data = output['data']
                        if 'text/plain' in data.keys():
                            texts = data['text/plain']
                            md_text += '\n<div class="op_wrap">'
                            for text in texts:
                                if text.find('Users/shindongwon') == -1:
                                    md_text += '<op>' + text + '</op>'
                            md_text += '</div>\n\n'

                    elif output_type == 'display_data':
                        data = output['data']
                        img = data['image/png']

                        img_path = f'/images/{_post_convention_name}/{i}_{j}.png'

                        if not os.path.isdir(f'./images/{_post_convention_name}/'):
                            os.makedirs(f'./images/{_post_convention_name}/')

                        # img path가 여기는 절대경로
                        md_text += f'![]({img_path})\n'

                        # img path가 여기는 상대경로
                        with open(f'.{img_path}', 'wb') as f:
                            f.write(base64.b64decode(img))

    return md_text
