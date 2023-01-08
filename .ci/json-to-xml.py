import glob
from pathlib import Path
import os
import json

# https://stackoverflow.com/a/6117042
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

rlist = { '\"' : '\'',
          '\n' : '\\n',
        }

if __name__ == '__main__':
  entries = 0
  for patches in glob.glob('patches/json/*.json', recursive=True):
    new_xml = ''
    with open(patches, 'r') as fr:
      #print(patches)
      cont = json.load(fr)
      json_id = cont['patch']
      new_xml = '<?xml version="1.0" encoding="utf-8"?>\n'
      new_xml += (f'<Patch>\n')
      id_list = json_id[0]['app_titleid']
      new_xml += (f'    <TitleID>\n')
      for h in range(0, len(id_list)):
          new_xml += (f'        <ID>{id_list[h]}</ID>\n')
      new_xml += (f'    </TitleID>\n')
      for i in range(0, len(json_id)):
          title = json_id[i].get('title')
          name = json_id[i].get('name')
          appver = json_id[i].get('app_ver')
          app_elf = json_id[i].get('app_elf')
          patch_ver = json_id[i].get('patch_ver')
          note = json_id[i].get('note')
          author = json_id[i].get('author')
          new_xml += (f'    <Metadata')
          if title != None:
              new_xml += (f' Title="{title}"\n')
          if name != None:
              new_xml += (f'              Name="{name}"\n')
          if note != None:
              new_xml += (f'              Note="{replace_all(note, rlist)}"\n')
          if author != None:
              new_xml += (f'              Author="{author}"\n')
          if patch_ver != None:
              new_xml += (f'              PatchVer="{patch_ver}"\n')
          if appver != None:
              new_xml += (f'              AppVer="{appver}"\n')
          if app_elf != None:
              new_xml += (f'              AppElf="{app_elf}">\n')
          new_xml += '        <PatchList>\n'
          patch_list = json_id[i]['patch_list']
          for j in range (0, len(patch_list)):
              ptype = patch_list[j].get('type')
              paddr = patch_list[j].get('addr')
              pval = patch_list[j].get('value')
              pcomm = patch_list[j].get('comment')
              if pcomm != None:
                  new_xml += ('            <!-- {} -->\n'.format(pcomm))
              if ptype != None and paddr != None and pval != None:
                new_xml += (f'            <Line Type="{ptype}" Address="{paddr}" Value="{pval}"/>\n')
          new_xml += '        </PatchList>\n'
          new_xml += '    </Metadata>\n'
      new_xml += '</Patch>\n'
      #print(new_xml)
      outpath = ('{}'.format(patches.replace('json', 'xml')))
      print(outpath)
      with open(outpath, 'w') as fw:
          fw.write(new_xml)
