# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
import datetime
from .. import readers
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_trial(conn, trial, source_id):
    """Write trial to database.

    Args:
        conn (dict): connection dict
        trial (dict): normilized trial data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        (str, bool)/(None, None): trial id and is primary flag/if not written (skipped)

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Get facts/read object
    facts = list(trial['identifiers'].values())
    if 'scientific_title' in trial:
        facts.append(trial['scientific_title'])
    facts = helpers.slugify_array(facts)
    object = readers.read_objects(conn, 'trials', single=True, facts=facts)

    # Create object
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['facts'] = []
        create = True

    # Decide primary
    is_primary = False
    priority = ['nct', 'euctr', 'isrctn']
    for register in priority:
        if 'source_id' not in object:
            is_primary = True
            break
        elif object['source_id'] == source_id:
            is_primary = True
            break
        elif source_id == register:
            is_primary = True
            break
        elif object['source_id'] == register:
            is_primary = False
            break

    # Update meta
    object.update({
        'updated_at': timestamp,
        'facts': helpers.slugify_array(object['facts'] + facts),
    })

    # Update data only if it's primary
    if is_primary:

        # Update object
        object.update({
            'source_id': source_id,
            # ---
            'primary_register': trial['primary_register'],
            'primary_id': trial['primary_id'],
            'identifiers': trial['identifiers'],
            'registration_date': trial.get('registration_date', None),
            'public_title': trial['public_title'],
            'brief_summary': trial.get('brief_summary', None),
            'scientific_title': trial.get('scientific_title', None),
            'description': trial.get('description', None),
            'recruitment_status': trial.get('recruitment_status', None),
            'eligibility_criteria': trial.get('eligibility_criteria', None),
            'target_sample_size': trial.get('target_sample_size', None),
            'first_enrollment_date': trial.get('first_enrollment_date', None),
            'study_type': trial.get('study_type', None),
            'study_design': trial.get('study_design', None),
            'study_phase': trial.get('study_phase', None),
            'primary_outcomes': trial.get('primary_outcomes', None),
            'secondary_outcomes': trial.get('primary_outcomes', None),
            'gender': trial.get('gender', None),
            'has_published_results': trial.get('has_published_results', None),
        })

    # Write object
    conn['database']['trials'].upsert(object, ['id'], ensure=False)

    # Log debug
    logger.debug('Trial - %s: %s',
        'created' if create else 'updated', trial['primary_id'])

    return object['id'], is_primary
