# -*- coding: utf-8 -*-

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import yaml
from collections import OrderedDict

import logging
from pylons import config
log = logging.getLogger(__name__)



class DdiHarvest(plugins.SingletonPlugin):
    """
    Plugin containing the harvester for ddi for
    the World Bank
    """


class DdiSchema(plugins.SingletonPlugin, tk.DefaultDatasetForm):
    """
    Plugin containing the extended schema for ddi for the World Bank
    """

    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm, inherit=False)

    def update_config(self, config):
        pass

    def get_helpers(self):
        return {}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        # Add new fields as extras
        # Identification fields
        schema.update({
            'abbreviation': [tk.get_validator('ignore_missing'),
                             tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'studyType': [tk.get_validator('ignore_missing'),
                          tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'seriesInformation': [tk.get_validator('ignore_missing'),
                                  tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'idNumber': [tk.get_validator('ignore_missing'),
                         tk.get_converter('convert_to_extras')]
        })

        # Version fields
        schema.update({
            'productionDate': [tk.get_validator('ignore_missing'),
                               tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'description': [tk.get_validator('ignore_missing'),
                      tk.get_converter('convert_to_extras')]
        })

        # Overview fields
        schema.update({
            'abstract': [tk.get_validator('ignore_missing'),
                         tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'kindOfData': [tk.get_validator('ignore_missing'),
                           tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'unitOfAnalysis': [tk.get_validator('ignore_missing'),
                               tk.get_converter('convert_to_extras')]
        })

        # Scope fields
        schema.update({
            'descriptionOfScope': [tk.get_validator('ignore_missing'),
                                   tk.get_converter('convert_to_extras')]
        })

        # Coverage fields
        schema.update({
            'country': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'geographicCoverage': [tk.get_validator('ignore_missing'),
                                   tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'universe': [tk.get_validator('ignore_missing'),
                         tk.get_converter('convert_to_extras')]
        })

        # Producers and Sponsors fields
        schema.update({
            'primaryInvestigator': [tk.get_validator('ignore_missing'),
                                    tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'otherProducers': [tk.get_validator('ignore_missing'),
                               tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'funding': [tk.get_validator('ignore_missing'),
                        tk.get_converter('convert_to_extras')]
        })

        # Sampling fields
        schema.update({
            'samplingProcedure': [tk.get_validator('ignore_missing'),
                                  tk.get_converter('convert_to_extras')]
        })

        # Data Collection fields
        schema.update({
            'datesOfDataCollection': [tk.get_validator('ignore_missing'),
                                      tk.get_converter('convert_to_extras')]
        })

        # Data Appraisal fields
        schema.update({
            'accessAuthority': [tk.get_validator('ignore_missing'),
                                tk.get_converter('convert_to_extras')]
        })

        schema.update({
            'citationRequirement': [tk.get_validator('ignore_missing'),
                                    tk.get_converter('convert_to_extras')]
        })

        # Contacts fields
        schema.update({
            'contactPersons': [tk.get_validator('ignore_missing'),
                               tk.get_converter('convert_to_extras')]
        })

        return schema

    def create_package_schema(self):
        schema = super(DdiSchema, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(DdiSchema, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(DdiSchema, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        # Add new fields to the dataset schema.
        # Identification fields
        schema.update({
            'studyType': [tk.get_converter('convert_from_extras'),
                          tk.get_validator('ignore_missing')]
        })

        schema.update({
            'seriesInformation': [tk.get_converter('convert_from_extras'),
                                  tk.get_validator('ignore_missing')]
        })

        schema.update({
            'idNumber': [tk.get_converter('convert_from_extras'),
                         tk.get_validator('ignore_missing')]
        })

        # Version fields

        schema.update({
            'productionDate': [tk.get_converter('convert_from_extras'),
                               tk.get_validator('ignore_missing')]
        })

        schema.update({
            'description': [tk.get_converter('convert_from_extras'),
                      tk.get_validator('ignore_missing')]
        })

        # Overview fields
        schema.update({
            'abstract': [tk.get_converter('convert_from_extras'),
                         tk.get_validator('ignore_missing')]
        })

        schema.update({
            'kindOfData': [tk.get_converter('convert_from_extras'),
                           tk.get_validator('ignore_missing')]
        })

        schema.update({
            'unitOfAnalysis': [tk.get_converter('convert_from_extras'),
                               tk.get_validator('ignore_missing')]
        })

        # Scope fields

        schema.update({
            'descriptionOfScope': [tk.get_converter('convert_from_extras'),
                                   tk.get_validator('ignore_missing')]
        })

        # Coverage fields
        schema.update({
            'country': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')]
        })

        schema.update({
            'geographicCoverage': [tk.get_converter('convert_from_extras'),
                                   tk.get_validator('ignore_missing')]
        })

        schema.update({
            'universe': [tk.get_converter('convert_from_extras'),
                         tk.get_validator('ignore_missing')]
        })

        # Producers and Sponsors fields
        schema.update({
            'primaryInvestigator': [tk.get_converter('convert_from_extras'),
                                    tk.get_validator('ignore_missing')]
        })

        schema.update({
            'otherProducers': [tk.get_converter('convert_from_extras'),
                               tk.get_validator('ignore_missing')]
        })

        schema.update({
            'funding': [tk.get_converter('convert_from_extras'),
                        tk.get_validator('ignore_missing')]
        })

        # Sampling fields
        schema.update({
            'samplingProcedure': [tk.get_converter('convert_from_extras'),
                                  tk.get_validator('ignore_missing')]
        })

        # Data Collection fields
        schema.update({
            'datesOfDataCollection': [tk.get_converter('convert_from_extras'),
                                      tk.get_validator('ignore_missing')]
        })
        # Data Appraisal fields
        schema.update({
            'accessAuthority': [tk.get_converter('convert_from_extras'),
                                tk.get_validator('ignore_missing')]
        })

        schema.update({
            'citationRequirement': [tk.get_converter('convert_from_extras'),
                                    tk.get_validator('ignore_missing')]
        })

        # Contacts fields
        schema.update({
            'contactPersons': [tk.get_converter('convert_from_extras'),
                               tk.get_validator('ignore_missing')]
        })

        return schema


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def get_ddi_config():
    with open(config.get('ckanext.ddi.config_file')) as config_file: 
        ddi_config = ordered_load(config_file)
    return ddi_config


class DdiTheme(plugins.SingletonPlugin, tk.DefaultDatasetForm):
    """
    Plugin containing the theme for ddi for
    the World Bank
    """

    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)

    ddi_config = None

    def update_config(self, config):
        self.ddi_config = yaml.load(config.get('ckanext.ddi.config_file'))
        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'public')
        log.debug("update config")

    def get_helpers(self):
        log.debug("get_helpers")
        return {'ddi_theme_get_ddi_config': get_ddi_config }

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return False

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def setup_template_variables(self, context, data_dict):
        context['ddi_config'] = self.ddi_config 
        return super(DdiTheme, self).setup_template_variables(
            context, data_dict
        )
