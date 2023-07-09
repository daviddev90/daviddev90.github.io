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

for root, dirs, files in os.walk(input_path):
    for file in files:

        if not (file.endswith('.ipynb') or file.endswith('.md')):
            continue
        
        file_path = os.path.join(root, file)

        # 파일의 생성 날짜를 가져옴
        creation_date = datetime.fromtimestamp(os.path.getctime(file_path))

        if file.endswith('.ipynb'):
            shutil.copy2(file_path, temp_path)

            # 파일 이름을 'YYYY-MM-DD-NN.ipynb' 형식으로 변경
            new_file_name = creation_date.strftime('%Y-%m-%d-') + creation_date.strftime('%H%M%S') + '.ipynb'
            new_file_path = os.path.join(temp_path, new_file_name)
            os.rename(os.path.join(temp_path, file), new_file_path)

            try:
              with io.open(new_file_path, 'r', encoding='utf-8') as f:
                  notebook = json.load(f)

              # Markdown 셀 생성
              file_name = os.path.splitext(file)[0]  # 파일 이름에서 확장자 제거
              group_name = file_path.split('/')[-2].split('.')[-1]

              markdown_cell = {
                  "cell_type": "markdown",
                  "metadata": {},
                  "source": [
                      "---\n",
                      "layout: single\n",
                      f'title: "[{group_name}]{file_name}"\n',
                      "categories: ml\n",
                      "tag: [python, ml]\n",
                      "toc: true\n",
                      "author_profile: false\n",
                      "typora-root-url: ../\n",
                      "sidebar:\n",
                      '  nav: "docs"\n',
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
                os.remove(new_file_path)


        if file.endswith('.md'):  # md 파일만 처리
            shutil.copy2(file_path, output_path)

            # 파일 이름을 'YYYY-MM-DD-NN.ipynb' 형식으로 변경
            new_file_name = creation_date.strftime('%Y-%m-%d-') + creation_date.strftime('%H%M%S') + '.md'
            new_file_path = os.path.join(output_path, new_file_name)
            os.rename(os.path.join(output_path, file), new_file_path)

            try:
                # 파일 열기 및 데이터 읽기
                with io.open(new_file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                file_name = os.path.splitext(file)[0]  # 파일 이름에서 확장자 제거
                group_name = file_path.split('/')[-2].split('.')[-1]

                # 새로운 데이터 생성 (상단에 내용 추가)
                new_data = "---\n" \
                        "layout: single\n" \
                         f'title: "[{group_name}]{file_name}"\n' \
                        'categories: ml\n' \
                        'tag: [python, ml]\n' \
                        'toc: true\n' \
                        'author_profile: false\n' \
                        'typora-root-url: ../\n' \
                        '\n' \
                        'sidebar:\n' \
                        '  nav: "docs"\n' \
                        '---\n' \
                        '\n' + contents

                # 파일 열기 및 데이터 쓰기
                with io.open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(new_data)

            except:
                # remove file
                os.remove(new_file_path)

def ipynb_to_md(ipynb_path, file_name):
  md_data = ''

  with io.open(ipynb_path, 'r', encoding='utf-8') as f:
      notebook = json.load(f)

      for i in range(len(notebook['cells'])):
        cell = notebook['cells'][i]
        cell_type = cell['cell_type']


        if cell_type == 'markdown':
          for j in range(len(notebook['cells'][i]['source'])):
            md_data += notebook['cells'][i]['source'][j]
          
          md_data += '\n'


        if cell_type == 'code':

          md_data += '\n``` python\n'
          sources = cell['source']

          for j in range(len(sources)):
            # if last item
            md_data += sources[j] + '\n'

          md_data += '\n```\n'


          output_len = len(cell['outputs'])

          if output_len > 0:
            for j in range(output_len):
                output = cell['outputs'][j]
                output_type = output['output_type']

                if output_type == 'stream':
                  texts = output['text']
                  md_data += '\n'
                  for text in texts:
                    md_data += '\> ' + text
                  md_data += '\n'

                elif output_type == 'execute_result':
                  data = output['data']
                  if 'text/plain' in data.keys():
                    texts = data['text/plain']
                    md_data += '\n'
                    for text in texts:
                      md_data += '\> ' + text
                    md_data += '\n'
                    
                elif output_type == 'display_data':
                  data = output['data']
                  img = data['image/png']

                  img_path = f'/images/{file_name}/{i}_{j}.png'

                  if not os.path.isdir(f'./images/{file_name}/'):
                    os.makedirs(f'./images/{file_name}/')

                  # img path가 여기는 절대경로
                  md_data += f'![]({img_path})\n'

                  # img path가 여기는 상대경로
                  with open(f'.{img_path}', 'wb') as f:
                    f.write(base64.b64decode(img))


  with open(f'{output_path}{file_name}.md', 'w') as f:
    f.write(md_data)



for root, dirs, files in os.walk(temp_path):
    for file in files:
        if file.endswith('.ipynb'):
            ipynb_path = os.path.join(root, file)

            file_name = os.path.splitext(file)[0]
            ipynb_to_md(ipynb_path, file_name)

# remove temp folder
shutil.rmtree(temp_path)