from setuptools import setup, find_packages

setup(
    name='Moving_Average_MG',
    version='1.0.0',
    url='https://github.com/raudez77/Stock-Analysis',
    author='Marvin G.',
    author_email='raudez77@hotmail.com',
    description='Calcualte different moving average',
    packages=find_packages(),    
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1' , 'pandas >= 0.25.1' ],
)
