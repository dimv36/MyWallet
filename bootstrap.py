#!/usr/bin/python3
import os
import sys
import platform
import argparse
import subprocess
import pathlib


def exit_with_error(error):
    sys.stderr.write(error + '\n')
    sys.exit(1)


def exec_cmd(*args):
    try:
        args = [str(arg) for arg in args]
        process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL,
                                   universal_newlines=True)
        out, unused = process.communicate()
        return (process.returncode == 0, out.rstrip())
    except subprocess.CalledProcessError as e:
        return (False, str(e))


def _get_pyside2_root():
    try:
        import PySide2 as p
        return pathlib.Path(p.__file__).parent
    except ImportError:
        exit_with_error('PySide2 package does not installed')


def genui():
    UI_REPLACES = [
        ('tablewidget', 'mywallet.widgets.tablewidget'),
        ('resource_rc', 'mywallet.resources.resource_rc')
    ]

    uic_bin, rcc_bin = None, None
    if platform.system() == 'Linux':
        uic_found, uic_bin = exec_cmd('which', 'pyside2-uic',)
        rcc_found, rcc_bin = exec_cmd('which', 'pyside2-rcc')
    elif platform.system() == 'Windows':
        # uic and rcc installed at PythonHome/Scripts
        python_bin_dir = pathlib.Path(sys.executable).parent
        uic_bin = python_bin_dir / 'Scripts' / 'pyside2-uic.exe'
        rcc_bin = python_bin_dir / 'Scripts' / 'pyside2-rcc.exe'
        uic_found, rcc_found = uic_bin.exists(), rcc_bin.exists()
    if not (uic_found and rcc_found):
        exit_with_error('Could not find pyside2-uic or pyside2-rcc')
    else:
        print('Using pyside2-uic at {} ...'.format(uic_bin))
        print('Using pyside2-rcc at {} ...'.format(rcc_bin))
    for filename in pathlib.Path('mywallet').glob('**/*.ui'):
        pyuic = filename.parent / 'ui_{}.py'.format(filename.stem)
        print('Generate form for {} ...'.format(filename))
        ret, out = exec_cmd(uic_bin, filename)
        for replace in UI_REPLACES:
            out = out.replace(*replace)
        with open(pyuic, mode='w') as fp:
            fp.write(out + '\n')
    for filename in pathlib.Path('mywallet').glob('**/*.qrc'):
        pyrcc = filename.parent / '{}_rc.py'.format(filename.stem)
        print('Generate resouce for {} ...'.format(filename))
        ret, out = exec_cmd(rcc_bin, filename)
        with open(pyrcc, mode='w') as fp:
            fp.write(out + '\n')


def localize():
    lupdate_bin = None
    if platform.system() == 'Linux':
        lupdate_found, lupdate_bin = exec_cmd('which', 'pyside2-lupdate')
    elif platform.system() == 'Windows':
        # as above, lupdate installed at PythonHome/Scripts
        python_bin_dir = pathlib.Path(sys.executable).parent
        lupdate_bin = python_bin_dir / 'Scripts' / 'pyside2-lupdate.exe'
        lupdate_found = lupdate_bin.exists()
    if not lupdate_found:
        exit_with_error('Could not found pyside2-lupdate')
    else:
        print('Using pyside2-lupdate at {} ...'.format(lupdate_bin))
    tmp_lupdate_pro = 'mywallet.pro'
    py_sources = [str(pyfile) for pyfile in pathlib.Path('mywallet').glob('**/*.py')]
    with open(tmp_lupdate_pro, mode='w') as fp:
        fp.write('TRANSLATIONS = mywallet/translations/mywallet_ru.ts\n')
        fp.write('SOURCES = {}\n'.format(' '.join(py_sources)))
    print('Update localizations ...')
    ret, out = exec_cmd(lupdate_bin, '-noobsolete', tmp_lupdate_pro)
    if not ret:
        exit_with_error('localization update error')
    os.remove(tmp_lupdate_pro)


def localization_compile(lrelease='lrelease-qt5'):
    lrelease_bin = None
    if platform.system() == 'Linux':
        lrelease_found, lrelease_bin = exec_cmd('which', lrelease)
    elif platform.system() == 'Windows':
        # lrelease can be found at PySide2 dir
        lrelease_bin = _get_pyside2_root() / 'lrelease.exe'
        lrelease_found = lrelease_bin.exists()
    if not lrelease_found:
        exit_with_error('Could not fild lrelease')
    else:
        print('Using lrelease at {} ...'.format(lrelease_bin))
    print('Compile localizations ...')
    for filename in pathlib.Path('mywallet').glob('**/*.ts'):
        print('Compile translation {} ...'.format(filename))
        ret, out = exec_cmd(lrelease_bin, filename)
        if not ret:
            print('Error: translation {} compilation failed'.format(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    genui_parser = subparsers.add_parser('genui', help='Regenerate forms and resources')
    localize_update_parser = subparsers.add_parser('locale-update', help='Update localization')

    localize_compile_parser = subparsers.add_parser('locale-compile', help='Compile localization')
    localize_compile_parser.add_argument('--lrelease-bin', default='lrelease-qt5', required=False,
                                         help='lrelease binary name, default=lrelease-qt5')

    args = parser.parse_args()
    if args.command == 'genui':
        genui()
    elif args.command == 'locale-update':
        localize()
    elif args.command == 'locale-compile':
        localization_compile(args.lrelease_bin)
    else:
        parser.print_help()
