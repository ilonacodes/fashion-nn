from fabric.api import local, env, run, settings, cd

env.user = 'root'
env.hosts = ['139.59.208.165']

code_dir = '/srv/fashion-nn'
git_repo = 'https://github.com/ilonacodes/fashion-nn'

def check_code_dir():
    return run('test -d %s' % code_dir)

def git_clone():
    return run('git clone %s %s' % (git_repo, code_dir))

def update_code():
    with cd(code_dir):
        run('git stash')
        run('git pull')

def deploy_code():
    with settings(warn_only=True):
        if check_code_dir().failed:
            git_clone()

    update_code()

def update_apt():
    run('apt-get update -qqyy')

def install_package(name):
    run('apt-get install -qqyy %s' % name)

def install_supervisor():
    install_package('supervisor')

def install_python_3_6():
    run('add-apt-repository -y ppa:jonathonf/python-3.6')
    update_apt()
    install_package('python3.6 python3.6-dev python3.6-venv')
    run('ln -sf /usr/bin/python3.6 /usr/local/bin/python3')

def install_pip_for_python_3_6():
    run('wget https://bootstrap.pypa.io/get-pip.py')
    run('python3.6 get-pip.py')
    run('ln -sf /usr/local/bin/pip /usr/local/bin/pip3')

def create_virtualenv():
    with cd(code_dir):
        run('python3 -m venv ./virtualenv3')

def update_dependencies():
    with cd(code_dir):
        run('./scripts/update-dependencies.sh')

def prepare():
    update_apt()
    install_supervisor()
    install_python_3_6()
    install_pip_for_python_3_6()
    deploy_code()
    create_virtualenv()
    update_dependencies()
    # setup_supervisor_config()
