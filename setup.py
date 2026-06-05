from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="xianyvagent",
    version="1.0.0",
    author="55184",
    description="闲鱼AI智能客服 - 多专家路由自动回复系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/55184/xianyvAgent",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.65.5",
        "websockets>=12.0",
        "loguru>=0.7.0",
        "python-dotenv>=1.0.0",
        "requests>=2.32.0",
        "flask>=3.0.0",
        "httpx>=0.27.0",
    ],
)
