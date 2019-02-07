from setuptools import setup, find_packages


setup(
    name='gsheets_fetch',
    description='Download sheets from Google Sheets as CSV, plain text, or JSON files.',
    version='0.0.1',
    url='https://github.com/kbambz/gsheets-fetch',
    author='Kathryn Bambino',
    author_email='katie.bambino@gmail.com',
    copyright='Copyright 2019 Kathryn Bambino',
    packages=find_packages(),
    py_modules=['gsheets_fetch'],
    include_package_data=True,
    install_requires=[
        'google-api-python-client==1.7.8',
        'google-auth-httplib2==0.0.3',
        'google-auth-oauthlib==0.2.0',
    ],
    entry_points='''
        [console_scripts]
        gsheets-fetch=gsheets_fetch.scripts.fetch:cli
    ''',
)
