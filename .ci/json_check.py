import json
import sys

if __name__ == '__main__':
  file_in = sys.argv[1]
  with open(file_in, 'r') as fr:
    cont = json.load(fr)
    print('json.load(%s) # check passed' % (sys.argv[1]))
    with open(file_in, 'w') as fw:
      write_data_ = json.dumps(cont, indent=2)
      write_data = (f'{write_data_}\n')
      fw.write(write_data)
