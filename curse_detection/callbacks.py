import tensorflow as tf
import tensorflow.keras.backend as backend
import math


# CosineAnneling Example.
class CosineAnnealingLearningRateSchedule(tf.keras.callbacks.Callback):
    # constructor
    def __init__(self, opt):
        self.epochs = opt['epoch']
        self.cycles = opt['cycle']
        self.lr_max = opt['max-lr']
        self.min_lr = opt['min-lr']
        self.lrates = list()

    # caculate learning rate for an epoch
    def cosine_annealing(self, epoch, n_epochs, n_cycles, lrate_max):
        # 전체 epoch / 설정 cycle 수만큼 cycle을 반복
        epochs_per_cycle = math.floor(n_epochs / n_cycles)
        cos_inner = (math.pi * (epoch % epochs_per_cycle)) / (epochs_per_cycle)

        return lrate_max / 2 * (math.cos(cos_inner) + 1)

    # calculate and set learning rate at the start of the epoch
    def on_epoch_begin(self, epoch, logs=None):
        lr = self.cosine_annealing(epoch, self.epochs, self.cycles, self.lr_max)
        print('\nEpoch %05d: CosineAnnealingScheduler setting learng rate to %s.' % (epoch + 1, lr))

        # set learning rate
        backend.set_value(self.model.optimizer.lr, lr)
        # log value
        self.lrates.append(lr)
