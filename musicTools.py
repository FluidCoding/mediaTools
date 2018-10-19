#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re, platform
from pprint import pprint as pp

# Metadata IO
# from mutagen.flac import FLAC

# The Selfhosted Music-Toolbox

# + -------------------------------------------------------------------
# | Base Directory to the root directory of the music
# |
# | audio/
# |		artists/
# |
# + -------------------------------------------------------------------
if platform.system() == 'Darwin':
	AUDIO_LIB='/Volumes/rxd01/audio/library'
else:
	AUDIO_LIB='/mnt/rxd01/audio/library'

AUDIO_DIR_ARTISTS = AUDIO_LIB + '/artists'

# + -------------------------------------------------------------------
# | Album Base Name: Artist - Year - Album (Edition)
# |
# | Examples:
# | The Wombats - 2011 - This Modern Glitch (Australian Tour Edition)
# | The Wombats - 2015 - Glitterbug
# | 
# + -------------------------------------------------------------------
PATTERN_ALBUM_BASE = '^(.*) - ([1-2]\d{3}) - (.*)'

# + -------------------------------------------------------------------
# | Album Metadata: [SOURCE - FORMAT - QUALITY]
# |
# | Examples:
# | [CD - FLAC - Lossless]
# | [GAME - MP3 - 320]
# | [WEB - FLAC - Lossless]
# | [VINYL - FLAC - 16-44]
# | 
# + -------------------------------------------------------------------
PATTERN_ALBUM_FORMATS = '(WAVE|FLAC|ALAC|MP3|AAC)'
PATTERN_ALBUM_SOURCES = '(CD|GAME|WEB|TAPE|VINYL)'
PATTERN_ALBUM_QUALITY = '(Lossless|24-48|16-44|320|224|192|128|V0|V1)'
PATTERN_ALBUM_META = '( \[' + PATTERN_ALBUM_SOURCES + ' - ' + PATTERN_ALBUM_FORMATS + ' - ' + PATTERN_ALBUM_QUALITY + '\])'

# + -------------------------------------------------------------------
# | Album Identifier: {IDENTIFIER}
# | A String that belongs to this particular release
# | e.g. Barcode, CatalogueID, Label+Id, ...
# |
# | Examples:
# | {3716232}
# | {US, 509992 65787 2 9}
# | 
# | Mainly used with CDs/Vinyl and therefore optional
# + ------------------------------------------------------------------- 
PATTERN_ALBUM_CATALOG = '( \{.*\})?'

# + -------------------------------------------------------------------
# | File Naming
# |
# | Example:
# | 01 Life in Technicolor II.flac
# | 
# + ------------------------------------------------------------------- 
PATTERN_AFILE_TRACKNAME = '^(\d{1,2} (.*).)'
PATTERN_AFILE_EXTENSION = '\.(mp3|m4a|aac|flac|alac|wav)'


# + -------------------------------------------------------------------
# | Main Patterns: Album / File
# |
# | Bundle the defined patterns to use them in the validation
# + ------------------------------------------------------------------- 
PATTERN_ALBUM = PATTERN_ALBUM_BASE + PATTERN_ALBUM_META + PATTERN_ALBUM_CATALOG
PATTERN_AFILE = PATTERN_AFILE_TRACKNAME + PATTERN_AFILE_EXTENSION

# + -------------------------------------------------------------------
# | Additional Patterns
# |
# | Album MultiDisc: CD1,CD2 / CD01,CD02,.. / Disc01, Disc02 / ...
# + ------------------------------------------------------------------- 
PATTERN_ALBUM_MULTIDISC = '^((CD|Disc) ?[0-9]+)$'


# + -------------------------------------------------------------------
# | Artist Folder Contents:
# |
# | artist.ini			<-- Contains Metadata / IDs
# | artist.(jpg|png) 	<-- Main Picture for Galleries etc.
# | <ALBUMS>			<-- All Albums defined by pattern
# | 
# + ------------------------------------------------------------------- 
def validate_artist(artistPath):
	root = os.listdir(artistPath)
	if root == []:
		print("! - Artist is empty")
		return False
	return True

# + -------------------------------------------------------------------
# | Album Validation
# | Single Disc Album:
# | 	TRACKNUMBER - TRACKTITLE.EXT
# |		Cover.jpg
# | 	Scans/Artwork / Front.jpg, Back.jpg
# | 	ALBUMARTIST - ALBUM.cue
# | 	ALBUMARTIST - ALBUM.log
# ---
# | Multi-Disc Album:
# | 	CD1 / TRACKNUMBER - TRACKTITLE.EXT
# | 	CD1 / Cover.jpeg
# | 	CD1 / Scans|Artwork / ...
# | 	CD1 / ALBUMARTIST - ALBUM.cue
# |
# + -------------------------------------------------------------------

def validate_album(albumPath):
	root = os.listdir(albumPath)
	if root == []:
		print("! - Album is empty")
		return False
	discs = [re.match(PATTERN_ALBUM_MULTIDISC, element) for element in root]
	count = len([element for element in discs if element is not None])
	if(count > 1):
		for element in root:
			if (re.match(multiDiscPattern, element)):
				validate_album(os.path.join(albumPath, element))
	else:
		return True
		


def validate_album_name(albumFolder):
	return re.match(PATTERN_ALBUM, albumFolder)

# + -------------------------------------------------------------------
# | Main Function - Script Entrypoint
# |
# + -------------------------------------------------------------------
def validate_artist_section(sectionPath):
	good=[]
	bad=[]
	excludes=['.DS_Store', 'Artwork']
	for artist in sorted(os.listdir(sectionPath)):
		artistPath = os.path.join(sectionPath, artist)
		for album in sorted(os.listdir(artistPath)):
			albumPath = os.path.join(artistPath, album)
			if album in excludes:
				continue
			valid = validateAlbumFolder(albumPath)
			name_ok = validateAlbumFolderName(album)
			if (name_ok):
				good.append(album)
			else:
				bad.append(album)
	print('Total Bad: ', len(bad))
	pp(bad)
	print('-----------------------')
	print('Total Good: ', len(good))
	pp(good)


# + -------------------------------------------------------------------
# | Main Function - Script Entrypoint
# |
# + -------------------------------------------------------------------
if __name__ == "__main__":
	validateArtistSection(AUDIO_DIR_ARTISTS)

# EOF
