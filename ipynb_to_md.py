import os
import shutil
from datetime import datetime
import io
import json
import base64

input_path = './study/'
output_path = './_posts/'
temp_path = './temp/'

# output_path가 존재하지 않을 경우 생성
if not os.path.isdir(output_path):
    os.makedirs(output_path)

if not os.path.isdir(temp_path):
    os.makedirs(temp_path)

if not os.path.isdir('./images/'):
    os.makedirs('./images/')

processed_idx = 0
already_exist_idx = 0
error_occured_idx = 0

# 이미 _posts 폴더에 파일이 존재하면 작업을 건너뛰기 위함
file_paths = []
for root, dirs, files in os.walk(output_path):
    for file in files:
        # file의 앞 11글짜 제거
        postname = file[11:]
        postname = postname.split('.')[0]
        file_paths.append(postname)


cods = {}

for root, dirs, files in os.walk(input_path):
    for file in files:

        if not (file.endswith('.ipynb') or file.endswith('.md')):
            continue
        
        file_path = os.path.join(root, file)

        splited = file_path.split('/')

        name_category = splited[2] # ml, python, etc
        ns = splited[-2].replace(' ', '_') # collection name C02_머신러닝_프로젝트
        name_doc = splited[-1].split('.')[0].replace(' ', '_') # doc name 01_목표설계


        if ns not in cods:
            cods[ns] = {
                'docs': [],
                'name_category': name_category,
            }
        
        cods[ns]['docs'].append({
            'name_doc': name_doc,
            'file_path': file_path,
        })


for name_series in cods:
  series = cods[name_series]
  name_category = series['name_category']

  for doc in series['docs']:
    name_doc = doc['name_doc']
    file_path = doc['file_path']

    post_name = name_series + '~' + name_doc # C02_머신러닝_프로젝트~01_목표설계

    # github blog식 파일 이름으로 변경
    creation_date = datetime.fromtimestamp(os.path.getctime(file_path))
    new_file_name = creation_date.strftime('%Y-%m-%d-') + post_name

    if post_name[-3:] == '작성중':
        continue
    
    if '~' not in post_name:
        continue

    # 이미 post가 존재할 경우 넘어감!
    if post_name in file_paths:
        continue
    
    tag_text = ''

    if name_category == 'python':
        tag_text = '[python]'
    else:
        tag_text = f'[python, {name_category}]'


    if file_path.endswith('.ipynb'):
        new_file_name += '.ipynb'
        
        if not os.path.isdir('./temp/' + name_category):
          os.makedirs('./temp/' + name_category)

        new_file_path = os.path.join(temp_path, name_category, new_file_name)
        shutil.copy2(file_path, new_file_path)

        try:
          with io.open(new_file_path, 'r', encoding='utf-8') as f:
              notebook = json.load(f)

          name_series_title = name_series.replace('_', ' ')
          name_doc_title = name_doc.replace('_', ' ')

          markdown_cell = {
              "cell_type": "markdown",
              "metadata": {},
              "source": [
                  "---\n",
                  "layout: single\n",
                  f'title: "[{name_series_title}]{name_doc_title}"\n',
                  f"categories: {name_category}\n",
                  f"tag: {tag_text}\n",
                  "toc: true\n",
                  "author_profile: false\n",
                  "typora-root-url: ../\n",
                  "sidebar:\n",
                  '  nav: "counts"\n',
                  '---\n',
              ]
          }

          # 새로운 셀을 최상단에 추가
          notebook['cells'].insert(0, markdown_cell)

          # 파일 열기 및 데이터 쓰기
          with io.open(new_file_path, 'w', encoding='utf-8') as f:
              json.dump(notebook, f)

        except:
            # remove file
            print('remove file: ', new_file_path)
            os.remove(new_file_path)


    if file_path.endswith('.md'):  # md 파일만 처리
        copying_path = os.path.join(output_path, creation_date.strftime('%Y-%m-%d-') +name_series + '~' + name_doc + '.md')

        shutil.copy2(file_path, copying_path)

        try:
            # 파일 열기 및 데이터 읽기
            with io.open(copying_path, 'r', encoding='utf-8') as f:
                contents = f.read()

            n_contents = ''

            h2_name = name_series.replace('_', ' ')
            
            n_contents += f'<nav class="cods"><h2>{h2_name} 시리즈 목차</h2><ol>'
            doclist = cods[name_series]['docs']

            # copy doclist
            sorted = doclist.copy()

            # sort doclist by name_doc
            sorted.sort(key=lambda x: x['name_doc'])

            for doc_path in sorted:
              name_doc_in_doclist = doc_path['name_doc']

              doc_name = name_doc_in_doclist.replace('_', ' ')

              if name_doc_in_doclist != name_doc:
                if name_doc_in_doclist[-3:] != '작성중':
                  n_contents += f'<li><a href="/{name_category}/{name_series}~{name_doc_in_doclist}/">{doc_name}</a></li>'
              else:
                n_contents += f'<li><p>(현재 글) {name_doc}</p></li>'

            n_contents += '</ol></nav>\n\n'

            name_series_title = name_series.replace('_', ' ')
            name_doc_title = name_doc.replace('_', ' ')
        
            # 새로운 데이터 생성 (상단에 내용 추가)
            new_data = "---\n" \
                    "layout: single\n" \
                    f'title: "[{name_series_title}]{name_doc_title}"\n' \
                    f'categories: {name_category}\n' \
                    f'tag: {tag_text}\n' \
                    'toc: true\n' \
                    'author_profile: false\n' \
                    'typora-root-url: ../\n' \
                    'sidebar:\n' \
                    '  nav: "counts"\n' \
                    '---\n' \
                    '\n' + n_contents + contents

            # 파일 열기 및 데이터 쓰기
            with io.open(copying_path, 'w', encoding='utf-8') as f:
                f.write(new_data)
            
            processed_idx += 1

        except:
            # remove file
            error_occured_idx += 1
            print('problematic file: ', copying_path)


