from rx.subject import Subject
from .view.app import App


def main():
    subject = Subject()

    app = App(subject)

    app.run()


if __name__ == "__main__":
    main()