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
C_HEART = CRED + CBOLD + '\u2665' + CEND # <3
C_BULLET_CHRG = CYELLOW + CBOLD + '\u25B2' + CEND   # Triangle plein
C_MONEY =  CYELLOW + CBOLD + '$' + CEND   # $

C_TRE_WEAPON = ['\u272D', '\u272E', '\u272F']
C_TRE_GUN = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']

# Bullets
C_BULLET_COLOR = CYELLOW
C_BULLETS = [C_BULLET_COLOR + CBOLD + '>' + CEND,
             C_BULLET_COLOR + CBOLD + '/' + CEND,
             C_BULLET_COLOR + CBOLD + '^' + CEND,
             C_BULLET_COLOR + CBOLD + '\\' + CEND,
             C_BULLET_COLOR + CBOLD + '<' + CEND,
             C_BULLET_COLOR + CBOLD + '/' + CEND,
             C_BULLET_COLOR + CBOLD + 'v' + CEND,
             C_BULLET_COLOR + CBOLD + '\\' + CEND]
# swords
C_SWORD_COLOR = CYELLOW
C_SWORDS = [C_SWORD_COLOR + CBOLD + '-' + CEND,
            C_SWORD_COLOR + CBOLD + '/' + CEND,
            C_SWORD_COLOR + CBOLD + '|' + CEND,
            C_SWORD_COLOR + CBOLD + '\\' + CEND]
# Entity door
C_DOOR_COLOR = CBLUE
C_DOORS = [C_DOOR_COLOR + '\u2599' + CEND,
           C_DOOR_COLOR + '\u259B' + CEND,
           C_DOOR_COLOR + '\u259C' + CEND,
           C_DOOR_COLOR + '\u259F' + CEND]

# Monsters
C_MONSTERS = [CRED     + CBOLD + 'X' + CEND,
              CVIOLET2 + CBOLD + 'X' + CEND,
              CBOLD + 'X' + CEND]
C_MONSTER_RUN = CRED + CBOLD + 'X' + CEND

# Player
C_PLAYER = CBOLD + '@' + CEND

# ===================================== VILLAGE ===============================

C_VILLAGE_PATH = CVIOLET + '\u2591' + CEND
C_VILLAGE_PATH_DOOR = CYELLOW + CBOLD + '\u25A1' + CEND

C_ROOM_INSIDE = '.'

# ===================================== PAUSE =================================
C_PAUSE_BORDER = CGREYBG + ' ' + CEND
C_PAUSE_FILL = '.'

# ===================================== BAR ===================================
C_BAR_DECORATIONS = ['|', '/', '-', '\\']
