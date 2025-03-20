from setuptools import setup, find_packages

setup(
    name="ci_cd_challenge",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "Flask-SQLAlchemy"
    ],
    entry_points={
        'console_scripts': [
            'i_cd_challenge = app:app.run',
        ]
    },
)
