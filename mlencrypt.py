import click
import subprocess


@click.group()
def cli():
    pass


@cli.command()
@click.argument('destination')
def send(destination):
    click.echo(f'send to {destination}')
    subprocess.run(["python", "communications/send_data.py"])


@cli.command()
def receive():
    click.echo('receive')
    subprocess.run(["twistd", "-y", "communications/receive.tac"])


if __name__ == '__main__':
    cli()
