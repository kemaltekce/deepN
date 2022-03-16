# deepN

> deepN is a note translator and the name was inspired by the awesome language translator deepL. But this note translator doesn't use artificial intelligence just simple regex.

### Note translator from Notion to Obsidian

Note-taking is a great way to store, understand, connect, and learn new concepts. There are several tools out there that one can use to take notes like Notion or Obsidian. Every one of them has its advantages and disadvantages - things you like about them and dislike about them.

You might even consider moving from one tool to another. Like I did with. I moved from taking notes on Notion to taking notes on Obsidian.

Instead of leaving notes behind, this script helps transform your Notion notes into Obsidian notes.

Specifically, Notion stores links and tags in a different way in their markdown files than Obsidian does. So this script translates the Notion links and tags into links and tags that can be used by Obsidian.

For example links like:

```
[note id: name of note](note%20id%20ab1cd.md)

https://www.notion.so/123456789abcdefghijklmnopqrstuvwx
```

will be translated into Obsidian links:

```
[[note id: name of note]]

[[another note id: another name of note]]
```

## My note structure

Taking notes is a very personalized activity. Everyone takes notes differently. Everyone includes different information. Everyone links note differently together.

The notes I took and for which the script was designed looks like this after exporting them as Markdown from Notion:

```
# note id: note title

ID: note id
connection from: https://www.notion.so/12345abcde
created datetime: February 17, 2021 4:02 PM
random ID: 249906635
ref. literature note: https://www.notion.so/6789fghi
state: shaped

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua ([another note id: another note title](another%20not%205ghf1.md)).

At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
```

Depending on your note structure the script might work for you as well, it might not, or parts of it might work. You might have to adjust a few settings to make it work. Of course, ideally it might work out of the box.

## Hacking

1. Install `Python >= 3.6.3`.
1. Export your Notion notes - notes as well as literature notes - as markdown files onto your machine.
1. Create two folders - `notes` and `literature_notes` - and save the respective notes (markdown files) from Notion in them.
1. Run the translation via `python -m deepN` and translate the notion notes into obsidian notes.
1. The obisidan notes will be exported into the `export` folder which will be created automatically.
