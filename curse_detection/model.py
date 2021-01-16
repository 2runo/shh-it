# 모델을 정의한다.
import tensorflow as tf
from tensorflow.keras.layers import Dense, Bidirectional, LSTM, Concatenate, Dropout, add, Embedding
from tensorflow.keras import Input, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.constraints import min_max_norm
import tensorflow_hub as hub
import numpy as np


input_shape = (30, 128)

norm2 = min_max_norm(-2, 2)
norm3 = min_max_norm(-3, 3)


def flatten(l):
    # flatten
    r = []
    for i in l:
        if isinstance(i, list):
            r.extend(flatten(i))
        else:
            r.append(i)
    return r


class BahdanauAttention(tf.keras.Model):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = Dense(units)
        self.W2 = Dense(units)
        self.V = Dense(1)

    def call(self, values, query, mask):
        hidden_with_time_axis = tf.expand_dims(query, 1)

        score = self.V(tf.nn.tanh(
            self.W1(values) + self.W2(hidden_with_time_axis)))

        score = score + (tf.expand_dims(mask, 2) * -1e+9)

        attention_weights = tf.nn.softmax(score, axis=1)

        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


class ClassificationModel:
    def __init__(self):
        self.embed = hub.load("https://tfhub.dev/google/nnlm-ko-dim128-with-normalization/2")

    def embedding(self, tokens, pad=None):
        vectors = np.array(self.embed(flatten(tokens)))
        if not pad:
            pad = [np.zeros_like(vectors[0]).tolist()]
        r = []
        mask = []
        for i in range(len(tokens)):
            length = len(tokens[i])
            mask.append([0]*length + [1]*(input_shape[0] - length))
            r.append(vectors[:length].tolist() + pad * (input_shape[0] - length))
            vectors = vectors[length:]
        return np.array(r), np.array(mask)

    @staticmethod
    def lstm(units, return_state=False):
        return LSTM(units, dropout=0.4, return_sequences=True, return_state=return_state, recurrent_constraint=norm2, kernel_constraint=norm2)

    def attention_block(self):
        # 양방향 LSTM 어텐션 메커니즘
        inp = Input(shape=input_shape)
        mask_inp = Input(shape=(input_shape[0],))
        inter = Bidirectional(self.lstm(128))(inp)
        inter = tf.keras.layers.LayerNormalization()(inter)
        inter = Bidirectional(self.lstm(128))(inter)
        inter = tf.keras.layers.LayerNormalization()(inter)
        inter = Bidirectional(self.lstm(64))(inter)
        inter = tf.keras.layers.LayerNormalization()(inter)
        lstm, forward_h, forward_c, backward_h, backward_c = Bidirectional(self.lstm(64, return_state=True))(inter)

        attention = BahdanauAttention(128)  # 가중치 크기 정의
        state_h = Concatenate()([forward_h, backward_h])  # 은닉 상태
        context_vector, attention_weights = attention(lstm, state_h, mask_inp)
        return [inp, mask_inp], context_vector, attention_weights

    def build_model(self):
        # 모델을 반환한다.
        inp, context_vector, attention_weights = self.attention_block()

        inter = Dropout(0.4)(context_vector)
        inter = Dense(64, activation="relu")(inter)
        output = Dense(1, activation="sigmoid", kernel_constraint=norm2)(inter)
        model = Model(inputs=inp, outputs=output)

        optimizer = Adam(lr=0.0001)
        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        return model


if __name__ == "__main__":
    classficiation_model = ClassificationModel()
    model = classficiation_model.build_model()
    model.summary()

