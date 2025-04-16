############################
# @author EliasDH Team     #
# @see https://eliasdh.com #
# @since 01/01/2025        #
############################

from PyQt5.QtWidgets import QApplication
import sys
from gui.window import MousePadWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MousePadWindow()
    window.show()
    sys.exit(app.exec_())