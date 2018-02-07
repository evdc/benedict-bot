import glob
import numpy as np

# Load a dir of data where each filename is a different category
# containing examples for that category, one per line
def load_dir(directory):
    X = []
    for filename in glob.glob(directory+'/*.txt'):
        label = filename.split('/')[-1].split('.')[0]
        with open(filename, 'r') as f:
            for line in f:
                X.append((line.strip(), label))
    return X

# Load a file of examples with two tab-sep columns of data and label, one per line
def load_file(filename, sep='\t'):
    X = []
    Y = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = line.strip().split('\t')
            X.append(x)
            Y.append(y)
    return np.array(X), np.array(Y)

def write_file(filename, data, sep='\t'):
    with open(filename, 'w') as f:
        for x in data[:-1]:
            f.write('%s\t%s\n' % x)
        f.write('%s\t%s' % data[-1])

def train_test_split(data, pct):
    idx = int(len(data) * pct)
    return data[:idx], data[idx:]

def x_y_split(data):
    return [x[0] for x in data], [x[1] for x in data]

def labels2indexes(y, label_names):
    return np.array([label_names.index(y_) for y_ in y])

def indexes2labels(y, label_names):
    return np.array([label_names[y_] for y_ in y])

def from_categorical(Y):
    return np.nonzero(Y)[1]

def gen_train_test_data(directory):
    data = load_dir(directory)
    np.random.shuffle(data)
    train, test = train_test_split(data, 0.8)
    write_file(directory + '/train.txt', train)
    write_file(directory + '/test.txt', test)