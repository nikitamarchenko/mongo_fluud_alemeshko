import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements


install_requires_pip = parse_requirements('requirements.txt',
                                          session=uuid.uuid1())

install_requires_setuptools = []

for ir in install_requires_pip:
    install_requires_setuptools.append(str(ir.req))

setup(
    name='mongo_fluud_alemeshko',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='',
    author='nmarchenko',
    author_email='',
    description='',
    setup_requires=[
        'setuptools_git >= 0.3'
    ],
    entry_points={
        'console_scripts': [
            'mongo-fluud = mongo_fluud_alemeshko:start_fluud',
        ]
    },
    install_requires=install_requires_setuptools,
    include_package_data=True
)
