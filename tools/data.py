from os.path import isfile
import zipfile
import numpy as np

dataset_path = './data/MU.zip'

def get_dataset_file():
    if not isfile(dataset_path):
        import urllib
        origin = (
            'http://www.mindbigdata.com/opendb/MindBigData-MU-v1.0.zip'
        )
        print 'Downloading data from %s' % origin
        urllib.urlretrieve(origin, dataset_path)
    return open(dataset_path, 'rb')

def get_datasets():
    f = get_dataset_file()
    zf = zipfile.ZipFile(f)
        
    data = zf.open('MU.txt', 'r')
    entire_dataset = []
    current_event = np.zeros(512 * 4 + 2)
    
    print 'Reading data file'
    i = 0

    for l in data:
        id, event, device, channel, code, size, data = l.split('\t')

        signals = np.array([int(val) for val in data.split(',')])
        
        current_event[1+ i*512:1+ i*512 + min(len(signals), 512)] = signals[:512]
        i += 1

        if i == 4: # we assume all channels from an event are in sequence
            current_event[-1] = int(code)
            current_event[0] = min(len(signals), 512)

            entire_dataset.append(current_event)
            current_event = np.zeros(512 * 4 + 2)
            i = 0

    entire_dataset = np.array(entire_dataset)
    return entire_dataset[:30000], entire_dataset[30000:]