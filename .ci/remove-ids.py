import glob
from pathlib import Path
import os
import json

# https://stackoverflow.com/a/6117042
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

rlist = { '\n          \"type\"' : ' \"type\"',
          ',\n          \"addr\"' : ', \"addr\"',
          ',\n          \"value\"' : ', \"value\"',
          '\"\n        },' : '\" },',
          '\"\n        }' : '\" }',
          '\n          \"comment\"' : ' \"comment\"',
        }

if __name__ == '__main__':
  entries = 0
  for patches in glob.glob('output/json/*.json', recursive=True):
    with open(patches, 'r') as fr:
      cont = json.load(fr)
      json_id = cont['patch']
      length_id = len(json_id)
      for i in range(0, length_id):
        del json_id[i]['app_titleid']
        entries += 1
      with open(patches, 'w') as fw:
        fw.write((f'{replace_all(json.dumps(cont, indent=2), rlist)}\n'))
  print('processed %i entries' % (entries))
