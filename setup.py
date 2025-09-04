from setuptools import setup, find_packages

setup(
    name='pybugmate',
    version='0.1.2',
    description='Effortless debugging, error hints, profiling, and postmortem REPL for Python',
    author='ANU SONI',
    author_email='anusoni25.2006@gmail.com',
    packages=find_packages(),
    install_requires=['IPython'],  
    python_requires='>=3.6',
    include_package_data=True,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ANU-2524/pybugmate',
)
