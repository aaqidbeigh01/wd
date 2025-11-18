from setuptools import find_packages,setup
from typing import List
hypen='-e .'
def get_req(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    require=[]
    with open(file_path) as file_obj:
        require=file_obj.readlines()
        require=[req.replace('\n','')for req in require]
        if hypen in require:
            require.remove(hypen)
    return require
setup(
    name='Project',
    version='0.0.1',
    author='AAQID',
    author_email='aaqidget@gmail.com0,',
    packages=find_packages(),
    install_require=get_req('requirements.txt')
)