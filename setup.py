#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import Extension, setup, find_packages

# from Cython.Build import cythonize

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

install_requirements = [
    'Cython',
    'numpy',
#    'Click>=6.0',
]

setup_requirements = [
    'setuptools>=18.0',
    'Cython',
    'wheel',
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'asv',
]

XML_FORMAT_FILES = [
    'src/TotalDepth/util/plot/formats/Azimuthal_Density_3Track.xml',
    'src/TotalDepth/util/plot/formats/Azimuthal_Density_Image.xml',
    'src/TotalDepth/util/plot/formats/Azimuthal_Resistivity_3Track.xml',
    'src/TotalDepth/util/plot/formats/Blank_3Track_Depth.xml',
    'src/TotalDepth/util/plot/formats/Blank_3Track_Time.xml',
    'src/TotalDepth/util/plot/formats/Formation_Micro_Image_Aligned.xml',
    'src/TotalDepth/util/plot/formats/Formation_Micro_Image_Processed.xml',
    'src/TotalDepth/util/plot/formats/Formation_Test_Time.xml',
    'src/TotalDepth/util/plot/formats/HDT.xml',
    'src/TotalDepth/util/plot/formats/Micro_Resistivity_3Track.xml',
    'src/TotalDepth/util/plot/formats/Natural_GR_Spectrometry_3Track.xml',
    'src/TotalDepth/util/plot/formats/OilBaseMicroImager_Equalized.xml',
    'src/TotalDepth/util/plot/formats/Porosity_GR_3Track.xml',
    'src/TotalDepth/util/plot/formats/Pulsed_Neutron_3Track.xml',
    'src/TotalDepth/util/plot/formats/Pulsed_Neutron_Time.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_3Track_Correlation.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_3Track_Logrithmic.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_Porosity_GR_3Track.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_Radial_Investigation_Image.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_at_the_Bit.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_at_the_bit_deep_image.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_at_the_bit_medium_image.xml',
    'src/TotalDepth/util/plot/formats/Resistivity_at_the_bit_shallow_image.xml',
    'src/TotalDepth/util/plot/formats/Sonic_3Track.xml',
    'src/TotalDepth/util/plot/formats/Sonic_LowerDipole_VDL.xml',
    'src/TotalDepth/util/plot/formats/Sonic_P_S_VDL.xml',
    'src/TotalDepth/util/plot/formats/Sonic_Stonely_VDL.xml',
    'src/TotalDepth/util/plot/formats/Sonic_UpperDipole_VDL.xml',
    'src/TotalDepth/util/plot/formats/Sonic_Waveform4_Depth.xml',
]

XML_FORMAT_FILES = [os.path.join(*p.split('/')) for p in XML_FORMAT_FILES]

# ext_modules = cythonize(
#     module_list="src/TotalDepth/LIS/core/*.pyx",
# )

ext_modules = [
    Extension(
        "TotalDepth.LIS.core.cRepCode",
        sources=[
            "src/TotalDepth/LIS/core/cRepCode.pyx",
        ]
    ),
    Extension(
        "TotalDepth.LIS.core.cFrameSet",
        sources=[
            "src/TotalDepth/LIS/core/cFrameSet.pyx",
        ]
    ),
]

ext_modules.extend(
    [
        Extension(
            "TotalDepth.LIS.core.cpRepCode",
            sources=[
                "src/TotalDepth/LIS/core/cpLISRepCode.cpp",
                "src/TotalDepth/LIS/core/LISRepCode.cpp",
            ],
        ),
    ]
)

print('TRACE:', ext_modules)

setup(
    name='TotalDepth',
    version='0.2.2rc0',
    description="TotalDepth is a software collection that can process petrophysical data such as wireline logs and seismic data.",
    long_description=readme + '\n\n' + history,
    author="Paul Ross",
    author_email='apaulross@gmail.com',
    url='https://github.com/paulross/TotalDepth',
    packages=find_packages('src'),
    package_dir={'' : 'src'},
    # package_data={'' : ['TotalDepth/util/plot/formats/*.xml']},
    data_files= [
        (os.path.join('TotalDepth', 'util', 'plot', 'formats'), XML_FORMAT_FILES),
    ],
    entry_points={
        # All TotalDepth scripts have a 'td' prefix.
        # Experimental scripts have a 'tdX' prefix.
        'console_scripts': [
            'tdplotlogs=TotalDepth.PlotLogs:main',
            'tdlisdetif=TotalDepth.LIS.DeTif:main',
            'tdlisdumpframeset=TotalDepth.LIS.DumpFrameSet:main',
            'tdlisindex=TotalDepth.LIS.Index:main',
            'tdlistohtml=TotalDepth.LIS.LisToHtml:main',
            'tdlisplotlogpasses=TotalDepth.LIS.PlotLogPasses:main',
            'tdXlisrandomframesetread=TotalDepth.LIS.RandomFrameSetRead:main',
            'tdlisscanlogidata=TotalDepth.LIS.ScanLogiData:main',
            'tdlisscanlogirecord=TotalDepth.LIS.ScanLogiRec:main',
            'tdlisscanphysrec=TotalDepth.LIS.ScanPhysRec:main',
            'tdlistablehistogram=TotalDepth.LIS.TableHistogram:main',
            'tdlasreadlasfiles=TotalDepth.LAS.ReadLASFiles:main',
            'tdarchive=TotalDepth.util.archive:main',
            'tdrp66v1scanfiles=TotalDepth.RP66V1.ScanFile:main',
#            'TotalDepth=TotalDepth.cli:main'
        ]
    },
    include_package_data=True,
    license="GPLv2",
    zip_safe=False,
    keywords='TotalDepth',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    setup_requires=setup_requirements,
    install_requires=install_requirements,
    tests_require=test_requirements,
    # cmdclass = {'build_ext': build_ext},
    ext_modules=ext_modules
)
