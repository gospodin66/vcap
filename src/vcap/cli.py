
import click
from vcap import Vcap


CONTEXT_SETTINGS = dict(
    default_map={
        'cap__video': {'path': 'videos'},
        'play__video': {'path': 'videos'}
    }
)

@click.group(context_settings=CONTEXT_SETTINGS)
def cli_cmd():
    pass


@cli_cmd.command()
@click.option(
   '-c',
   '--cap-video',
   type=bool,
   is_flag=True,
   show_default=True,
   default=False,
   help='Mode to initialize cap - capture or play video'
)
@click.argument(
    'path',
    type=str,
    default='./videos'
)
def cap__video(path):
    v = Vcap(path)
    capres = v.cap_video()
    if capres == 0:
        print("\ncap test passed successfully!")


@cli_cmd.command()
@click.option(
   '-p',
   '--play-video',
   type=bool,
   is_flag=True,
   show_default=True,
   default=False,
   help='Mode to initialize cap - capture or play video'
)
@click.argument(
    'path',
    type=str
)
def play__video(path):
    v = Vcap(path)
    playres = v.play_video()
    if playres == 0:
        print("\nplay test passed successfully!")


cli = click.CommandCollection(sources=[cli_cmd])

if __name__ == '__main__':
    cli()
