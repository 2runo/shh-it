from konlpy.tag import Komoran
from tensorflow.keras import Model

from model import ClassificationModel, input_shape


if __name__ == "__main__":
    komoran = Komoran()

    model_parent = ClassificationModel()
    model = model_parent.build_model()
    embedding = model_parent.embedding

    model.load_weights("curse_detection/weights-short.h5")


    att_model = Model(inputs=[model.input], outputs=model.layers[10].output)

    while True:
        inp = input(':')
        inp, mask = embedding([komoran.morphs(inp)])
        out = model.predict((inp, mask)).squeeze(1)
        att = att_model.predict((inp, mask))[1].squeeze(2)
        print(att)
        print(out)
