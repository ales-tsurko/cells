from cells.view.app import App
from rx.subject import Subject


def main():
    subject = Subject()

    app = App(subject)

    app.run()


if __name__ == "__main__":
    main()
