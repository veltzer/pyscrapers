import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pyscrapers',
    version='0.0.18',
    packages=[
        'pyscrapers',
        'pyscrapers.core',
        'pyscrapers.endpoints',
        'pyscrapers.workers',
    ],
    # from here all is optional
    description='A collection of scrapers for the web',
    long_description='project to produce various useful scrapers',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'scrape',
        'images',
        'social',
        'facebook',
        'instagram',
        'vk.com',
        'download',
        'pics',
    ],
    url='https://veltzer.github.io/pyscrapers',
    download_url='https://github.com/veltzer/pyscrapers',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'lxml',
        'requests',
        'browser-cookie3',
        'pytconf',
        'pylogconf',
        'pornhub-api',
        'youtube-dl',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    data_files=[
    ],
    entry_points={'console_scripts': [
        'pyscrapers=pyscrapers.endpoints.main:main',
    ]},
    python_requires='>=3.5',
)
