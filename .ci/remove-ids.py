import glob
from pathlib import Path
import os
import json

if __name__ == '__main__':
  for patches in glob.glob('output/json/*.json', recursive=True):
    with open(patches, 'r') as fr:
      cont = json.load(fr)
      json_id = cont['patch']
      length_id = len(json_id)
      for i in range(0, length_id):
        del json_id[i]['app_titleid']
      write = json.dumps(cont, indent=2)
      with open(patches, 'w') as fw:
        fw.write(write)
