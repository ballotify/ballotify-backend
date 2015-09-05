from fabric.api import env, run, cd, settings, prefix, task, sudo


@task
def beta():
    env.stage = "beta"
    env.hosts = ['144.76.3.131', ]
    env.user = 'rambo'
    env.project_dir = '/home/rambo/projects/beta/ballotify'


@task
def prod():
    pass


@task(alias="pull")
def git_pull():
    with cd(env.project_dir):
        run('git pull origin master')


@task(alias="pip")
def pip_install():
    with settings(cd(env.project_dir), prefix('workon ballotify')):
        run('pip install -r reqs/%s.txt' % env.stage)


@task(alias="run")
def run_command(command):
    with settings(cd(env.project_dir), prefix('workon ballotify')):
        run('python manage.py %s --settings="ballotify.settings.%s"' % (command, env.stage))


@task
def migrate():
    run_command("migrate")


@task(alias="static")
def collectstatic():
    run_command("collectstatic --noinput")


@task(alias="restart")
def restart_supervisor():
    with settings(cd(env.project_dir), prefix('workon ballotify')):
        sudo("supervisorctl restart ballotify-beta")


@task
def deploy():
    # backend
    git_pull()
    pip_install()
    migrate()
    collectstatic()
    # # server
    restart_supervisor()
