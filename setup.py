from setuptools import setup, find_packages

setup(
    name='birthday_planner',
    description='The Ultimate Birthday Planner!',
    version='0.1.0',
    author='Minions Co.',
    author_email='dev@minions.co',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'birthday-planner=personal_assistant.main:main',
        ],
    },
    install_requires=[
        'python-dateutil',
    ],
    python_requires='>=3.10',
)
