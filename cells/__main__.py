from rx.subject import Subject
from .view.app import App
from .models.document import Document
from .settings import Settings


def main():
    subject = Subject()

    Settings(subject)
    Document(subject)

    app = App(subject)

    app.run()


if __name__ == "__main__":
    main()