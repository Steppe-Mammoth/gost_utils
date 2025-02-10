# rm -rf dist/ build/ *.egg-info
# python setup.py sdist bdist_wheel

# pip uninstall gost_utils
# pip install .

# twine upload dist/*


from setuptools import setup, find_packages



setup(
    name="gost_utils",
    version="0.1.4",                 # Версія
    description="Many utils",  # Короткий опис
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Steppe_Mammoth",              # Ваше ім'я
    author_email="qwqwqww505@yahoo.com",  # Ваш email
    url="",  # Посилання на репозиторій
    packages=find_packages(include=["utils", "utils.*"]),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',         # Мінімальна версія Python
)
