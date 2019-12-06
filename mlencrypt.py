import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('destination')
def send(destination):
    click.echo(f'send to {destination}')


@cli.command()
def receive():
    click.echo('receive')


if __name__ == '__main__':
    cli()
