from cx_Freeze import setup, Executable

base = None


executables = [Executable("main.py", base=base)]

packages = ["pygments"]
options = {
    'build_exe': {

        'packages':packages,
        
    },

}

setup(
    name = "Main",
    options = options,
    version = "1.0",
    description = 'main file',
    executables = executables
)
