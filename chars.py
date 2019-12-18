#!/usr/bin/env python3
"""
CHARS
"""
# pylint: disable=C0326

CEND        = '\33[0m'
CBOLD       = '\33[1m'
CITALIC     = '\33[3m'
CURL        = '\33[4m'
CBLINK      = '\33[5m'
CBLINK2     = '\33[6m'
CSELECTED   = '\33[7m'

CBLACK      = '\33[30m'
CRED        = '\33[31m'
CGREEN      = '\33[32m'
CYELLOW     = '\33[33m'
CBLUE       = '\33[34m'
CVIOLET     = '\33[35m'
CBEIGE      = '\33[36m'
CWHITE      = '\33[37m'

CBLACKBG    = '\33[40m'
CREDBG      = '\33[41m'
CGREENBG    = '\33[42m'
CYELLOWBG   = '\33[43m'
CBLUEBG     = '\33[44m'
CVIOLETBG   = '\33[45m'
CBEIGEBG    = '\33[46m'
CWHITEBG    = '\33[47m'

CGREY       = '\33[90m'
CRED2       = '\33[91m'
CGREEN2     = '\33[92m'
CYELLOW2    = '\33[93m'
CBLUE2      = '\33[94m'
CVIOLET2    = '\33[95m'
CBEIGE2     = '\33[96m'
CWHITE2     = '\33[97m'

CGREYBG     = '\33[100m'
CREDBG2     = '\33[101m'
CGREENBG2   = '\33[102m'
CYELLOWBG2  = '\33[103m'
CBLUEBG2    = '\33[104m'
CVIOLETBG2  = '\33[105m'
CBEIGEBG2   = '\33[106m'
CWHITEBG2   = '\33[107m'

# ===================================== ENTITY ========================================

# Treasure
C_HEART = CRED + '\u2665' + CEND # <3
C_BULLET_CHRG = CYELLOW + '\u25B2' + CEND   # Triangle plein
C_MONEY =  CYELLOW + '$' + CEND   # $

# Bullets
C_BULLET_COLOR = CYELLOW
C_BULLETS = [C_BULLET_COLOR + '>' + CEND,
             C_BULLET_COLOR + '/' + CEND,
             C_BULLET_COLOR + '^' + CEND,
             C_BULLET_COLOR + '\\' + CEND,
             C_BULLET_COLOR + '<' + CEND,
             C_BULLET_COLOR + '/' + CEND,
             C_BULLET_COLOR + 'v' + CEND,
             C_BULLET_COLOR + '\\' + CEND]
# swords
C_SWORD_COLOR = CYELLOW
C_SWORDS = [C_SWORD_COLOR + '-' + CEND,
            C_SWORD_COLOR + '/' + CEND,
            C_SWORD_COLOR + '|' + CEND,
            C_SWORD_COLOR + '\\' + CEND]
# Entity door
C_DOOR_COLOR = CBLUE
C_DOORS = [C_DOOR_COLOR + '\u2599' + CEND,
           C_DOOR_COLOR + '\u259B' + CEND,
           C_DOOR_COLOR + '\u259C' + CEND,
           C_DOOR_COLOR + '\u259F' + CEND]

# Monsters
C_MONSTERS = [CRED     + 'X' + CEND,
              CVIOLET2 + 'X' + CEND,
              'X']

# Player
C_PLAYER = '@'

#Treasure
C_TRE_WEAPON = ['\u272D', '\u272E', '\u272F']
C_TRE_GUN = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']

# ===================================== VILLAGE ========================================

C_VILLAGE_PATH = "\033[33m" + '\u2591' + "\033[0m"
C_VILLAGE_PATH_DOOR = "\033[33m" + '\u25A1' + "\033[0m"

C_ROOM_INSIDE = '.'