for name_series in cods:
  series = cods[name_series]
  name_category = series['name_category']
  
  for doc in series['docs']:
    name_doc = doc['name_doc']
    file_path = doc['file_path']
    # github blog식 파일 이름으로 변경
    creation_date = datetime.fromtimestamp(os.path.getctime(file_path))

    ipynb_path = './temp/' + name_category + '/'  + creation_date.strftime('%Y-%m-%d-')+ name_series + '~' + name_doc + '.ipynb'

    post_path = './_posts/' + creation_date.strftime('%Y-%m-%d-')+ name_series + '~' + name_doc + '.md'

    if file_path.endswith('.ipynb'):

      post_name = name_series + '~' + name_doc # C02_머신러닝_프로젝트~01_목표설계


      if post_name[-3:] == '작성중':
          continue
      
      if '~' not in post_name:
          continue

      # 이미 post가 존재할 경우 넘어감!
      if post_name in file_paths:
          already_exist_idx += 1
          continue

      md_data = ''

      with io.open(ipynb_path, 'r', encoding='utf-8') as f:
          notebook = json.load(f)

          for i in range(len(notebook['cells'])):
            cell = notebook['cells'][i]
            cell_type = cell['cell_type']

            if i == 1:
              h2_name = name_series.replace('_', ' ')
              
              md_data += f'<nav class="cods"><h2>{h2_name} 시리즈 목차</h2><ol>'
              doclist = cods[name_series]['docs']

              # copy doclist
              sorted = doclist.copy()

              sorted.sort(key=lambda x: x['name_doc'])
              
              for doc_path in sorted:
                name_doc_in_doclist = doc_path['name_doc']

                doc_name = name_doc_in_doclist.replace('_', ' ')

                if name_doc_in_doclist != name_doc:
                  if name_doc_in_doclist[-3:] != '작성중':
                    md_data += f'<li><a href="/{name_category}/{name_series}~{name_doc_in_doclist}/">{doc_name}</a></li>'
                else:
                  md_data += f'<li><p>(현재 글) {name_doc}</p></li>'

              md_data += '</ol></nav>\n\n'


            if cell_type == 'markdown':
              for j in range(len(notebook['cells'][i]['source'])):
                md_data += notebook['cells'][i]['source'][j]
              
              md_data += '\n \n'


            if cell_type == 'code':

              md_data += '\n``` python\n'
              sources = cell['source']

              for j in range(len(sources)):
                md_data += sources[j]

              md_data += '\n```\n'


              output_len = len(cell['outputs'])

              if output_len > 0:
                for j in range(output_len):
                    output = cell['outputs'][j]
                    output_type = output['output_type']

                    if output_type == 'stream':
                      texts = output['text']
                      md_data += '\n<div class="op_wrap">'
                      for text in texts:
                        if text.find('Users/shindongwon') == -1:
                          md_data += '<op>' + text + '</op><br>'
                      md_data += '</div>\n'

                    elif output_type == 'execute_result':
                      data = output['data']
                      if 'text/plain' in data.keys():
                        texts = data['text/plain']
                        md_data += '\n<div class="op_wrap">'
                        for text in texts:
                          if text.find('Users/shindongwon') == -1:
                            md_data += '<op>' + text + '</op>'
                        md_data += '</div>\n\n'
                        
                    elif output_type == 'display_data':
                      data = output['data']
                      img = data['image/png']

                      img_path = f'/images/{post_name}/{i}_{j}.png'

                      if not os.path.isdir(f'./images/{post_name}/'):
                        os.makedirs(f'./images/{post_name}/')

                      # img path가 여기는 절대경로
                      md_data += f'![]({img_path})\n'

                      # img path가 여기는 상대경로
                      with open(f'.{img_path}', 'wb') as f:
                        f.write(base64.b64decode(img))


      with open(post_path, 'w') as f:
        f.write(md_data)

      processed_idx += 1

#remove temp folder
shutil.rmtree(temp_path)

print('processed: ', processed_idx)
print('already exist: ', already_exist_idx)
print('error occured: ', error_occured_idx)