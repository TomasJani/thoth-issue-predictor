# Thoth Issue Predictor

The goal of this thesis is to create a predictive model that can, based on data aggregated, spot patterns
causing issues in software stacks and predict which software stacks will likely not work without actually
running the application. An example of an issue can be a specific version of TensorFlow installed together
with a specific version of numpy that cause API incompatibility issues spotted on run time.

## Running Jupyter Notebook on VM
Open all HTTP ports

Then generate jupyter_notebook_config.py file.

`$ jupyter notebook --generate-config`

Config will be saved in `/home/ubuntu/.jupyter/jupyter_notebook_config.py`

By default, jupyter_notebook_config.py would have everything commented. Modify the following entries:

 - Accept incoming request from any host (not only localhost).
   Find **#c.NotebookApp.ip = 'localhost'** and change it to c.NotebookApp.ip = '*'
 - Do not launch a browser.
   Find **#c.NotebookApp.open_browser = True** and change it to c.NotebookApp.open_browser = False
