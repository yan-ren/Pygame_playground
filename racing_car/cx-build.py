import cx_Freeze

executables = [cx_Freeze.Executable("racing.py")]

cx_Freeze.setup(
    name="Racing Car",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["img/", "audio/", "fonts/", "modules/"]}},
    executables = executables
)
