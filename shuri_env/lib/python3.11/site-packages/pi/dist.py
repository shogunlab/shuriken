import distutils.core

def read_script(script_name):
    return distutils.core.run_setup(script_name, stop_after='config')
