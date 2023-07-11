import keyboard

class ExitOnKey:
    def __init__(self):
        self.is_exit = False

        def update_is_exit(remove_hook, e):
            # print(f'{e=} {e.scan_code=}')
            if e.scan_code == 1:  # esc.
                self.is_exit = True
                remove_hook()

        remove_hook = keyboard.hook(lambda e: update_is_exit(remove_hook, e))

    def __bool__(self):
        return self.is_exit
