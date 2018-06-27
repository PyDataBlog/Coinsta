import setuptools

setuptools.setup(
    name="coinsta",
    version="0.0.1",
    url="https://github.com/PyDataBlog/Coinsta",

    author="Bernard Brenyah",
    author_email="bbrenyah@gmail.com",

    description="A Python package for acquiring both historical and current data of cryptocurrencies",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
