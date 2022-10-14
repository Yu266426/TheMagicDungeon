from data.modules.base.app import App

if __name__ == '__main__':
    app = App()
    while app.is_running:
        app.handle_events()
        app.update()
        app.draw()
        app.switch_state()
