from setuptools import setup, find_packages

setup(
    name="py-amo-client",        # Имя вашего пакета
    version="0.1.4",
    author="cheboxarov",
    author_email="lalakasuper2@gmail.com",
    description="Api client for amoCRM",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cheboxarov/py_amo.git",
    packages=find_packages(),
    install_requires=[
    ],
    python_requires=">=3.9",
)
