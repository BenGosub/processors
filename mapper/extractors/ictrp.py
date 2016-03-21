# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class IctrpExtractor(base.Extractor):

    # Public

    basis = 'warehouse'
    table = 'data_ictrp'

    def extract_source(self, item):

        source = {
            'name': 'ictrp',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        trial = {
            'primary_register': 'ictrp',
            'primary_id': item['main_id'],
            'secondary_ids': {},
            'registration_date': None,  # TODO: text on scrap layer
            'public_title': item['pucli_title'],
            'brief_summary': '',  # TODO: review
            'scientific_title': item['scientific_title'],  # TODO: review
            'description': None,  # TODO: review
            'recruitment_status': item['recruitment_status'],
            'eligibility_criteria': {'criteria': item['key_inclusion_exclusion_criteria']},
            'target_sample_size': item['target_sample_size'],
            'first_enrollment_date': None,  # TODO: text on scraper layer
            'study_type': item['study_type'],
            'study_design': item['study_design'],
            'study_phase': item['study_phase'],
            'primary_outcomes': item['primary_outcomes'],
            'secondary_outcomes': item['secondary_outcomes'],
        }

        return trial

    def extract_record(self, item):

        record = {
            'type': 'trial',
            'data': {
                # TODO: item seriliazation issue
            },
        }

        return record

    def extract_problems(self, item):

        problems = []

        for element in item['health_conditions_or_problems_studied'] or []:

            problems.append({
                'name': element,
            })

        return problems

    def extract_interventions(self, item):

        interventions = []

        for element in item['interventions'] or []:

            # TODO: parse "drug: name"
            interventions.append({
                'name': element,
            })

        return interventions

    def extract_locations(self, item):

        locations = []

        for element in item['countries_of_recruitment'] or []:

            locations.append({
                'name': element,
                'type': 'country',
                'role': 'recruitment_countries',
            })

        return locations

    def extract_organisations(self, item):

        # TODO: check on scraper level
        organisations = []

        return organisations

    def extract_persons(self, item):

        # TODO: check on scraper level
        persons = []

        return persons
