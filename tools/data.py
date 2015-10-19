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

selected_length = 476

def get_datasets():
    f = get_dataset_file()
    zf = zipfile.ZipFile(f)
        
    data = zf.open('MU.txt', 'r')
    entire_dataset = []
    current_event = []
    
    print 'Reading data file'
    for l in data:
        id, event, device, channel, code, size, data = l.split('\t')
        signals = [int(n) for n in data.split(',')]
        
        if len(signals) == selected_length:
            current_event.extend(signals)
            if len(current_event) == selected_length * 4: # we assume all channels from an event are in sequence
                current_event.append(np.array([int(code)]))

                entire_dataset.append(np.array(current_event).reshape(selected_length * 4+1))
                current_event = []

    entire_dataset = np.array(entire_dataset)
    return entire_dataset[:10000], entire_dataset[10000:]