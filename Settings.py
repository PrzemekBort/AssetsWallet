import os
import pathlib

# Path to project directory
rootPath = pathlib.Path(os.path.abspath(''))

# Subpath to database directory
dataBaseDirectoryPath = rootPath.joinpath('Database')

# Subpath to directory with icons
iconsPath = rootPath.joinpath('GUI', 'Resources', 'Icons')
