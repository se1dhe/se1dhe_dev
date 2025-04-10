from setuptools import setup, find_packages

setup(
    name="se1dhe-dev",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "sqlalchemy==2.0.27",
        "pydantic==2.6.1",
        "python-jose==3.3.0",
        "passlib==1.7.4",
        "python-multipart==0.0.6",
        "redis==5.0.1",
        "python-dotenv==1.0.1",
    ],
) 