import datetime


def make_tensorboard_name(net_name, variables):
    # print(f'{net_name=} {variables=}')
    net_name += datetime.datetime.now().strftime(' %y%m%d-%H%M%S')
    # Python 3.7+ guarantees ordered dictionary. Not sure about locals(), but assume order is ok unless shown otherwise.
    # https://stackoverflow.com/questions/5629023/the-order-of-keys-in-dictionaries
    for k, v in variables.items():
        # print(f'{k=} {v=}')
        net_name += f' {k}={v}'
    # print(f'{net_name=}')
    return net_name


if __name__ == "__main__":
    def mock_train(param_a, param_b = 2):
        tensorboard_name = make_tensorboard_name('mock_cnn', locals())
        print(f'{tensorboard_name}')

    mock_train(param_a=1)
    mock_train(param_a=3, param_b=4)


