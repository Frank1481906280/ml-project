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

def split_into_subsequences(data, n_sequences, length):
    output = np.zeros((data.shape[0]*n_sequences, length*4+1))
    for i in range(data.shape[0]):
        steps = data[i, 0] / n_sequences

        for j in range(n_sequences):
            output[i*n_sequences+j,:length]           = data[i, j*steps: j*steps+length]
            output[i*n_sequences+j,length:length*2]   = data[i, j*steps+512: j*steps+512+length]
            output[i*n_sequences+j,length*2:length*3] = data[i, j*steps+512*2: j*steps+512*2+length]
            output[i*n_sequences+j,length*3:length*4] = data[i, j*steps+512*3: j*steps+512*3+length]
            output[i*n_sequences+j,-1] = data[i, -1]

    return output