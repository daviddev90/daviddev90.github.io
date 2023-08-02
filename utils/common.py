import os
from datetime import datetime
input_path = './study/'


def _generate_create_date_text(root_path, file_name):
    _date = datetime.fromtimestamp(
        os.path.getctime(root_path + '/' + file_name))
    _text = _date.strftime('%Y-%m-%d-')
    return _text


def _generate_convention_name(root_path, file_name, category_sub):
    _created_date_text = _generate_create_date_text(root_path, file_name)
    _name = category_sub + '~' + file_name
    _name = _name.replace(' ', '_')
    _name = _created_date_text + _name
    return _name


def _generate_href_text(category_main, category_sub, file_name, ext):
    _href = category_main + '/' + category_sub + '~' + file_name
    _href = _href.replace(' ', '_')
    _href = _href.replace('.' + ext, '')

    return _href


def _generate_tag_text(category_main, category_sub, file_name):
    # 중복 무시됨
    tag_set = set()
    tag_set.add(category_main)

    langs = ['javascript', 'typescript', 'react', 'svelte', 'python',
             'html', 'css', 'math', 'web', 'data science', 'algorithm']

    concat_name = category_main + '_' + category_sub + '_' + file_name
    concat_name = concat_name.lower()

    if file_name.endswith('.ipynb'):
        tag_set.add('python')

    if category_main == 'ml':
        tag_set.add('data science')
        tag_set.add('python')

    if category_main == 'dsa':
        tag_set.add('algorithm')
        tag_set.add('data structure')

    if category_main == 'leetcode':
        tag_set.add('algorithm')
        tag_set.add('data structure')

    for lang in langs:
        if lang in concat_name:
            tag_set.add(lang)

    tag_text = "[" + ", ".join(str(elem) for elem in tag_set) + "]"
    return tag_text


def _generate_post_series_htmls(files_info):
    series_dict = {}
    for f in files_info:
        series = f['category_sub']
        if series not in series_dict:
            series_dict[series] = []
        series_dict[series].append({
            'category_main': f['category_main'],
            'category_sub': f['category_sub'],
            '_post_convention_name': f['_post_convention_name'],
            'post_title': f['post_title'],
            'href': f['href']
        })

        for series_name, series_list in series_dict.items():
            series_list.sort(key=lambda x: x['post_title'])

    for f in files_info:
        series_name = f['category_sub']
        series_list = series_dict[series_name]
        series_html = f'<nav class="cods"><h2>{series_name} posts</h2><ol>'
        current_title = f['post_title']

        for s in series_list:
            s_title = s['post_title']
            href = s['href']

            if current_title == s_title:
                series_html += f'<li><p>(current) {current_title}</p></li>'
            else:
                series_html += f'<li><a href="{href}">{s_title}</a></li>'

        series_html += '</ol></nav>\n\n'

        f['series_html'] = series_html

    return files_info


def get_files_data():
    files_info = []
    for root_path, _, files in os.walk(input_path):
        folder_path = root_path.replace(input_path, '')
        # os.path.sep을 사용: 윈도우와 리눅스(맥)의 경로 구분자가 다르기 때문에
        folder_path_list = folder_path.split(os.path.sep)

        category_main = folder_path_list[0]
        category_sub = folder_path_list[-1]

        for file_name in files:
            if not (file_name.endswith('.ipynb') or file_name.endswith('.md')):
                continue

            if '[작성중]' in file_name:
                continue

            ext = file_name.split('.')[-1]
            href_text = _generate_href_text(
                category_main, category_sub, file_name, ext)

            # github blog 파일명 규칙에 맞게 변경
            _post_convention_name = _generate_convention_name(
                root_path, file_name, category_sub)
            # 태그 텍스트 생성
            tag_text = _generate_tag_text(
                category_main, category_sub, file_name)

            files_info.append({
                'category_main': category_main,
                'category_sub': category_sub,
                'file_name': file_name,
                '_post_convention_name': _post_convention_name,
                'tag_text': tag_text,
                'href': href_text,
                # 윈도우와 리눅스(맥)의 경로 구분자가 다르기 때문에 아래가 필요
                'full_path': os.path.join(root_path, file_name),
                'ext': ext,
                'post_title': file_name.replace('.' + ext, '')
            })

    files_info = _generate_post_series_htmls(files_info)

    return files_info
