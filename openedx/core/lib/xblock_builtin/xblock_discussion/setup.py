"""
Setup for discussion-forum XBlock.
"""

import os
from setuptools import setup


def package_data(pkg, root_list):
    """
    Generic function to find package_data for `pkg` under `root`.
    """
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-discussion',
    version='0.2',
    description='XBlock - Discussion',
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'ui_block.v1': [
            'discussion_board = xblock_discussion:DiscussionBoardBlock'
        ],
        'xblock.v1': [
            'discussion = xblock_discussion:DiscussionXBlock'
        ],
    },
    package_data=package_data("xblock_discussion", ["static"]),
)
