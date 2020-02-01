from cx_Freeze import setup, Executable, build_exe as build_exe_orig
from diffui.version import VERSION
import shutil
import os
import sys
import glob


def remove_path(path):
    print('Removing {} ...'.format(path))
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def pyside2_libs(modules):
    res = []
    for module in modules:
        res.append('{}.pyd'.format(module))
        res.append('{}.pyi'.format(module))
    return res


executables = [Executable('diffui/__main__.py',
                          icon='./diffui.ico',
                          targetName='diffui.exe',
                          base='Win32GUI')]

excludes = ['logging', 'unittest', 'email', 'http', 'xml',
            'bz2', 'select', 'pydoc_data']

zip_include_packages = ['collections', 'encodings', 'importlib']

pyside2_binaries = ['designer.exe', 'lconvert.exe', 'linguist.exe', 'lrelease.exe', 'lupdate.exe',
                    'pyside2-rcc.exe', 'pyside2-lupdate.exe', 'qtdiag.exe', 'pyside2.abi3.lib']

pyside2_modules = ['Qt3DAnimation', 'Qt3DCore', 'Qt3DExtras', 'Qt3DInput', 'Qt3DLogic',
                   'Qt3DRender', 'QtAxContainer', 'QtCharts', 'QtConcurrent', 'QtDataVisualization',
                   'QtHelp', 'QtLocation', 'QtMultimedia', 'QtMultimediaWidgets', 'QtOpenGL',
                   'QtOpenGLFunctions', 'QtPositioning', 'QtQml', 'QtQuick', 'QtQuickWidgets',
                   'QtRemoteObjects', 'QtScript', 'QtScriptTools', 'QtScxml', 'QtSensors',
                   'QtSql', 'QtSvg', 'QtTest', 'QtTextToSpeech', 'QtUiTools',
                   'QtWinExtras', 'QtXml', 'QtXmlPatterns']

qt_libs = ['Qt5Bluetooth.dll', 'Qt5Bodymovin.dll', 'Qt5Charts.dll', 'Qt5Concurrent.dll', 'Qt5DataVisualization.dll',
           'Qt5DBus.dll', 'Qt5Designer.dll', 'Qt5DesignerComponents.dll', 'Qt5Gamepad.dll', 'Qt5Help.dll',
           'Qt5Location.dll', 'Qt5Multimedia.dll', 'Qt5MultimediaQuick.dll', 'Qt5MultimediaWidgets.dll',
           'Qt5NetworkAuth.dll', 'Qt5Nfc.dll', 'Qt5OpenGL.dll', 'Qt5PositioningQuick.dll', 'Qt5Purchasing.dll',
           'Qt5QuickControls2.dll', 'Qt5QuickParticles.dll', 'Qt5QuickShapes.dll', 'Qt5QuickTemplates2.dll',
           'Qt5QuickTest.dll', 'Qt5RemoteObjects.dll', 'Qt5Script.dll', 'Qt5ScriptTools.dll', 'Qt5Scxml.dll',
           'Qt5Sensors.dll', 'Qt5SerialBus.dll', 'Qt5SerialPort.dll', 'Qt5Sql.dll', 'Qt5Svg.dll',
           'Qt5Test.dll', 'Qt5TextToSpeech.dll', 'Qt5VirtualKeyboard.dll', 'Qt5WinExtras.dll', 'Qt5Xml.dll',
           'Qt5XmlPatterns.dll', 'Qt53DAnimation.dll', 'Qt53DCore.dll',
           'Qt53DExtras.dll', 'Qt53DInput.dll', 'Qt53DLogic.dll', 'Qt53DQuick.dll', 'Qt53DQuickAnimation.dll',
           'Qt53DQuickExtras.dll', 'Qt53DQuickInput.dll', 'Qt53DQuickRender.dll', 'Qt53DQuickScene2D.dll',
           'Qt53DRender.dll',
           ]

bin_path_items = {
    'PySide2': {
        'excludes': [
                        'examples', 'glue', 'include', 'qml', 'scripts', 'support',
                        'typesystems',
                        ('resources', ('qtwebengine_devtools_resources.pak',)),
                    ] + pyside2_binaries + pyside2_libs(pyside2_modules) + qt_libs,
        'includes': [
                        ('plugins', ('platforms', 'platformthemes', 'styles')),
                        ('translations\\qtbase_ru.qm', 'translations\\qtwebengine_ru.qm',
                         'translations\\qtwebengine_locales\\ru.pak'),
                    ]
    },
    'diffui': {
        'excludes': [
                        ('ui', ('documentchangeitemwidget.ui', 'documentchangeswidget.ui', 'documentview.ui',
                                'mainwindow.ui', 'progressdialog.ui', 'settingsdialog.ui',
                                'workingdirectorydialog.ui')),
                        ('translations', ('diffui_ru.ts',)),
                    ],
        'includes': [
                        ('resources', ('__init__.pyc', 'resources_rc.pyc'))
                    ]
    },
    'shiboken2': {
        'excludes': [
                        'docs', 'files.dir', 'shiboken2.abi3.lib'
                    ]
    }
}


