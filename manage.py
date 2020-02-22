import os
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
@click.option('--category', default=10, help='Quantity of categories, default is 10.')
@click.option('--post', default=50, help='Quantity of posts, default is 50.')
@click.option('--comment', default=500, help='Quantity of comments, default is 500.')
def forge(category, post, comment):
    """Generate fake data."""
    from app.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

    db.drop_all()
    db.create_all()

    click.echo('Generating the administrator...')
    fake_admin()

    click.echo('Generating %d categories...' % category)
    fake_categories(category)

    click.echo('Generating %d posts...' % post)
    fake_posts(post)

    click.echo('Generating %d comments...' % comment)
    fake_comments(comment)

    click.echo('Generating links...')
    fake_links()

    click.echo('Done.')

