# KSP Localization Synchronizer

Polished mulitpurpose script to manage KSP localizations for mods.

## Uses

* Load a main .cfg (default en-us.cfg)
* Format the main .cfg file
* Synchronize and format other .cfg files
* Create a new .cfg file

## Usage

* IMPORTANT: Format comments as said in formatting to get desired results
* Run the locsync.py in the directory of the .cfg files
* Follow instructions. (y/n) means yes/no, (Y/n) means yes/no, but defaulting to yes if answer is empty

### Formatting

While the script does the formatting, comments need to be in a rather flexible format

#### Headings

Headings start with a number asterisks (*)

* Heading: 8 - will be padded on the top and bottom
* Subheading: 4 - will be padded only on the top
* Microheading: 2 - will be padded only on the top

You only need to type the amount of asterists on the left of the content, the format script will reformat it automatically. Any asterisks right of the comment itself will be ignored. Behaviour of not having any content inside a heading is undefined.

#### Planet names

For your convinience planet names have a separate heading, with 20 dashes on each side. It is enough to type 2 dashes on the left of your content to autocomplete the entire planet comment after reformatting.

#### Line commments

Comments that do not fall under headings will be "glued" to the line beneath them, which could be a definition, comment, or heading. They will be copied over to the other localization files.

Line comments that are in in language files that are not in the main file will be preserved during synchronization, so translators can leave language-specific comments

## Customization

The BASE constant can be used to change the base language file if you want to do that for some reason.
