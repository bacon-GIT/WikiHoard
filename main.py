# Made by Josh Bacon
# github.com/bacon-GIT

# TODO
# -Move to argparse
# -Convert Language selection to Json
# -better compresion

import wikipediaapi
import re
import os
from zipfile import ZipFile
import pathlib

def main():

    # Accumulates extra pages
    list = {}
    pages = []

    # Wikipedia Hoarder is available in the following languages
    languages = [
        'en',
        'ceb',
        'sv',
        'fr',
        'de',
        'es',
        'ja',
        'ru',
        'nl',
        'sq']

    banner = '''
 _    _ _ _    _   _   _                     _           
| |  | (_) |  (_) | | | |                   | |          
| |  | |_| | ___  | |_| | ___   __ _ _ __ __| | ___ _ __ 
| |/\| | | |/ / | |  _  |/ _ \ / _` | '__/ _` |/ _ \ '__|
\  /\  / |   <| | | | | | (_) | (_| | | | (_| |  __/ |   
 \/  \/|_|_|\_\_| \_| |_/\___/ \__,_|_|  \__,_|\___|_|   
'''

    # main loop
    while True:
        print(banner)
        # TODO - More languages
        user_Choice_lang = str(input('''
        Please Choose a language:
        |   en English
        |   ceb Cebuano
        |   sv Swedish
        |   fr French
        |   de German
        |   es Spanish
        |   ja Japanese
        |   ru Russian
        |   nl Dutch
        Choice:\t'''))
        wiki = wikipediaapi.Wikipedia(user_Choice_lang)

        # Page Choice loop
        while user_Choice_lang in languages:
            # Sets user choice page to exact search string
            while True:
                user_Choice_page = wiki.page(str(input("\nEnter a Topic:\t")))
                if doesPageExist(user_Choice_page) == 0:
                    print("Page does not exist and no related pages found.")
                else:
                    break

            if (" may refer to:") in pageSum(user_Choice_page)[1]:
                print(f"{user_Choice_page} may refer to different wikipedia pages.\nPlease Select One:")
                iteration = 0
                for entry in print_links(user_Choice_page):
                    print(f"{iteration}. {entry}")
                    list.update({f"{iteration}": f"{entry}"})
                    iteration += 1

                user_Choice_dl_relatedpages = input("Number of Desired Entry: (Or if you want to download all, enter \"All\")\nChoice: ")

                while True:
                    try:
                        if user_Choice_dl_relatedpages in ("ALL", "all", "All"):
                            for sub_page in print_links(user_Choice_page):
                                print("Adding Disambiguation:", sub_page)
                                pages.append(sub_page)

                        else:
                            user_Choice_page = wiki.page(extractTitle(user_Choice_dl_relatedpages, wiki, list))
                            print(user_Choice_page)

                    except(ValueError, KeyError):
                        print(f"Incorrect Value, please only enter values up to {len(user_Choice_dl_relatedpages)}")
                    break

            # Page Exists Check
            if doesPageExist(user_Choice_page) == 1:

                print(f'''Captured {wiki.page(user_Choice_page)} and all containing links
    It looks like this:
    {pageSum(user_Choice_page)}

    It's related links are:
    {print_links(user_Choice_page)}

    Download how many pages? 
    Available sub pages: {len(print_links(user_Choice_page))}
    (Enter '1' if you only want to download the captured page.)
    ''')
                # Run the loop until we've reached user preference of relational page depth
                # When loop = user preference, break the loop
                loop = 0
                while True:
                    try:
                        user_Choice_page_amount = int(input("Pages to Download: "))
                        for sub_page in print_links(user_Choice_page):
                            print("Adding subpage:", sub_page)
                            pages.append(sub_page)
                            # "Look, I know this is a half baked way of doing this but I promise you,
                            # I will fix this method."
                            #       -The last thought I will ever have about doing it this way
                            loop += 1
                            if loop == user_Choice_page_amount:
                                break

                    except ValueError:
                        print("Please enter an integer up to {}".format(len(print_links(user_Choice_page))))
                    break

                print("User choice page title: ", user_Choice_page.title)

                # Download starts here

                filename = str(input("Enter Filename for the hoard\nFilename:\t"))
                zipObj = ZipFile(f"{filename}", "w")

                # Add to this if there are more common characters you want
                # to avoid in your filenames from your field/language
                chars = str("'\" /")

                print("Hoarding..")
                todelete = []

                with ZipFile(f"{filename}.zip", 'w') as zipObj:
                    with open(f"{filename}.txt", "w+", encoding="utf-8") as f:
                        f.write(pageInfo(user_Choice_page))
                        zipObj.write(f"{f.name}")

                    for page in range(len(pages)):
                        user_Choice_page = wiki.page(pages[page][0])
                        if doesPageExist(user_Choice_page) == 0:
                            print("Page not found")
                        title = re.sub('[^A-Za-z0-9]+', '', user_Choice_page.title)
                        #filename = user_Choice_page.title[0]
                        print(".")
                        with open(f"{title}.txt", "w+", encoding="utf-8") as b:
                            b.write(user_Choice_page.text)
                            zipObj.write(f"{b.name}")
                            todelete.append(f"{b.name}")
                for file in todelete:
                    os.remove(f"{file}")

                os.remove(f"{filename}.txt")
                os.remove(f"{filename}")

            else:
                print("Page Does Not Exist")


# Functions
# Formatting may seem odd but it structures the actual code far better
def pageSum(page):
    # to return full page summary
    s = len(page.summary)
    return page.title, page.summary[:s]


def pageInfo(page):
    return page.text


def pageHTML(page):
    return page.page


# Returns boolean
def doesPageExist(page):
    if page.exists() == True:
        return 1
    else:
        return 0


# Relational pages get
def print_links(page):
    linklist = []
    links = page.links
    for title in sorted(links.keys()):
        linklist.append((title, links[title]))

    return linklist


# Thank you jared
def extractTitle(title, lang, list):
    user_title = str((lang.page(list.get(f"{title}", ""))))
    matched = str(re.findall('''(?<=')\s*[^']+?\s*(?=')''', user_title)).strip("[]\'")
    return matched


if __name__ == "__main__":
    main()
