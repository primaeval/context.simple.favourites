import xbmc,xbmcgui
import sys
import urllib

def remove_formatting(label):
    label = re.sub(r"\[/?[BI]\]",'',label)
    label = re.sub(r"\[/?COLOR.*?\]",'',label)
    return label

def escape( str ):
    str = str.replace("&", "&amp;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    str = str.replace("\"", "&quot;")
    return str

def unescape( str ):
    str = str.replace("&lt;","<")
    str = str.replace("&gt;",">")
    str = str.replace("&quot;","\"")
    str = str.replace("&amp;","&")
    return str

d = xbmcgui.Dialog()

title = xbmc.getInfoLabel('ListItem.Label')
path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
icon = xbmc.getInfoLabel('ListItem.Icon')
fanart = xbmc.getInfoLabel('ListItem.Art(fanart)')
folder = xbmc.getInfoLabel('Container.FolderPath')
xml = xbmc.getInfoLabel('Window.Property(xmlfile)')

if not fanart:
    fanart = ' '
if not icon:
    icon = ' '

media = ''
if folder.startswith('addons'):
    media = folder.rsplit('/',1)[-1]
elif 'content_type' in folder:
    match = re.search('content_type=(.*?)',folder)
    if match:
        media = match.group(1)
elif 'video' in xml.lower():
    media = 'video'
elif 'music' in xml.lower():
    media = 'music'
elif 'programs' in xml.lower():
    media = 'programs'
elif 'pics' in xml.lower():
    media = 'pictures'


folder = ''
while True:
    if media in ["video"]:
        window = "videos"
    elif media in ["music","audio"]:
        window = "music"
    elif media in ["executable","programs"]:
        window = "programs"
    elif media in ["image","pictures"]:
        window = "pictures"
    else:
        window = "programs"
    what = d.select('Add to Simple Favourites',['[COLOR yellow]Add[/COLOR]','Name: %s' % title, 'Folder: %s' % folder.strip('/'), 'Type: %s' % media])

    if what == -1:
        break
    if path.startswith("plugin://script"):
        play_url = escape('RunScript("%s")' % (path))
    else:
        play_url = escape('ActivateWindow(%s,"%s",return)' % (window,path))
    if what == 0:
        favourites_file = "special://profile/addon_data/plugin.program.simple.favourites/folders/%sfavourites.xml" % folder
        url = "plugin://plugin.program.simple.favourites/add_favourite/%s/%s/%s/%s/%s" % (urllib.quote_plus(favourites_file),
        urllib.quote_plus(title),urllib.quote_plus(play_url),urllib.quote_plus(icon),urllib.quote_plus(fanart))
        xbmc.executebuiltin("PlayMedia(%s)" % url)
        break
    elif what == 1:
        new_title = d.input("Name: %s" % title,title)
        if new_title:
            title = new_title
    elif what == 2:
        top_folder = 'special://profile/addon_data/plugin.program.simple.favourites/folders/'
        where = d.browse(0, 'Choose Folder', 'files', '', False, True, top_folder)
        if not where:
            continue
        if not where.startswith(top_folder):
            d.notification("Error","Please keep to the folders path")
        else:
            folder = where.replace(top_folder,'')
    elif what == 3:
        types = ['video','audio','pictures','programs']
        new_media = d.select('Type: %s' % media,types)
        if new_media > -1:
            media = types[new_media]
