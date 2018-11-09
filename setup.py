from setuptools import setup

setup(
    name='instaBot',
    version='1.1',
    description='Unofficial instagram bot: stats, unfollowers, autolike, autofollow, autofeedliker, developing on python',
    url='https://github.com/jajosheni/instaBot',
    author='Sheni Hamitaj',
    author_email='shen.i@live.com',
    license='MPL',
    packages=['InstagramAPI'],
    zip_safe=False,
    install_requires=[
        "requests==2.11.1",
        "requests-toolbelt==0.7.0"
    ])
