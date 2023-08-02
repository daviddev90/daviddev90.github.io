import re
import importlib
import utils.common
import utils.cvt_ipynb
import utils.add_layout_to_md
import io
import json

importlib.reload(utils.common)
importlib.reload(utils.cvt_ipynb)
importlib.reload(utils.add_layout_to_md)

get_files_data = utils.common.get_files_data
convert_ipynb = utils.cvt_ipynb.convert_ipynb
add_layout = utils.add_layout_to_md.add

input_path = './study/'
output_path = './_posts/'

# [작성중] 표시가 없는 ipynb, md파일만 가져옴
files_info = get_files_data()
for file in files_info:

    if file['ext'] == 'ipynb':
        with io.open(file['full_path'], 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        md_text = convert_ipynb({
            'notebook': notebook,
            'file': file
        })

    if file['ext'] == 'md':
        md_text = add_layout(file)
        with io.open(file['full_path'], 'r', encoding='utf-8') as f:
            md_text += f.read()
        md_text = re.sub(r'(\.\./)+images/typora', '/images/typora', md_text)

    # 파일명 규칙에 맞게 변경
    file_name = file['_post_convention_name']
    ext = file['ext']
    file_name = file_name.replace(ext, 'md')
    # 파일 생성
    with io.open(output_path + file_name, 'w', encoding='utf-8') as f:
        f.write(md_text)
