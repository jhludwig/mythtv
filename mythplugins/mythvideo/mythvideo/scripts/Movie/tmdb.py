#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ----------------------
# Name: tmdb.py
# Python Script
# Author: R.D. Vaughan
# Purpose:
#   This python script is intended to perform Movie data lookups
#   based on information found on the http://themoviedb.org/ website. It
#   follows the MythTV standards set for grabbers
#   http://www.mythtv.org/wiki/MythVideo_Grabber_Script_Format
#   This script uses the python module tmdb_api.py which should be included
#   with this script.
#   The tmdb_api.py module uses the full access v2.1 XML api published by
#   themoviedb.org see: http://api.themoviedb.org/2.1/
#   Users of this script are encouraged to populate themoviedb.org with Movie
#   information, posters and fan art. The richer the source the more
#   valuable the script.
# Command example:
# See help (-u and -h) options
#
# Design:
#   1) Verify the command line options (display help or version and exit)
#   2) Verify that themoviedb.org has the Movie being requested exit if does not exit
#   3) Find the requested information and send to stdout if any found
#
#
# License:Creative Commons GNU GPL v2
# (http://creativecommons.org/licenses/GPL/2.0/)
#-------------------------------------
__title__ ="TheMovieDB APIv2 Query";
__author__="R.D.Vaughan"
__version__="v0.1.2"
# 0.1.0 Initial development
# 0.1.1 Alpha Release
# 0.1.2 New movie data fields now have proper key names
#       Dynamic CamelCoding of keys if they are not already in the translation list
#       Fixed and re-arranged some code for minor issues.

