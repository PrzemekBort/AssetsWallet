import os
import pathlib

# Path to project directory
rootPath = pathlib.Path(os.getcwd())

# Subpath to database
dataBasePath = rootPath.joinpath('Database', 'AssetsDataBase.db')
