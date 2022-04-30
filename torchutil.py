import os
import __main__
import torch
import keyboard
import tqdm

def get_current_script_name():
    return os.path.splitext(os.path.basename(__main__.__file__))[0]


def get_torch_device():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device {device}')
    return device


def training_loop(model_evaluate_fn, model, optimizer, epochs, iters_per_epoch, model_name=get_current_script_name(),
                  visualize_fn=lambda *args: None, cache_mode='train'):
    model_file = f'{model_name}.pt'
    if cache_mode == 'load' or cache_mode == 'resume':
        try:
            model.load_state_dict(torch.load(model_file))
            model.eval()
            if cache_mode == 'load':
                visualize_fn(0)
                return
        except (FileNotFoundError, RuntimeError):
            print(f'Failed to load model from {model_file}, training...')

    keep_running = True
    def on_press_x(_):
        nonlocal keep_running
        keep_running = False
    key_handler = keyboard.on_press_key('x', on_press_x)


    for epoch in range(epochs):
        running_loss = 0.0
        for i in tqdm.tqdm(range(iters_per_epoch)):
            optimizer.zero_grad()
            loss = model_evaluate_fn()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if not keep_running:
                break

        print(f'[{epoch}] loss: {running_loss:.10f}')
        visualize_fn(running_loss)
        torch.save(model.state_dict(), model_file)

        if not keep_running:
            break

    keyboard.unhook_key(key_handler)
