import joblib
import numpy as np

from .model import ClassificationModel
from .data import DataLoader
from .callbacks import CosineAnnealingLearningRateSchedule
from .options import opt


model_parent = ClassificationModel()
model = model_parent.build_model()
embedding = model_parent.embedding

model.load_weights("curse_detection/weights-short.h5")

scheduler = CosineAnnealingLearningRateSchedule(opt)

data_type = "short"
try:
    x_train, x_train_mask, x_test, x_test_mask, y_train, y_test = joblib.load("curse_detection/data-{}.joblib".format(data_type))
except Exception as e:
    print(e)
    x_train, x_test, y_train, y_test = DataLoader("curse_detection/dataset/{}.txt".format(data_type)).get_data()

    print('embedding..')
    r = []
    r_mask = []
    for i in range(0, len(x_train), 500):
        vector, mask = embedding(x_train[i:i+500])
        r.extend(list(vector))
        r_mask.extend(list(mask))
    x_train = np.array(r)
    x_train_mask = np.array(r_mask)
    x_test, x_test_mask = embedding(x_test)

    import joblib
    joblib.dump((x_train, x_train_mask, x_test, x_test_mask, y_train, y_test), "curse_detection/data-{}.joblib".format(data_type))


try:
    model.fit((x_train, x_train_mask), y_train, batch_size=opt['batch'], epochs=opt['epoch'],
              callbacks=[scheduler], validation_data=((x_test, x_test_mask), y_test), verbose=1)
except KeyboardInterrupt:
    pass

import datetime
model.save_weights("curse_detection/weights-{}.h5".format(str(datetime.datetime.now()).replace(':', '')))
