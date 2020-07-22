import click
from datetime import date, datetime
from . import NSEHistory

import requests
from urllib3.exceptions import InsecureRequestWarning


@click.group()
def cli():
    pass

@cli.command()
@click.argument("symbol")
@click.option('--from', '-f', 'from_', help="yyyy-mm-dd", required=True)
@click.option('--to', '-t', help="yyyy-mm-dd", required=True)
@click.option("--output", default="", help='output file name')
@click.option('--host', '-h', default="", help='host url eg. http://www1.nseindia.com')
@click.option('--warnings/--no-warnings', default=True, help='suppress SSL warnings')
def stock(symbol, from_ ,to, output, host, warnings):
    """Download historical stock data between dates, refer help for usage-
    
    $ jdata stock --help
    """
    from_date = datetime.strptime(from_, "%Y-%m-%d").date()
    to_date = datetime.strptime(to, "%Y-%m-%d").date()
    n = NSEHistory()
    # host = "https://23.54.86.108"

    if host:
        n.base_url = host
        n.ssl_verify = False
    
    n.use_threads = False
    if not warnings:
        # Suppress only the single warning from urllib3 needed.
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    df = n.stock_history(symbol, from_date, to_date)
    click.echo(df.head())

@cli.command()
@click.argument("symbol")
@click.option('--from', '-f', 'from_', help="yyyy-mm-dd", required=True)
@click.option('--to', '-t', help="yyyy-mm-dd", required=True)
@click.option('--instru', '-i', help="Instrument type - FUTIDX, OPTIDX, FUTSTK, OPTSTK", required=True)
@click.option('--expiry', '-e', help="yyyy-mm-dd", required=True)
@click.option("--output", default="", help='output file name')
@click.option('--host', '-h', default="", help='host url eg. http://www1.nseindia.com')
@click.option('--warnings/--no-warnings', default=True, help='suppress SSL warnings')
def fno(symbol, from_, to, output, host, warnings):
    pass

if __name__=="__main__":
    cli()

