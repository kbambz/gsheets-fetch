from setuptools import setup, find_packages


setup(
    name='gsheets_fetch',
    description='Download sheets from Google Sheets as CSV, plain text, or JSON files.',
    version='0.0.4',
    url='https://github.com/kbambz/gsheets-fetch',
    author='Kathryn Bambino',
    author_email='katie.bambino@gmail.com',
    copyright='Copyright 2019 Kathryn Bambino',
    packages=find_packages(),
    py_modules=['gsheets_fetch'],
    include_package_data=True,
    install_requires=[
        'google-api-python-client==2.37.0',
        'google-auth-httplib2==0.1.0',
        'google-auth-oauthlib==0.4.6',
        'requests==2.27.1',
    ],
    entry_points='''
        [console_scripts]
        gsheets-fetch=gsheets_fetch.scripts.fetch:cli
    ''',
)
