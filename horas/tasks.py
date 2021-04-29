from invoke import Collection, task

ns = Collection()


@task
def clean(c):
    """Clean files"""
    patterns = ["**/*.pyc", "build", "dist"]
    for pattern in patterns:
        c.run(f"rm -rf {pattern}")
    c.run("find -path '**/migrations/*.py' -not -name '__init__.py' -delete")


@task
def test(c):
    """Execute tests"""
    c.run("python manage.py makemigrations")
    c.run("python manage.py test --verbosity 2")


@task(name="format")
def format_code(c):
    """Format code"""
    c.run(
        "python -m black --config ./pyproject.toml --exclude migrations -- horas"
    )


@task()
def styles(c):
    """Lint code styles"""
    c.run(
        """
        pylint \
            --load-plugins pylint_django \
            --django-settings-module=horas.settings \
            -- horas
        """
    )


@task
def types(c):
    """Lint code types"""
    c.run("python -m mypy -- horas")


ns.add_task(clean)
ns.add_task(test)
ns.add_task(format_code)

lint = Collection("lint")
lint.add_task(styles, name="styles")
lint.add_task(types, name="types")

ns.add_collection(lint)
