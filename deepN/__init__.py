import argparse
import os
import re


# notion settings
ID_MAPPER = (r'(\d{4})\/', '\\1|')  # map / to | cause / not valid as file name
NOTION_URL = r'https:\/\/www.notion.so\/[a-z0-9]+'
REFERENCE_STYLE = r'(\[\d[^\]\n]*\])(\([^\)]*\))'
STATE_TAG_STYLE = r'(state:\s)([a-z]+)'
# path settings
NOTE_PATH = 'notes/'
LITERATURE_PATH = 'literature_notes/'
EXPORT_PATH = 'export/'

HELP = (
    'Translator that tranlates notes from notion to notes that can be used '
    'by obsidian')

parser = argparse.ArgumentParser(description=HELP)


def get_notes(path):
    return [x for x in os.listdir(path) if x.endswith('.md')]


def get_note(file):
    with open(file, 'r') as notion_note:
        note = notion_note.read()
        note = clean_note_ids(note)
    return note


def get_title(file):
    note = get_note(file)
    lines = note.split('\n')
    # adjust title
    title = lines[0].replace('#', '').strip()
    return title


def clean_note_ids(note):
    # I used slash in notion to create unique sequential note ids. But
    # slash can't be used as file names and therefore as markdown
    # obsidian note names.
    return re.sub(ID_MAPPER[0], ID_MAPPER[1], note)


def map_links_to_connections(note, files):
    # map notion links to obsidian connections
    links = re.findall(NOTION_URL, note)
    link_mapper = {}
    for link in links:
        notion_id = link.split('/')[-1]
        # we only need the first five characters to find the respective
        # note
        notion_id = notion_id[:5]
        conn_file = [x for x in files if notion_id in x]
        if len(conn_file) > 1:
            raise ValueError(
                "More than one connection note found with id "
                f"{notion_id}: {', '.join(conn_file)}")
        elif len(conn_file) < 1:
            raise ValueError(
                f"No connection note found with id {notion_id}"
                f"in note:\n\n{'-'*5}\n\n{note}\n\n{'-'*5}\n")
        conn_file = conn_file[0]
        conn_title = get_title(conn_file)
        conn_title = clean_note_ids(conn_title)
        link_mapper[link] = conn_title
    for link, conn_title in link_mapper.items():
        note = note.replace(link, '[[' + conn_title + ']]')
    return note


def map_references_to_connections(note):
    references = re.findall(REFERENCE_STYLE, note)
    notion_references = [x[0] + x[1] for x in references]
    reference_titles = [x[0] for x in references]
    obsidian_connections = ['[' + x + ']' for x in reference_titles]
    mapper = dict(zip(notion_references, obsidian_connections))
    print('\n\n'.join([x + ' --> ' + y for x, y in mapper.items()]))
    for notion, obsidian in mapper.items():
        note = note.replace(notion, obsidian)
    return note


def map_state_tag(note):
    match = re.findall(r'(state:\s)([a-z]+)', note)
    if len(match) > 1:
        raise ValueError(
            f"Too many tags found in note:\n\n{'-'*5}\n\n{note}\n\n{'-'*5}\n")
    elif len(match) == 0:
        raise ValueError(
            f"No tags found in note:\n\n{'-'*5}\n\n{note}\n\n{'-'*5}\n")
    match = match[0]
    note = note.replace(match[0] + match[1], match[0] + '#' + match[1])
    return note


def export_note(title, note, path):
    os.makedirs(path, exist_ok=True)
    with open(path + title + '.md', 'w') as f:
        f.write(note)


def translate_notion_to_obsidian_note(note_file, all_files, export_path,
                                      map_conn=True, map_ref=True,
                                      map_tags=True):
    # adjust note title
    title = get_title(note_file)

    # adjust note - notion links and notion references to obsidian
    # connections
    note = get_note(note_file)
    if map_conn:
        note = map_links_to_connections(note, all_files)
    if map_ref:
        note = map_references_to_connections(note)
    if map_tags:
        note = map_state_tag(note)

    # save obsidian note
    export_note(title, note, export_path)


def main():
    parser.parse_args()
    # create export folder
    os.makedirs(EXPORT_PATH, exist_ok=True)

    # get notion file names
    note_files = get_notes(NOTE_PATH)
    literature_files = get_notes(LITERATURE_PATH)
    all_files = [NOTE_PATH + x for x in note_files] + [
            LITERATURE_PATH + x for x in literature_files]

    # translate notion notes to obsidian notes
    for nfile in note_files:
        translate_notion_to_obsidian_note(
            NOTE_PATH + nfile, all_files, EXPORT_PATH + 'notes/')

    for lfile in literature_files:
        translate_notion_to_obsidian_note(
            LITERATURE_PATH + lfile, all_files,
            EXPORT_PATH + 'literature_notes/', map_conn=False)
