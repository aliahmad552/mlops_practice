from setuptools import file_packeges, setup

def get_requirements(filepath):
    with open(filepath) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements

project_name = 'mlops_practice'
setup(
    name = project_name,
    author = 'Ali Ahmad',
    author_email = 'aliahmaddawana@gmail.com',
    packages = find_packages(where = 'src')
    package_dir = {"":"src"}
    description = "A machine learning project for house price prediction which is integrated all mlops concepts"
    install_requires = get_requirements('requirements.txt')
)