__usage_examples__='''
Request tmdb.py verison number:
> ./tmdb.py -v
themoviedb.org Query (v0.1.0) by R.D.Vaughan

Request a list of matching movie titles:
> ./tmdb.py -M "Avatar"
19995:Avatar (2009)
8514:The Avatar State (2006)
8518:Avatar Day (2006)
13336:Chrysalis (2007)
8493:The Avatar Returns (2005)
8500:Avatar Roku (Winter Solstice (2)) (2005)
8481:The Avatar and the Firelord (2007)
12467:Avatar Aang (2008)

Request movie details using a TMDB#:
> ./tmdb.py -D 19995
Title:Avatar
Year:2009
ReleaseDate:2009-12-18
InetRef:19995
URL:http://www.themoviedb.org/movie/19995
Director:James Cameron
Plot:A band of humans are pitted in a battle against a distant planet's indigenous population.
Runtime:166
Coverart:http://images.themoviedb.org/posters/76198/avatar_xlg.jpg
Fanart:http://images.themoviedb.org/backdrops/72434/wallpaper_05_1280x1024.jpg,http://images.themoviedb.org/backdrops/69971/avatar-newstills-101-full-01.jpg,http://images.themoviedb.org/backdrops/69968/avatar-3.jpg,http://images.themoviedb.org/backdrops/69965/avatar-2.jpg,http://images.themoviedb.org/backdrops/68648/Avatar.jpg,http://images.themoviedb.org/backdrops/67496/avatar2_resize.jpg,http://images.themoviedb.org/backdrops/67487/avatar1_resized.jpg,http://images.themoviedb.org/backdrops/52193/avatar_movie_based_ubisoft_game_concept_art_1.jpg
Cast:Sam Worthington, Zoe Saldana, Stephen Lang, Sigourney Weaver, Michelle Rodríguez
Genres:Science Fiction
Studios:Lightstorm Entertainment
Type:movie
Imdb:0499549
AlternativeName:Avatar
Homepage:http://www.avatarmovie.com/
Trailer:http://www.youtube.com/watch?v=j6AAt-oV3wE

Request movie details using a IMDB#:
> ./tmdb.py -D 0499549
Title:Avatar
Year:2009
ReleaseDate:2009-12-18
InetRef:19995
URL:http://www.themoviedb.org/movie/19995
Director:James Cameron
Plot:A band of humans are pitted in a battle against a distant planet's indigenous population.
Runtime:166
Coverart:http://images.themoviedb.org/posters/76198/avatar_xlg.jpg
Fanart:http://images.themoviedb.org/backdrops/72434/wallpaper_05_1280x1024.jpg,http://images.themoviedb.org/backdrops/69971/avatar-newstills-101-full-01.jpg,http://images.themoviedb.org/backdrops/69968/avatar-3.jpg,http://images.themoviedb.org/backdrops/69965/avatar-2.jpg,http://images.themoviedb.org/backdrops/68648/Avatar.jpg,http://images.themoviedb.org/backdrops/67496/avatar2_resize.jpg,http://images.themoviedb.org/backdrops/67487/avatar1_resized.jpg,http://images.themoviedb.org/backdrops/52193/avatar_movie_based_ubisoft_game_concept_art_1.jpg
Cast:Sam Worthington, Zoe Saldana, Stephen Lang, Sigourney Weaver, Michelle Rodríguez
Genres:Science Fiction
Studios:Lightstorm Entertainment
Type:movie
Imdb:0499549
AlternativeName:Avatar
Homepage:http://www.avatarmovie.com/
Trailer:http://www.youtube.com/watch?v=j6AAt-oV3wE

Request a list of People matching a name:
> ./tmdb.py -P "Cruise"
500:Tom Cruise
77716:Cruise Moylan

Request a Person's information using their TMDB id number:
> ./tmdb.py -I 500
name:Tom Cruise
also_known_as:Thomas Cruise Mapother IV
birthday:1962-07-03
birthplace:Syracuse, New York, USA
filmography:"War of the Worlds","character:Ray Ferrier"
filmography:"War of the Worlds","id:74"
filmography:"War of the Worlds","job:Actor"
filmography:"War of the Worlds","url:http://www.themoviedb.org/movie/74"
...
filmography:"All the Right Moves","character:Stefen Djordjevic"
filmography:"All the Right Moves","id:18172"
filmography:"All the Right Moves","job:Actor"
filmography:"All the Right Moves","url:http://www.themoviedb.org/movie/18172"
id:500
known_movies:33
popularity:2
url:http://www.themoviedb.org/person/500

Request Movie details using a Hash value:
> ./tmdb.py -H "00277ff46533b155"
Title:Willow
Year:1988
ReleaseDate:1988-05-20
InetRef:847
URL:http://www.themoviedb.org/movie/847
Director:Ron Howard
Plot:The dwarfish Nelwyn Willow Ufgood begins on an adventurous journey to protect the foundling Elora Danan who after a prophesy from the evil tyrant king Bavmorda must prepare for her end. Fantasy film from 1988 written by George Lucas.
UserRating:7.0
Runtime:126
Coverart:http://images.themoviedb.org/posters/73366/folder.jpg,http://images.themoviedb.org/posters/20426/Willow.jpg
Fanart:http://images.themoviedb.org/backdrops/19772/WILLOW-fanart.jpg,http://images.themoviedb.org/backdrops/11663/Willow_1920x1080.jpg
Cast:Val Kilmer, Joanne Whalley, Warwick Davis, Jean Marsh, Patricia Hayes, Billy Barty, Pat Roach, Gavan O'Herlihy, David Steinberg, Phil Fondacaro
Genres:Adventure,Fantasy
Countries:United Kingdom, United States of America, New Zealand
ScreenPlay:Bob Dolman
Studios:Imagine Entertainment,Sony,Sony Pictures,Metro-Goldwyn-Mayer,Lucasfilm Ltd.
Producer:Nigel Wooll
ProductionDesign:Allan Cameron
DirectorOfPhotography:Adrian Biddle
OriginalMusicComposer:James Horner
Story:George Lucas
CostumeDesign:Barbara Lane
Editor:Daniel P. Hanley, Mike Hill, Richard Hiscott
Type:movie
Casting:Janet Hirshenson, Jane Jenkins
AssociateProducer:Joe Johnston
Popularity:3
Budget:35000000
Imdb:0096446
ArtDirection:Tim Hutchinson, Jim Pohl, Tony Reading, Kim Sinclair, Malcolm Stone

'''

# Version 0.1.0 Initial development

import sys, os
from optparse import OptionParser
import re
from string import capitalize


