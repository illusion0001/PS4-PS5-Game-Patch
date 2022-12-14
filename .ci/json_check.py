import json
import sys

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
          '\n      \"note\": \"\",' : '',
        }

if __name__ == '__main__':
  file_in = sys.argv[1]
  with open(file_in, 'r') as fr:
    cont = json.load(fr)
    print('json.load(%s) # check passed' % (sys.argv[1]))
    with open(file_in, 'w') as fw:
      fw.write((f'{replace_all(json.dumps(cont, indent=2), rlist)}\n'))
