from setuptools import setup


setup(
  name='Flask-Captain',
  description="Handle webhooks with Flask",
  version='0.1.0',
  author='Mark Steve Samson',
  author_email='hello@marksteve.com',
  url='https://github.com/marksteve/flask-captain',
  license='MIT',
  py_modules=['flask_captain'],
  install_requires=[
    'Flask',
  ],
)