class OutStreamEncoder(object):
    """Wraps a stream with an encoder
    """
    def __init__(self, outstream, encoding=None):
        self.out = outstream
        if not encoding:
            self.encoding = sys.getfilesystemencoding()
        else:
            self.encoding = encoding

    def write(self, obj):
        """Wraps the output stream, encoding Unicode strings with the specified encoding"""
        if isinstance(obj, unicode):
            self.out.write(obj.encode(self.encoding))
        else:
            self.out.write(obj)

    def __getattr__(self, attr):
        """Delegate everything but write to the stream"""
        return getattr(self.out, attr)
# Sub class sys.stdout and sys.stderr as a utf8 stream. Deals with print and stdout unicode issues
sys.stdout = OutStreamEncoder(sys.stdout)
sys.stderr = OutStreamEncoder(sys.stderr)

# Verify that the tmdb_api modules are installed and accessable
try:
    import tmdb.tmdb_api as tmdb_api
    from tmdb.tmdb_exceptions import (TmdBaseError, TmdHttpError, TmdXmlError, TmdbUiAbort, TmdbMovieOrPersonNotFound,)
except Exception:
    sys.stderr.write('''
The subdirectory "tmdb" containing the modules tmdb_api.py (v0.1.1 or greater), tmdb_ui.py,
tmdb_exceptions.py must be in the same directory as tmdb.py.
They should have been included with the distribution of tmdb.py.

''')
    sys.exit(1)

if tmdb_api.__version__ < '0.1.1':
    sys.stderr.write("\n! Error: Your current installed tmdb_api.py version is (%s)\nYou must at least have version (0.1.1) or higher.\n" % tmdb_api.__version__)
    sys.exit(1)


