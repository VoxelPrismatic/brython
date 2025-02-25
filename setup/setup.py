# Always prefer setuptools over distutils
from setuptools import setup, find_packages

import os
import shutil
import sys

with open('README.rst', encoding='utf-8') as fobj:
    LONG_DESCRIPTION = fobj.read()

# source of index.html
html = """<!doctype html>
<html>

<head>
<meta charset="utf-8">
<script type="text/javascript" src="brython.js"></script>
<script type="text/javascript" src="brython_stdlib.js"></script>
</head>

<body onload="brython(1)">
<script type="text/python">
from browser import document

document <= "Hello"
</script>
</body>

</html>"""


command = sys.argv[1]

if command == "sdist":
    # before creating the distribution, copy files from other locations in
    # the repository
    print("copying files...")
    this_dir = os.getcwd()
    root_dir = os.path.dirname(this_dir)
    src_dir = os.path.join(root_dir, "www", "src")
    data_dir = os.path.join(this_dir, "data")

    # copy files from /www/src
    for fname in ["brython_stdlib.js", "unicode.txt"]:
        shutil.copyfile(os.path.join(src_dir, fname),
            os.path.join(data_dir, fname))
    shutil.copyfile(os.path.join(src_dir, "brython_no_static.js"),
        os.path.join(data_dir, "brython.js"))

    # copy python_minifier and make_package in current directory
    for fname in ["python_minifier.py", "make_package.py"]:
        shutil.copyfile(os.path.join(root_dir, "scripts", fname),
            fname)

    # copy index.html
    with open(os.path.join(data_dir, "index.html"), "w", encoding="utf-8") as out:
        out.write(html)

    # copy demo.html
    with open(os.path.join(root_dir, 'www', 'demo.html'), encoding="utf-8") as f:
        demo = f.read()
    start_tag = "<!-- start copy -->"
    end_tag = "<!-- end copy -->"
    start = demo.find(start_tag)
    if start == -1:
        raise Exception("No tag <!-- start copy --> in demo.html")
    end = demo.find(end_tag)
    if end == -1:
        raise Exception("No tag <!-- end copy --> in demo.html")
    body = demo[start + len(start_tag) : end].strip()

    with open(os.path.join(data_dir, "demo.tmpl"), encoding="utf-8") as f:
        template = f.read()

    demo = template.replace("{{body}}", body)

    with open(os.path.join(data_dir, "demo.html"), "w", encoding="utf-8") as out:
        out.write(demo)


setup(
    name='brython',

    version='3.8.0',
    description='Brython is an implementation of Python 3 running in the browser',

    long_description=LONG_DESCRIPTION,

    # The project's main homepage.
    url='http://brython.info',

    # Author details
    author='Pierre Quentel',
    author_email='quentel.pierre@orange.fr',

    packages = ['data', 'data.tools'],

    # Choose your license
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',

        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='Python browser',

    py_modules=["brython", "list_modules", "make_package", "python_minifier"],

    package_data={
        'data': [
            'README.txt',
            'demo.html',
            'index.html',
            'brython.js',
            'brython_stdlib.js',
            'unicode.txt'
            ]
    }

)