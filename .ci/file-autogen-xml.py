import glob
from pathlib import Path
import os
import xml.etree.ElementTree as ET
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        entry = 0
        for patches in glob.glob(sys.argv[1], recursive=True):
            print('Source: %s' % (patches))
            with open(patches, 'r') as fr:
                string_data = fr.read()
                string_data = string_data.replace('<?xml version="1.0" encoding="utf-8"?>\n', f'<?xml version="1.0" encoding="utf-8"?>\n<!-- File generated from: {patches} -->\n')
                root = ET.fromstring(string_data)
                ID = root.findall('TitleID/ID')
                for i in ID:
                    out = ('output/xml/{}.xml'.format(i.text))
                    print('Output: %s' % (out))
                    with open(out, 'w') as fw:
                        fw.write(string_data)
                    entry = entry + 1
        print('processed %u entries' % (entry))
    else:
        print('path to glob not provided')
