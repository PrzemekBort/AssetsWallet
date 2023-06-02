import sys
from Source.MainApplication import MainProgram


if __name__ == "__main__":
    app = MainProgram(sys.argv)
    sys.exit(app.exec())
