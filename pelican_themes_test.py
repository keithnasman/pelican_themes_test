#!/usr/bin/python3

"""
pelican_themes_test.py - a tool to winnow down the themes

Use git to download all the pelican themes from git hub
https://github.com/getpelican/pelican-themes

Put this script in your pelican folder and when you run it,
it will cycle through all the themes by adding a theme into the
pelicanconf.py file and regenerate your content, leaving you 
to just reload the web browser. Then it will ask you to keep it 
or not. If not, then that theme will be removed from the themes 
folder. Run repeatedly to get down to the theme you want.
"""
import os
import fileinput

THEME_DIR = "pelican-themes"
WEB_ROOT = "/var/www/html/"

def update_conf(new_theme):
    """ Updates the pelicanconf.py with the new theme
        If there isn't a THEME line, it adds one.
    """
    found = False
    # Open conf file
    for line in fileinput.input("pelicanconf.py", inplace=True):
        line = line.rstrip()
        # Test for a THEME line
        if "THEME" in line:
            # Replace line
            found = True
            print("THEME = \"", os.getcwd(), "/", THEME_DIR, "/", new_theme,"\"", sep='')
        else:
            print(line)
        if not found:
            # Add line
            theme_line = "THEME = \"" + os.getcwd() + "/" + THEME_DIR + "/" + new_theme + "\""
            append_line = "echo '" + theme_line + "' >> pelicanconf.py"
            os.system(append_line)

def rebuild_content():
    """ Rebuild content and copy over to web root directory """

    print("Rebuilding the pelican content.\n")
    # Run the pelican command
    rebuild = "pelican content"
    os.system(rebuild)

def refresh_website():
    """ Refresh the website file by copying the output files into web root """

    print("\nSynchronizing the content to web root.\n")
    # Use rsync to update the files in web root
    sync = "sudo rsync -avc output/ " + WEB_ROOT + " >> /dev/null"
    os.system(sync)
    print()

# Read in all the theme folders in pelican-themes
themes = os.listdir(THEME_DIR)

for theme in themes:
    theme = themes.pop()
    if os.path.isdir(THEME_DIR + "/" + theme) and theme[0] != '.':
        print("Loading %s theme for your review.\n" % theme)

        update_conf(theme)
        rebuild_content()
        refresh_website()

        keep = input("Would you like to keep this theme(y/n/q)? ")
        if keep == 'n':
            # delete theme
            delete = "rm -rf " + THEME_DIR + "/" + theme
            print("Removing theme %s" % theme)
            os.system(delete)
        elif keep == 'q':
            break
    print("-------------------------------------------------------")
