"""
@package mi.dataset.driver.moas.gl.flord.driver
@file marine-integrations/mi/dataset/driver/moas/gl/flord/driver.py
@author Stuart Pearce & Chris Wingard
@brief Driver for the glider FLORD
Release notes:

initial release
"""

__author__ = 'Stuart Pearce & Chris Wingard'
__license__ = 'Apache 2.0'

from mi.core.log import get_logger
log = get_logger()

from mi.dataset.dataset_driver import SimpleDataSetDriver
from mi.dataset.parser.glider import GliderParser
from mi.dataset.parser.glider import GgldrFlordDelayedDataParticle
from mi.dataset.harvester import AdditiveSequentialFileHarvester


class FLORDDataSetDriver(SimpleDataSetDriver):
    @classmethod
    def stream_config(cls):
        return [GgldrFlordDelayedDataParticle.type()]

    def _build_parser(self, parser_state, infile):
        config = self._parser_config
        config.update({
            'particle_module': 'mi.dataset.parser.glider',
            'particle_class': 'GgldrFlordDelayedDataParticle'
        })
        log.debug("MYCONFIG: %s", config)
        self._parser = GliderParser(
            config,
            parser_state,
            infile,
            self._save_parser_state,
            self._data_callback
        )

        return self._parser

    def _build_harvester(self, harvester_state):
        self._harvester = AdditiveSequentialFileHarvester(
            self._harvester_config,
            harvester_state,
            self._new_file_callback,
            self._exception_callback
        )

        return self._harvester

