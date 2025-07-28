from setuptools import setup, find_packages

setup(
    name="imagewatermark",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "imagewatermark = imagewatermark.app:main"
        ],
    },
    data_files=[
        ('share/applications', ['imagewatermark.desktop']),
        ('share/icons/hicolor/128x128/apps', ['assets/icon.png']),
    ]
)
