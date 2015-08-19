from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/alexvicegrab/tangoTimeMachine.git"

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    virtualenv_folder = source_folder + '/../virtualenv'
    
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder, virtualenv_folder)
    _update_static_files(source_folder, virtualenv_folder)
    _update_database(source_folder, virtualenv_folder)
    _set_up_nginx_gunicorn(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/djangoProject/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/djangoProject/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder, virtualenv_folder):
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % 
        (virtualenv_folder, source_folder)
    )

def _update_static_files(source_folder, virtualenv_folder):
    run('cd %s && %s/bin/python3 manage.py collectstatic --noinput' % 
        (source_folder, virtualenv_folder)
    )

def _update_database(source_folder, virtualenv_folder):
    run('cd %s &&  %s/bin/python3 manage.py migrate --noinput' % 
        (source_folder, virtualenv_folder)
    )

def _set_up_nginx_gunicorn(source_folder):
    if not exists('/etc/nginx/sites-available/%s' % env.host):
        # Convert Nginx template into workable server config file
        run(('cd %s && sed "s/SITENAME/%s/g; s/USERNAME/%s/g" ' +
        'deploy_tools/nginx.template.conf | sudo tee ' +
        '/etc/nginx/sites-available/%s') %
            (source_folder, env.host, env.user, env.host)
        )
    
    if not exists('/etc/nginx/sites-enabled/%s' % env.host):
        # Activate config file by making a symbolic link
        run(('sudo ln -s /etc/nginx/sites-available/%s ' + 
        '/etc/nginx/sites-enabled/%s') %
            (env.host, env.host)
        )
    
    if not exists('/etc/init/gunicorn_%s.conf' % env.host):
        # Write upstart script:
        run(('cd %s && sed "s/SITENAME/%s/g; s/USERNAME/%s/g" ' +
        'deploy_tools/gunicorn-upstart.template.conf | sudo tee ' +
        '/etc/init/gunicorn_%s.conf') %
            (source_folder, env.host, env.user, env.host)
        )
    
    # Start services:
    run('sudo service nginx reload')
    run('sudo restart gunicorn_%s' % env.host)