class moviedbQueries():
    '''Methods that query themoviedb.org for metadata and outputs the results to stdout any errors are output
    to stderr.
    '''
    def __init__(self,
                apikey,
                mythtv = False,
                interactive = False,
                select_first = False,
                debug = False,
                custom_ui = None,
                language = None,
                search_all_languages = False, ###CHANGE - Needs to be added
                ):
        """apikey (str/unicode):
            Specify the themoviedb.org API key. Applications need their own key.
            See http://api.themoviedb.org/2.1/ to get your own API key

        mythtv (True/False):
            When True, the movie metadata is being returned has the key and values massaged to match MythTV
            When False, the movie metadata is being returned matches what TMDB returned

        interactive (True/False):
            When True, uses built-in console UI is used to select the correct show.
            When False, the first search result is used.

        select_first (True/False):
            Automatically selects the first series search result (rather
            than showing the user a list of more than one series).
            Is overridden by interactive = False, or specifying a custom_ui

        debug (True/False):
             shows verbose debugging information

        custom_ui (tvdb_ui.BaseUI subclass):
            A callable subclass of tvdb_ui.BaseUI (overrides interactive option)

        language (2 character language abbreviation):
            The language of the returned data. Is also the language search
            uses. Default is "en" (English). For full list, run..

            >>> MovieDb().config['valid_languages'] #doctest: +ELLIPSIS
            ['da', 'fi', 'nl', ...]

        search_all_languages (True/False):
            By default, TMDB will only search in the language specified using
            the language option. When this is True, it will search for the
            show in any language

        """
        self.config = {}

        self.config['apikey'] = apikey
        self.config['moviedb'] = tmdb_api.MovieDb(apikey, mythtv = mythtv,
                interactive = interactive,
                select_first = select_first,
                debug = debug,
                custom_ui = custom_ui,
                language = language,
                search_all_languages = search_all_languages,)
        self.mythtvgrabber = [u'Title', u'Subtitle', u'Year', u'ReleaseDate', u'InetRef', u'URL', u'Director', u'Plot', u'UserRating', u'MovieRating', u'Runtime', u'Season', u'Episode', u'Coverart', u'Fanart', u'Banner', u'Screenshot', u'Cast', u'Genres', u'Countries', u'ScreenPlay', u'Studios', u'Producer', u'ProductionDesign', u'DirectorOfPhotography', u'OriginalMusicComposer', u'Story', u'CostumeDesign', u'Editor', u'Type', u'Casting', u'AssociateProducer', u'Popularity', u'Budget', u'Imdb', u'ArtDirection']
    # end __init__()

    def movieSearch(self, title):
        '''Search for movies that match the title and output their "tmdb#:Title" to stdout
        '''
        try:
            for match in self.config['moviedb'].searchTitle(title):
                if not match.has_key('released'):
                    name = match['name']
                elif len(match['released']) > 3:
                    name = u"%s (%s)" % (match['name'], match['released'][:4])
                else:
                    name = match['name']
                sys.stdout.write( u'%s:%s\n' % (match[u'id'], name))
        except TmdbUiAbort, msg:
            sys.stderr.write(u"! Error: An tmdb exception was raised (%s)\n" % msg)
        except:
            sys.stderr.write(u"! Error: Unknown tmdb_api Title search error\n")
    # end movieSearch()

    def peopleSearch(self, persons_name):
        '''Search for People that match the name and output their "tmdb#:Name" to stdout
        '''
        try:
            for match in self.config['moviedb'].searchPeople(persons_name):
                sys.stdout.write( u'%s:%s\n' % (match[u'id'], match['name']))
        except TmdbUiAbort, msg:
            sys.stderr.write(u"! Error: An tmdb exception was raised (%s)\n" % msg)
        except:
            sys.stderr.write(u"! Error: Unknown tmdb_api People search error\n")
    # end moviePeople()

    def camelcase(self, value):
        '''Make a string CamelCase
        '''
        return u"".join([capitalize(w) for w in re.split(re.compile(u"[\W_]*"), value)])
    # end camelcase()

    def displayMovieData(self, data):
        '''Display movie data to stdout # u'ArtDirection'
        '''
        data_keys = data.keys()
        data_keys_org = data.keys()
        for index in range(len(data_keys)):
            data_keys[index] = data_keys[index].replace(u' ',u'').lower()

        for key in self.mythtvgrabber:
            if  key.lower() in data_keys:
                sys.stdout.write(u"%s:%s\n" % (key, data[data_keys_org[data_keys.index(key.lower())]]))

        mythtvgrabber = []
        for item in self.mythtvgrabber:
            mythtvgrabber.append(item.lower())
        for key in data_keys:
            if not key in mythtvgrabber:
                sys.stdout.write(u"%s:%s\n" % (self.camelcase(data_keys_org[data_keys.index(key)]), data[data_keys_org[data_keys.index(key)]]))
    # end displayMovieData(()


    def movieData(self, tmdb_id):
        '''Get Movie data by IMDB or TMDB number and display "key:value" pairs to stdout
        '''
        if len(tmdb_id) == 7:
            self.displayMovieData(self.config['moviedb'].searchIMDB(tmdb_id))
        else:
            self.displayMovieData(self.config['moviedb'].searchTMDB(tmdb_id))
    # end movieData()

    def peopleData(self, tmdb_id):
        '''Get People data by TMDB people id number and display "key:value" pairs to stdout
        '''
        data = self.config['moviedb'].personInfo(tmdb_id)
        sys.stdout.write(u'%s:%s\n' % (u'name', data[u'name']))
        keys = sorted(data.keys())
        for key in keys:
            if key == u'name':
                continue
            if key in ['also_known_as', 'filmography', 'images' ]:
                for k in data[key]:
                    if key == 'also_known_as':
                        sys.stdout.write(u'%s:%s\n' % (key, k))
                    elif key == 'filmography':
                        kys = sorted(k.keys())
                        for c in kys:
                            if c == u'name':
                                continue
                            sys.stdout.write(u'%s:"%s","%s:%s"\n' % (key, k[u'name'], c, k[c]))
                    else:
                        kys = sorted(k.keys())
                        for c in kys:
                            if c == u'name':
                                continue
                            sys.stdout.write(u'%s:"%s"","%s:%s"\n' % (key, k[u'name'], c, k[c]))
            else:
                sys.stdout.write(u'%s:%s\n' % (key, data[key]))
    # end peopleData()

    def hashData(self, hash_value):
        '''Get Movie data by Hash value and display "key:value" pairs to stdout
        '''
        self.displayMovieData(self.config['moviedb'].searchHash(hash_value))
    # end hashData()

