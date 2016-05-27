# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'hra',
        'name': 'Health Research Authority'
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'hra_internal_identifier': record['application_id'],
        'iras_project_identifier': record['iras_proj_id'],
        'study_type_id': record['study_type_id']
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['application_title'],
        record['application_full_title'],
        record['application_id']
        )

    trial = {
        'primary_register': 'Health Research Authority',
        'primary_id': record['application_id'],
        'identifiers': identifiers,
        'registration_date': record['publication_date'],
        'public_title': public_title,
        'brief_summary': record['research_summary'],
        'scientific_title': record['application_full_title'],
        'study_type': record['study_type']
    }
    return trial


def extract_conditions(record):
    conditions = []
    return conditions


def extract_interventions(record):
    interventions = []
    return interventions


def extract_locations(record):
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    organisations.append({'name': record['sponsor_org']})
    if record['study_type'] == '8' or '20':
        organisations.extend([
            {'name': record['establishment_org']},
            {'name': record['establishment_org_address_1']},
            {'name': record['establishment_org_address_2']},
            {'name': record['establishment_org_address_3']},
            {'name': record['establishment_org_post_code']}
            ])
    return organisations


def extract_persons(record):
    persons = []
    persons.append({
        'name': record['contact_name'],
        'trial_id': record['application_id']
    })
    return persons
