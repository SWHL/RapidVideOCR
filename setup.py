# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import subprocess
from pathlib import Path
from typing import Optional

import setuptools


def get_latest_version(package_name: str) -> Optional[str]:
    output: str = subprocess.run(["pip", "index", "versions", package_name],
                                 capture_output=True).stdout.decode('utf-8')
    if output:
        name_versions = list(filter(lambda x: len(x) > 0, output.split('\n')))
        # e.g. opencv-python (4.7.0.68) → 68
        pack_name_version = name_versions[0].strip()
        latest_version = pack_name_version.split(' ')[-1][1:-1]
        return latest_version
    return None


def version_add_one(version: Optional[str], add_loc: int = -1) -> str:
    if not version:
        return '1.0.0'

    version_list = version.split('.')
    mini_version = str(int(version_list[add_loc]) + 1)
    version_list[add_loc] = mini_version
    new_version = '.'.join(version_list)
    return new_version


def get_readme() -> str:
    root_dir = Path(__file__).resolve().parent
    readme_path = str(root_dir / 'docs' / 'doc_whl.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


MODULE_NAME = 'rapid_videocr'
latest_version = get_latest_version(MODULE_NAME)
VERSION_NUM = version_add_one(latest_version)
VERSION_NUM = '1.1.0'

setuptools.setup(
    name=MODULE_NAME,
    version=VERSION_NUM,
    platforms="Any",
    description="RapidVideOCR",
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author="SWHL",
    author_email="liekkaskono@163.com",
    url="https://github.com/SWHL/RapidVideOCR.git",
    license='Apache-2.0',
    include_package_data=True,
    install_requires=["tqdm>=4.52.0", "rapidocr_onnxruntime"],
    packages=[MODULE_NAME],
    package_data={'': ['*.yaml']},
    keywords=['rapidocr,videocr,subtitle'],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [f'{MODULE_NAME}={MODULE_NAME}.{MODULE_NAME}:main'],
    }
)
