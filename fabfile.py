from fabric.api import local, env, run, settings, cd

env.user = 'root'
env.hosts = ['139.59.208.165']

code_dir = '/srv/fashion-nn'
git_repo = 'https://github.com/ilonacodes/fashion-nn'

# deployment

def check_code_dir():
    return run('test -d %s' % code_dir)

def git_clone():
    return run('git clone %s %s' % (git_repo, code_dir))

def update_code():
    with cd(code_dir):
        run('git stash')
        run('git pull')

def unzip_model():
    with cd(code_dir):
        run('unzip -o my_model_trained_x8.h5.zip')

def deploy_code():
    with settings(warn_only=True):
        if check_code_dir().failed:
            git_clone()

    update_code()
    unzip_model()

def update_dependencies():
    with cd(code_dir):
        run('./scripts/update-dependencies.sh')

def restart():
    run('supervisorctl restart fashion-nn-d')

def deploy():
    deploy_code()
    update_dependencies()
    restart()

# prepare server

def update_apt():
    run('apt-get update -qqyy')

def install_package(name):
    run('apt-get install -qqyy %s' % name)

def install_nginx():
    install_package('nginx')

def install_supervisor():
    install_package('supervisor')

def install_python_3_6():
    run('add-apt-repository -y ppa:jonathonf/python-3.6')
    update_apt()
    install_package('python3.6 python3.6-dev python3.6-venv')
    run('ln -sf /usr/bin/python3.6 /usr/local/bin/python3')

def install_unzip():
    install_package('unzip')

def create_virtualenv():
    with cd(code_dir):
        run('python3 -m venv ./virtualenv3')

def reread_supervisor_config():
    run('supervisorctl reread')
    run('supervisorctl update')

def setup_supervisor_config():
    run('ln -sf %s/conf/fashion-nn-d.conf /etc/supervisor/conf.d/fashion-nn-d.conf' % code_dir)
    reread_supervisor_config()

def remove_default_nginx_site():
    run('rm /etc/nginx/sites-enabled/default || true')

def setup_nginx_config():
    remove_default_nginx_site()
    run('ln -s %s/conf/nginx.conf /etc/nginx/sites-enabled/fashion-nn.conf' % code_dir)
    run('nginx -s reload')

def prepare():
    update_apt()
    install_nginx()
    install_supervisor()
    install_python_3_6()
    install_unzip()
    deploy_code()
    create_virtualenv()
    update_dependencies()
    setup_supervisor_config()
    restart()
    setup_nginx_config()

# Adding some swap :(

def add_swap():
    run('mkdir -v /var/cache/swap')
    with cd('/var/cache/swap'):
        run('dd if=/dev/zero of=swapfile bs=1K count=2M')
        run('chmod 600 swapfile')
        run('mkswap swapfile')
        run('swapon swapfile')

def setup_swap_for_reboot():
    run('echo "/var/cache/swap/swapfile none swap sw 0 0" | tee -a /etc/fstab')

def setup_swap():
    add_swap()
    setup_swap_for_reboot()
