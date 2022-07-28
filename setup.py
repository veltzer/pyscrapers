import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pyscrapers",
    version="0.0.65",
    packages=[
        'pyscrapers',
        'pyscrapers.core',
        'pyscrapers.workers',
    ],
    # from here all is optional
    description="project to produce various useful scrapers",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
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
    url="https://veltzer.github.io/pyscrapers",
    download_url="https://github.com/veltzer/pyscrapers",
    license="MIT",
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
        'pyeventroute',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={"console_scripts": [
        'pyscrapers=pyscrapers.main:main',
    ]},
)
