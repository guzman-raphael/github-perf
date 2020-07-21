# Configuration file for ipython-notebook.
from os import getenv, getuid
from pwd import getpwall
from IPython.lib import passwd


user = [u for u in getpwall() if u.pw_uid == getuid()][0]
c = get_config()

# ------------------------------------------------------------------------------
# NotebookApp configuration
# ------------------------------------------------------------------------------

# NotebookApp will inherit config from: BaseIPythonApplication, Application

# The IPython password to use i.e. "datajoint".
c.NotebookApp.password = passwd(getenv('JUPYTER_PASSWORD', 'datajoint')).encode("ascii")

# Allow root access.
c.NotebookApp.allow_root = True

# The IP to serve on.
c.NotebookApp.ip = u'0.0.0.0'

# The Port to serve on.
c.NotebookApp.port = 8888

c.NotebookApp.notebook_dir = user.pw_dir

c.NotebookApp.terminado_settings = {'shell_command': [user.pw_shell, '-l']}

c.FileContentsManager.root_dir = '/home'

# you may also use a query param ?file-browser-path= to modify tree navigation on left
c.NotebookApp.default_url = ('/lab' if getenv('JUPYTER_DISPLAY_FILEPATH') is None
                             else '/lab/tree{}'.format(
                                getenv('JUPYTER_DISPLAY_FILEPATH').replace(
                                    c.FileContentsManager.root_dir, '')))


def scrub_output_pre_save(model, **kwargs):
    """scrub output before saving notebooks"""
    # only run on notebooks
    if model['type'] != 'notebook':
        return
    # only run on nbformat v4
    if model['content']['nbformat'] != 4:
        return

    model['content']['metadata'].pop('signature', None)
    for cell in model['content']['cells']:
        if cell['cell_type'] != 'code':
            continue
        cell['outputs'] = []
        cell['execution_count'] = None


if getenv('JUPYTER_NOTEBOOK_SAVE_OUTPUT', 'FALSE').upper() == 'FALSE':
    c.FileContentsManager.pre_save_hook = scrub_output_pre_save
