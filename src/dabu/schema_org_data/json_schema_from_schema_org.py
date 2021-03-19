"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import sys

from .add_word import add_word
from .add_property import add_property, combine
from .set_property import set_property


def json_schema_from_schema_org(schemaorg_data, vocabulary, draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19

    This function generates a json schema from https://schema.org , which
    desribes the vocabulary.

    :param schemaorg_data: json-ld data from https://schema.org as returned
                           from :func:`get_schema_org_data`.
    :param vocabulary: list of words, which are a 
                       Schema.org Type (Schema.org vocabulary)
    :param draft: the used json schema, could be:

                  * 'draft-04'
                  * 'draft-06'
                  * 'draft-07'
                  * '2019-09'
    :return: json schema describing a json-ld for the given vocabulary
    """
    missing_words = set()
    for word in vocabulary:
        missing_words.add(word)
    schema = dict()
    schema_declaration = {
        'draft-04': "http://json-schema.org/draft-04/schema#",
        'draft-06': "http://json-schema.org/draft-06/schema#",
        'draft-07': "http://json-schema.org/draft-07/schema#",
        '2019-09': "http://json-schema.org/draft/2019-09/schema#"}
    if draft in schema_declaration:
        schema["$schema"] = schema_declaration[draft]
    else:
        raise NotImplementedError('do not understand json draft version')
    add_property(schema,
                 "title",
                 "json schema to define json-ld based on schema.org")
    add_property(schema,
                 "description",
                 "The vocabulary %s " % ', '.join(vocabulary) +
                 "from schema.org is defined as a json schema. "
                 "It should be a valid json-ld file. "
                 "All necessary words should be defined.")
    update_description = False
    found_vocabulary = []
    while len(missing_words) > 0:
        word = missing_words.pop()
        sys.stderr.write(f'searching: {word}\n')
        new_missing_words, word_schema = add_word(
            schemaorg_data, word, draft=draft)
        if word_schema is None:
            del vocabulary[vocabulary.index(word)]
            update_description = True
        else:
            found_vocabulary.append(word)
            combine(schema, word_schema)
            if len(new_missing_words) > 0:
                for t in new_missing_words:
                    if t not in schema["definitions"]:
                        missing_words.add(t)
        sys.stderr.write(f'finished: {word}\n')
        # return schema  # workaround for debugging
    if update_description:
        set_property(schema,
                     "description",
                     "The vocabulary %s " % ', '.join(vocabulary) +
                     "from schema.org is defined as a json schema. "
                     "It should be a valid json-ld file. "
                     "All necessary words should be defined.")
    if len(found_vocabulary) == 0:
        sys.stderr.write('nothing found\n')
        schema = dict()
    return schema
