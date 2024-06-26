import glob
from pathlib import Path
import os
import xml.etree.ElementTree as ET
import sys

if __name__ == '__main__':
    if len(sys.argv) == 4:
        entry = 0
        for patches in glob.glob(sys.argv[1], recursive=True):
            # print('Source: %s' % (patches))
            with open(patches, 'r') as fr:
                string_data = fr.read()
                string_data = string_data.replace('<?xml version="1.0" encoding="utf-8"?>\n', f'<?xml version="1.0" encoding="utf-8"?>\n<!-- File generated from: {patches} @ {sys.argv[2]} -->\n')
                root = ET.fromstring(string_data)
                ID = root.findall('TitleID/ID')
                for i in ID:
                    if not (i.text.startswith('CUSA') or i.text.startswith('PPSA')):
                        print(f'Ignored {i.text}')
                        continue
                    out = ('{}/{}.xml'.format(sys.argv[3], i.text))
                    # print('Output: %s' % (out))
                    with open(out, 'w') as fw:
                        fw.write(string_data)
                    entry = entry + 1
        print('processed %u entries' % (entry))
        exit(0)
    else:
        print('path to glob not or current time provided')
        exit(1)
