import sys
import cv2
import qrcode

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5 import uic, QtGui

# Main application window class.
class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("APP_GUI.ui", self)
        self.show()

        self.current_file = ""
        self.actionLoad.triggered.connect(self.load_image)
        self.loadButton.clicked.connect(self.load_image)
        self.actionSave.triggered.connect(self.save_image)
        self.actionQuit.triggered.connect(self.quit_program)
        self.generateButton.clicked.connect(self.generate_code)
        self.readButton.clicked.connect(self.read_code)

    # Open a file dialog to load an image.    
    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Ensure the filter works on all platforms

        # Set the file filter to show only image files
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "Images (*.png *.jpg *.jpeg);",
                                                  options=options)

        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(300, 300)
            self.label.setScaledContents(True)
            self.label.setPixmap(pixmap)

    # Open a file dialog to save the current image.    
    def save_image(self):
        options = QFileDialog.Option()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG (*.png)",
                                                  options=options)
        if filename != "":
            image = self.label.pixmap()
            image.save(filename, "PNG")

    # Generate a QR code based on the text in the text edit.    
    def generate_code(self):
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=20,
                           border=2)

        qr.add_data(self.textEdit.toPlainText())
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white")
        image.save("currentqr.png")
        pixmap = QtGui.QPixmap("currentqr.png")
        pixmap = pixmap.scaled(300, 300)
        self.label.setScaledContents(True)
        self.label.setPixmap(pixmap)

    # Read a QR code from the loaded image.        
    def read_code(self):
        if self.current_file == "":
            QMessageBox.warning(self, "Warning", "Please load an image of a QR code to read it.")
            return

        image = cv2.imread(self.current_file)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(image)

        if not data:
            QMessageBox.critical(self, "Error", "No QR code found in the loaded image.")
            return

        self.textEdit.setText(data)

    # Quit the application.
    def quit_program(self):
        sys.exit(0)

# Entry point for the application.
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == "__main__":
    main()
