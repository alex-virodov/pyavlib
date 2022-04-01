import datetime
from enum import Enum
import itertools


def make_tensorboard_name(net_name, variables, timestamp=True):
    # print(f'{net_name=} {variables=}')
    if timestamp:
        net_name += datetime.datetime.now().strftime(' %y%m%d-%H%M%S')
    # Python 3.7+ guarantees ordered dictionary. Not sure about locals(), but assume order is ok unless shown otherwise.
    # https://stackoverflow.com/questions/5629023/the-order-of-keys-in-dictionaries
    for k, v in variables.items():
        # print(f'{k=} {v=}')
        net_name += f' {k}={v}'
    # print(f'{net_name=}')
    return net_name


class UniqueList(list):
    """Like list, but with the '==' operator disabled. This is to disable aliasing in python enums."""

    def __init__(self, *args):
        if len(args) > 0 and (args[0] is list or args[0] is tuple):
            super().__init__(args[0])
        else:
            super().__init__(args)

    def __eq__(self, other):
        return False


class HyperParamsEnum(Enum):
    """A specialization of Enum that has a simpler printing of enum objects so that dict print looks simpler."""
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

def generate_hyperparams(hyperparams_enum, hyperparams_filter=None):
    """Generate an iterable of hyperparameters instances.

    Parameters:
        hyperparams_enum: enum with e.g.: a=[1, 2], b=[3, 4] or todo: dict/kwargs, but enum is best?
        filter:
            None,
            or an int for the run number (useful for after-the-fact reruns in the same sequence),
            [nyi] or a dictionary with subset of matching keys to set a specific value for each key,

    Returns:
        iterable of form [{a:1, b:3}, {a:1, b:4}, {a:2, b:3}, {a:2, b:4}] or a filtered version of thereof.
    """

    enum_value_tuples = [value.value for name, value in hyperparams_enum.__members__.items()]
    enum_key_list = hyperparams_enum.__members__.values()
    #print(f'{enum_value_tuples=}')
    #print(f'{enum_key_list=}')

    # https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
    for instance in itertools.product(*enum_value_tuples):
        yield dict(zip(enum_key_list, instance))


def __quick_test():
    def mock_train(param_a, param_b = 2):
        tensorboard_name = make_tensorboard_name('mock_cnn', locals())
        print(f'{tensorboard_name}')

    mock_train(param_a=1)
    mock_train(param_a=3, param_b=4)

    class HPARAMS(HyperParamsEnum):
        fd_train = UniqueList(True, False)
        l1_n = UniqueList(16, 32, 64)

    for hyperparam_instance in generate_hyperparams(HPARAMS):
        print(f'{hyperparam_instance=}')
        print(f'{hyperparam_instance[HPARAMS.l1_n]=}')
        print(f"name={make_tensorboard_name('mock_cnn_hyper', hyperparam_instance)}")

if __name__ == "__main__":
    __quick_test()



