import click

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info('Starting')

@click.command()
@click.option('--config', default='config.yml', help='Path to the configuration file.')
def start(config):
    print(config)