import os

from setuptools import setup


def read(path):
    try:
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), path)) as f:
            return f.read()
    except Exception:  # noqa
        return ''


if __name__ == '__main__':
    setup(
        name='tornado_jsonrpc',
        description='jsonrpc implementation for tornado',
        license='Apache',
        url='https://github.com/Pavel-Egorov/tornado_jsonrpc',
        version='1.0.5',
        author='Pavel Egorov',
        author_email='paveg.sp@gmail.com',
        maintainer='Pavel Egorov',
        maintainer_email='paveg.sp@gmail.com',
        keywords=['tornado', 'jsonrpc', 'rpc', 'handler'],
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        py_modules=['tornado_jsonrpc'],
        zip_safe=False,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        install_requires=['tornado>=4.0'],
    )
