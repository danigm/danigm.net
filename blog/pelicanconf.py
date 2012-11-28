#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"danigm"
SITENAME = u"danigm.net"
SITEURL = 'http://localhost:8000'

RELATIVE_URLS = False
TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'es'

DIRECT_TEMPLATES = ('index', 'categories', 'notfound', 'tags', 'archives')

# Blogroll
LINKS =  (
    ('wadobo', 'http://wadobo.com'),
    ('CUSL', 'http://www.concursosoftwarelibre.org/'),
    ('Linux Hispano', 'http://www.linuxhispano.net'),
    ('Blog antiguo', 'http://old.danigm.net/'),
    (u'Blog más antiguo', 'http://danigm.wordpress.com/'),
)

# Social widget
SOCIAL = (
    ('twitter', 'http://twitter.com/danigm'),
    ('facebook', 'http://facebook.com/danigmx'),
    ('github', 'http://github.com/danigm'),
)

DISQUS_SITENAME = ""
TWITTER_USERNAME = "danigm"

#A list of the extensions that the markdown processor will use.
MD_EXTENSIONS = ['codehilite', 'extra']

# The static paths you want to have accessible on the output path “static”. By
# default, pelican will copy the ‘images’ folder to the output folder.
# static paths will be copied under the same name
STATIC_PATHS = ["pictures", ]

# relative url to output the atom feed.
FEED_ATOM = "atom.xml"

# relative url to output the rss feed.
FEED_RSS = 'rss.xml'

CATEGORY_FEED_RSS = 'feeds/cat/%s.rss.xml'
CATEGORY_FEED_ATOM = 'feeds/cat/%s.atom.xml'

# relative url to output the tags atom feed. It should be defined using a “%s”
# matchin the tag name
TAG_FEED_ATOM = 'feeds/tags/%s.atom.xml'

# relative url to output the tag RSS feed
TAG_FEED_RSS = "feeds/tags/%s.rss.xml"


DEFAULT_PAGINATION = 3
WITH_PAGINATION = True

# Count of different font sizes in the tag cloud.
TAG_CLOUD_STEPS = 4

# Maximum tags count in the cloud.
TAG_CLOUD_MAX_ITEMS = 200

THEME = "danigm-theme"
#THEME = "dev-random"
