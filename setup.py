from setuptools import setup

APP = ['test.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'Bufibu Cloud',
        'CFBundleDisplayName': 'Bufibu Printer Cloud Services',
        'CFBundleGetInfoString': "Bufibu Printer Cloud Services",
        'CFBundleIdentifier': 'com.bufibu.cloud',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSBackgroundOnly': '1',
    },
    'packages': ['escpos', 'tkinter'],
    'includes': ['requests'],
    'excludes': ['tkinter'],  # Exclude tkinter if not used
    'resources': ['credentials.txt'],  # Include additional resource files
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)
