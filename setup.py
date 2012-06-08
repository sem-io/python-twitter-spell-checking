from setuptools import setup, find_packages

setup(
    name = "twitter-spell-checking",
    version = "0.1",
    packages = find_packages(),
    include_package_data = True,

    author = "Thomas Grange",
    author_email = "thomas@sem.io",
    description = "Spell checking with a database of words from twitter accounts",
    license = "Apache",
    keywords = "twitter license licenser open-source",
    url = "http://github.com/sem-io/python-twitter-spell-checking",
    install_requires = [
        'python-twitter',
        'ujson'
    ],

    # Setting up executable/main functions links
    entry_points = {
        'console_scripts': [
            'twitter_spelling = twitter_spelling.cli:main',
        ]
    },

    classifiers = [
        'Development Status :: 0.1 - Early Alpha',
        'Environment :: Unix-like Systems',
        'Intended Audience :: Developers, Project managers, Sys admins',
        'Programming Language :: Python',
        'Operating System :: Unix-like',
    ],
)
