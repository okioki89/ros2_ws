from setuptools import find_packages, setup

package_name = "moj_zolw"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    package_data={"": ["py.typed"]},
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Oskar Makowski",
    maintainer_email="oskar.makowski897@gmail.com",
    description="TODO: Package description",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "rysownik = moj_zolw.rysownik:main",
            "do_celu = moj_zolw.do_celu:main",
        ],
    },
)
