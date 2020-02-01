import os
import sys
import platform
from PySide2.QtCore import QTranslator, QLocale, Qt
from PySide2.QtWidgets import QApplication
from mywallet.mainwindow import MainWindow


if __name__ == '__main__':
    module_name = 'mywallet'

    # Fix for black screen ???
    QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
    app = QApplication(sys.argv)

    frozen = getattr(sys, 'frozen', False)

    if (platform.system() == 'Windows' and frozen):
        root_dir = os.path.dirname(sys.executable)
        translations_path = os.path.join(root_dir, 'lib', 'PySide2', 'translations')
        for lib in ('qtbase', 'qtwebengine'):
            translator = QTranslator()
            translator.load(QLocale(), lib, '_', translations_path)
            app.installTranslator(translator)
        app_translator = QTranslator()
        app_translation_path = os.path.join(root_dir, 'lib', module_name, 'translations')
        app_translator.load(QLocale(), module_name, '_', app_translation_path)
        app.installTranslator(app_translator)
    elif not frozen:
        app_translator = QTranslator()
        app_translator.load(QLocale(), module_name, '_', os.path.join(module_name, 'translations'))
        app.installTranslator(app_translator)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
