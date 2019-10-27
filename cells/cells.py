from rx.subject import Subject
from .view.app import App


def main():
    subject = Subject()
    App.run(subject)


if __name__ == "__main__":
    main()
