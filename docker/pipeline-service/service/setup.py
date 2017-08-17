from setuptools import setup

setup(
    name='pipelineservice',
    packages=['pipelineservice'],
    include_package_data=False,
    install_requires=[
        'flask', 'gomatic', "hvac"
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