# end Class moviedbQueries()


def main():
    """Gets movie details using an IMDB# and a TMDB# OR get People information using a name
    """
    # themoviedb.org api key given by Travis Bell for Mythtv
    apikey = "c27cb71cff5bd76e1a7a009380562c62"

    parser = OptionParser(usage=u"%prog usage: tmdb -hdruviomMPFBDS [parameters]\n <series name or 'series and season number' or 'series and season number and episode number'>\n\nFor details on using tmdb with Mythvideo see the tmdb wiki page at:\nhttp://www.mythtv.org/wiki/tmdb.py")

    parser.add_option(  "-d", "--debug", action="store_true", default=False, dest="debug",
                        help=u"Show debugging info")
    parser.add_option(  "-r", "--raw", action="store_true",default=False, dest="raw",
                        help=u"Dump raw data only")
    parser.add_option(  "-u", "--usage", action="store_true", default=False, dest="usage",
                        help=u"Display examples for executing the tmdb script")
    parser.add_option(  "-v", "--version", action="store_true", default=False, dest="version",
                        help=u"Display version and author")
    parser.add_option(  "-i", "--interactive", action="store_true", default=False, dest="interactive",
                        help=u"Interaction mode (allows selection of a specific Movie or Person)")
    parser.add_option(  "-l", "--language", metavar="LANGUAGE", default=u'en', dest="language",
                        help=u"Select data that matches the specified language fall back to english if nothing found (e.g. 'es' Español, 'de' Deutsch ... etc)")
    parser.add_option(  "-M", "--movielist", action="store_true", default=False, dest="movielist",
                        help=u"Get matching Movie list")
    parser.add_option(  "-D", "--moviedata", action="store_true", default=False, dest="moviedata",
                        help=u"Get Movie metadata including graphic URLs")
    parser.add_option(  "-H", "--moviehash", action="store_true", default=False, dest="moviehash",
                        help=u"Get Movie metadata including graphic URLs using a Hash value.\nSee: http://api.themoviedb.org/2.1/methods/Hash.getInfo")
    parser.add_option(  "-P", "--peoplelist", action="store_true", default=False, dest="peoplelist",
                        help=u"Get matching People list")
    parser.add_option(  "-I", "--peopleinfo", action="store_true", default=False, dest="peopleinfo",
                        help=u"Get A Person's metadata including graphic URLs")

    opts, args = parser.parse_args()

    # Make alls command line arguments unicode utf8
    for index in range(len(args)):
        args[index] = unicode(args[index], 'utf8')

    if opts.debug:
        sys.stdout.write("\nopts: %s\n" % opts)
        sys.stdout.write("\nargs: %s\n\n" % args)

    # Process version command line requests
    if opts.version:
        sys.stdout.write("%s (%s) by %s\n" % (
        __title__, __version__, __author__ ))
        sys.exit(0)

    # Process usage command line requests
    if opts.usage:
        sys.stdout.write(__usage_examples__)
        sys.exit(0)

    if not len(args) == 1:
        sys.stderr.write("\n! Error: There must be one value for any option, Your options are (%s)\n\n" % (args))
        sys.exit(1)

    Queries = moviedbQueries(apikey,
                mythtv = True,
                interactive = opts.interactive,
                select_first = False,
                debug = opts.debug,
                custom_ui = None,
                language = opts.language,
                search_all_languages = False,)

    # Process requested option
    if opts.movielist:                  # Movie Search -M
       Queries.movieSearch(args[0])
    elif opts.moviedata:                # Movie metadata -D
       Queries.movieData(args[0])
    elif opts.peoplelist:               # People Search -P
       Queries.peopleSearch(args[0])
    elif opts.peopleinfo:               # Person metadata -I
       Queries.peopleData(args[0])
    elif opts.moviehash:                # Movie metadata using a hash value -H
       Queries.hashData(args[0])

    sys.exit(0)
# end main()

if __name__ == '__main__':
    main()
