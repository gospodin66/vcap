import click

from .cap import cap

CONTEXT_SETTINGS = dict(
    default_map={
        '--cap-video': {'path': 'videos'},
        '--play-video': {'path': 'videos'}
    }
)
context_settings=CONTEXT_SETTINGS
@click.group()
def cli_cmd():
    pass


@cli_cmd.command()
@click.option(
   '--cap-video','-c',
   type=bool,
   is_flag=True,
   show_default=True,
   default=False,
   help='Mode to initialize cap - capture or play video'
)
@click.argument(
    'path',
    type=str,
    required=False
)
def cap_video(cap_video, path):
    v = cap.Vcap(path)
    capres = v.cap_video()
    if capres == 0:
        print("\ncap test passed successfully!")


@cli_cmd.command()
@click.option(
   '--play-video','-p',
   type=bool,
   is_flag=True,
   show_default=True,
   default=False,
   help='Mode to initialize cap - capture or play video'
)
@click.argument(
    'path',
    type=str,
    required=False
)
def play_video(play_video, path):
    v = cap.Vcap(path)
    playres = v.play_video()
    if playres == 0:
        print("\nplay test passed successfully!")



cli = click.CommandCollection(sources=[cli_cmd])

if __name__ == '__main__':
    cli()
