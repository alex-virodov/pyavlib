import matplotlib.pyplot as plt
from pyavlib.pltutil import plt_clf_subplots, plt_show_in_loop, UpdatablePlot
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchsummary
import torch.optim as optim
from pyavlib.nputil import list_of_tuples_to_tuple_of_lists
import random
from pyavlib.keyboard_util import ExitOnKey

def generator(x):
    return x, 1.0 if x > 25 else 0.0


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc2 = nn.Linear(1, 1)

    def forward(self, x):
        x = self.fc2(x)
        x = F.sigmoid(x)
        return x

def main():
    torch.manual_seed(1)
    random.seed(1)
    np.random.seed(1)
    ax = plt_clf_subplots(2, 2, rowspan_colspan_map={0: (1, 2)})
    xs = np.linspace(-100, 100, num=20)
    _, ys = list_of_tuples_to_tuple_of_lists([generator(x) for x in xs])
    ys = np.array(ys)
    ax[0].plot(xs, ys, 'm--')
    ax[0].set_ylim([-0.5, 1.2])
    result_plot = UpdatablePlot(ax[0], set_xdata=False)

    device = torch.device('cuda' if torch.cuda.is_available() and False else 'cpu')
    print(f'{torch.cuda.is_available()=} {device=}')

    net = Net().to(device)
    xs_tensor = torch.tensor(xs.reshape(-1, 1), dtype=torch.float32)
    ys_tensor = torch.tensor(ys.reshape(-1, 1))
    torchsummary.summary(net, xs_tensor, verbose=2, device=device)

    # First run before training.
    print(f'{net.fc2.weight=}')
    outputs = net.forward(xs_tensor)
    print(f'{outputs.shape=}')

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)

    is_exit = ExitOnKey()

    for epoch in range(2000):  # loop over the dataset multiple times
        running_loss = 0.0
        for i in range(1):
            optimizer.zero_grad()
            outputs = net.forward(xs_tensor)
            # print(f'{outputs.transpose(0, 1)=}')
            # print(f'{gt_batch_tensor.transpose(0, 1)=}')
            loss = criterion(outputs.transpose(0, 1), ys_tensor.transpose(0, 1))
            # print(f'{loss=}')
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            if is_exit: break
        if is_exit: break

        print(f'{outputs.device=}')
        print(f'[epoch={epoch + 1}] loss: {running_loss=:.3f}')
        result_plot.plot_line('outputs', xs, outputs.cpu().detach(), 'bo-')
        plt_show_in_loop()

    print('Finished Training')





if __name__ == '__main__':
    main()