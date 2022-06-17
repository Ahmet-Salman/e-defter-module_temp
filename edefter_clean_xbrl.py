from typing import Dict, List

from xbrl import XBRLParser

# (tag, name)
ACCOUNTING_ENTRIES_ATTRS = (
    ('gl-cor', 'uniqueId'),
    ('gl-cor', 'creationDate'),
    ('gl-cor', 'periodCoveredStart'),
    ('gl-cor', 'periodCoveredEnd'),
    ('gl-bus', 'fiscalYearStart'),
    ('gl-bus', 'fiscalYearEnd'),
)

ENTRY_HEADER_ATTRS = (
    ('gl-cor', 'enteredBy'),
    ('gl-cor', 'enteredDate'),
    ('gl-cor', 'entryNumber'),
    ('gl-cor', 'entryComment'),
    ('gl-bus', 'totalDebit'),
    ('gl-bus', 'totalCredit'),
    ('gl-cor', 'entryNumberCounter'),
)

ENTRY_DETAIL_ATTRS = (
    ('gl-cor', 'lineNumber'),
    ('gl-cor', 'lineNumberCounter'),
    ('gl-cor', 'accountMainID'),
    ('gl-cor', 'accountMainDescription'),
    ('gl-cor', 'accountSubDescription'),
    ('gl-cor', 'accountSubID'),
    ('gl-cor', 'amount'),
    ('gl-cor', 'debitCreditCode'),
    ('gl-cor', 'postingDate'),
)


def find_child(element, name: str):
    """Returns the first tag with the given name in element
    """

    return element.find(name.lower())


def find_all_children(element, name: str):
    """Returns all children tags with the given name in element
    """

    return element.find_all(name.lower())


def find_child_text(element, name: str) -> str:
    """Returns the text (content) of the first tag with the given name in element
    """

    child = find_child(element, name)
    return child.text if child else None


def clean_xbrl(file_path) -> List[Dict[str, str]]:
    """Reads an XBRL file from the given path and extracts specific data from it according
    to the E-Defter specification.\n
    Returns a list of dicts, each dict representing a single row/entry.
    """

    root = XBRLParser().parse(file_path)

    # Traverse the XBRL file until we reach our desired data
    edefter = find_child(root, 'edefter:defter')
    accountingEntries = find_child(edefter, 'gl-cor:accountingEntries')

    # Dynamically look for and add all child elements we want from this element
    accountingEntriesAttrs = dict()
    for tag, name in ACCOUNTING_ENTRIES_ATTRS:
        accountingEntriesAttrs[name] = find_child_text(accountingEntries, f'{tag}:{name}')

    entries = []
    for entryHeader in find_all_children(accountingEntries, 'gl-cor:entryHeader'):
        # Create a new dictionary for this entry header, and initialize it using the accounting entry elements
        # This way, each entry in the final list will have these values (to be used in a column) even though
        # they are constant across all elements
        entryHeaderAttrs = dict(accountingEntriesAttrs)
        for tag, name in ENTRY_HEADER_ATTRS:
            entryHeaderAttrs[name] = find_child_text(entryHeader, f'{tag}:{name}')

        for entryDetail in find_all_children(entryHeader, 'gl-cor:entryDetail'):
            # This is the smallest unit, a single record/row in the database
            cleanedEntry = dict(entryHeaderAttrs)
            for tag, name in ENTRY_DETAIL_ATTRS:
                cleanedEntry[name] = find_child_text(entryDetail, f'{tag}:{name}')

            entries.append(cleanedEntry)

    return entries
  
