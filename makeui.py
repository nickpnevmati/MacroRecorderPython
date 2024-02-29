import os
import subprocess

dir = 'ui'
dest = 'src/frontend/ui'
for file in os.listdir(dir):
    f = os.path.join(dir, file)
    
    if not os.path.isfile(f):
        continue
    
    destFile = 'ui' + file.strip('.ui').lower()
    
    result = subprocess.run(['bash', '-c', f'pyuic5 -o {os.path.join(dest, destFile)}.py {f}'], capture_output=True, text=True)

    # Access the standard output
    stdout = result.stdout

    # Access the standard error
    stderr = result.stderr

    # Access the return code
    return_code = result.returncode