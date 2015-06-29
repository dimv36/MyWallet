import os
import sys
import subprocess
import shlex

CWD = os.path.dirname(os.path.abspath(__file__))

for fname in os.listdir(CWD):
    if not fname.endswith('.ui'):
        continue

    print('compiling', fname)

    full_name = os.path.join(CWD, fname)

    cmd = '"%s" -m PyQt5.uic.pyuic -d "%s" -o "%s"' % (
        sys.executable, full_name,
        os.path.join(
            os.path.dirname(full_name),
            'ui_'+fname.replace('.py', '').replace('.ui', '')+'.py'
        )
    )
    cmd = str(cmd)
    subprocess.Popen(shlex.split(cmd)).wait()


"""
#!/bin/bash

uic=$(which pyuic5)

for file in *.ui; do
  echo "compiling ${file}"
  ${uic} "${file}" > ui_${file%%.*}.py
done
"""