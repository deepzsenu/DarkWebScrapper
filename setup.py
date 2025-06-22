from setuptools import setup, find_packages

setup(
    name='DarkWebScrapper',
    version='1.0.0',
    description='Scrape and download .mp4, .jpg, and .png files from .onion sites over Tor',
    author='deepzsenu',
    author_email='deepzsenu@gmail.com',
    url='https://github.com/deepzsenu/DarkWebScrapper',
    packages=find_packages(),
    py_modules=['dark_scraper'],
    install_requires=[
        'requests[socks]',
        'beautifulsoup4',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'dark-scraper=dark_scraper:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Environment :: Console'
    ],
    python_requires='>=3.7',
)
