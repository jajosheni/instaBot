from setuptools import setup

setup(
    name='instaBot',
    version='2.2.1',
    description='Unofficial instabot, developed on python, learn more about the features inside the readme file',
    url='https://github.com/jajosheni/instaBot',
    author='Sheni Hamitaj',
    author_email='shen.i@live.com',
    license='MPL',
    packages=['InstagramAPI'],
    zip_safe=False,
    install_requires=[
        "requests==2.20.0",
        "requests-toolbelt==0.7.0"
    ])
