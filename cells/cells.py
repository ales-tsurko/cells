from rx.subject import Subject
from .view.app import App
from .models.document import Document


def main():
    subject = Subject()
    document = Document(subject)
    App.run(subject)


if __name__ == "__main__":
    main()
