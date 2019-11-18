import os


def viewResourcesDir():
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "resources"))
