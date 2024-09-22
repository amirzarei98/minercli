import click

from constants import VERSION

from cli.debug import DebugCommandGroup

import cli.miner as mining
import cli.twitter_entry as twitter_entry
import cli.drive_entry as drive_entry
import cli.openai_entry as openai_entry
import cli.auth.twitter as twitter_auth
import cli.auth.drive as drive_auth
import cli.auth.vana as vana_auth
import cli.auth.openai as openai_auth

import cli.account.rewards as volara_rewards

import cli.update as volara_update


@click.group(cls=DebugCommandGroup)
@click.version_option(version=VERSION)
@click.pass_context
def volara(ctx):
    """SixGPT CLI tool"""
    ctx.ensure_object(dict)


@volara.group()
def auth():
    """Commands related to authentication"""
    pass


drive_entry.register(auth)
openai_entry.register(auth)

@volara.group(cls=DebugCommandGroup)
def mine():
    """Commands related to mining"""
    pass


@mine.command()
@click.option(
    "--background", "-b", is_flag=True, help="Run the miner in a background process"
)
def start(background: bool):
    """Start the mining process"""
    click.echo("Checking Vana credentials...")
    if vana_auth.get_vana_hotkey() is None:
        click.echo(
            "Vana account is not present. Please install the Vana CLI and create a wallet."
        )
        return
    click.echo("Checking drive credentials...")
    if drive_auth.get_active_account() is None:
        click.echo("No active drive account found. Requesting credentials...")
        drive_auth.set_active_account()
    click.echo("Checking openai credentials...")
    if openai_auth.get_active_account() is None:
        click.echo("No active openai api key found. Requesting credentials...")
        openai_auth.set_active_account()
    click.echo("Starting mining daemon...")
    if background:
        mining.start_daemon()
    else:
        mining.start_inline()


@mine.command()
def stop():
    """Stop the mining process"""
    click.echo("Stopping mining daemon...")
    mining.stop_daemon()


@mine.command()
def logs():
    """Get the logs from the mining process"""
    click.echo("Getting mining logs...")
    mining.echo_logs()


@volara.command()
def update():
    """Update the SixGPT CLI"""
    volara_update.update_cli()



if __name__ == "__main__":
    volara(obj={})