class diffui_build_exe(build_exe_orig):
    def run(self):
        if os.path.exists(self.build_exe):
            shutil.rmtree(self.build_exe)
        self.pre_processing()
        super(diffui_build_exe, self).run()
        self.post_processing()

    def pre_processing(self):
        from bootstrap import genui, localization_compile
        try:
            genui()
            localization_compile()
        except Exception as e:
            print('Pre processing failure: {}'.format(e))
            sys.exit(1)

    def post_processing(self):
        # Copy python3.dll
        exec_python = sys.executable
        shutil.copyfile(os.path.join(os.path.dirname(exec_python), 'python3.dll'),
                        os.path.join(self.build_exe, 'python3.dll'))
        # vcruntime
        shutil.copyfile(os.path.join(os.path.dirname(exec_python), 'vcruntime140.dll'),
                        os.path.join(self.build_exe, 'vcruntime140.dll'))
        # diffui-bat
        with open(os.path.join(self.build_exe, 'diffui-run.bat'), mode='w') as fp:
            fp.writelines(['SET QT_PLUGIN_PATH=lib/PySide2/plugins\n',
                           'diffui.exe'])
        # api ms???
        for dll in glob.glob(os.path.join(self.build_exe, 'api*.dll')):
            os.remove(dll)
        for pkg, pkg_data in bin_path_items.items():
            print('\n********************\n')
            print('Processing {} ...'.format(pkg))
            fullpkgpath = os.path.join(os.path.abspath(os.path.curdir), self.build_exe, 'lib', pkg)
            for item_type, filespec in pkg_data.items():
                if item_type == 'excludes':
                    for item in filespec:
                        if isinstance(item, str):
                            fullpath = os.path.join(fullpkgpath, item)
                            remove_path(fullpath)
                        elif isinstance(item, tuple):
                            subdir, files = item
                            for file in files:
                                fullpath = os.path.join(fullpkgpath, subdir, file)
                                remove_path(fullpath)
                elif item_type == 'includes':
                    for item in filespec:
                        if isinstance(item, tuple):
                            if isinstance(item[1], tuple):
                                subdir, saved = item
                                abssubdir = os.path.join(fullpkgpath, subdir)
                                to_remove = sorted(list(set(os.listdir(abssubdir)) - set(saved)))
                                for file in to_remove:
                                    remove_path(os.path.join(abssubdir, file))
                            elif all(isinstance(elem, str) for elem in item):
                                tmpdirpath = os.path.join('tmp')
                                if os.path.exists(tmpdirpath):
                                    shutil.rmtree(tmpdirpath)
                                os.mkdir(tmpdirpath)
                                for file in item:
                                    src = os.path.join(fullpkgpath, file)
                                    dst = os.path.join(tmpdirpath, file)
                                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                                    shutil.copyfile(src, dst)
                                dstdir = os.path.join(fullpkgpath, os.path.split(item[0])[0])
                                shutil.rmtree(dstdir)
                                for dir_or_file in os.listdir(tmpdirpath):
                                    src = os.path.join(tmpdirpath, dir_or_file)
                                    if os.path.isdir(src):
                                        shutil.copytree(src,
                                                        os.path.join(fullpkgpath, dir_or_file))
                                shutil.rmtree(tmpdirpath)

shortcut_table = [
    ('DesktopShortcut',        # Shortcut
     'DesktopFolder',          # Directory_
     'Сравнитель документов',  # Name
     'TARGETDIR',              # Component_
     '[TARGETDIR]diffui.exe',  # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
]

include_files = [('conf/compare-options.conf', 'conf/compare-options.conf')]

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
        'include_files': include_files,
        'packages': ['diffui'],
    },
    'bdist_msi': {
        'data': {'Shortcut': shortcut_table}
    }
}

setup(name='diffui',
      version=VERSION,
      description='Document comparator',
      author='НТЦ Система',
      author_email='www.systema.ru',
      executables=executables,
      options=options,
      cmdclass={'build_exe': diffui_build_exe})
