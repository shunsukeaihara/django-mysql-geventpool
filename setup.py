from setuptools import setup, find_packages

setup(
    name='django-mysql-geventpool-27',
    version='0.3.3',
    install_requires=['django', 'gevent', 'mysqlclient', 'pymysql'],
    description='Add a MySQL connection pool for django using gevent',
    long_description=open("README.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0',
    lassifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    author='lollo789',
    author_email='laurent@labatut.net'
)
