from utils.tosenum import TOSEnum

class TOSLanguage(TOSEnum):
    en = 0  # english
    ja = 1  # japanese
    ko = 2  # korean
    zh = 3  # traditional chinese
    pt = 4  # portiugues
    de = 5  # deutsch
    th = 6  # thai
    ru = 7  # russian
    @staticmethod
    def to_string(value):
        return {
            TOSLanguage.en: 'en',
            TOSLanguage.ja: 'ja',
            TOSLanguage.ko: 'ko',
            TOSLanguage.zh: 'zh',
            TOSLanguage.pt: 'pt',
            TOSLanguage.de: 'de',
            TOSLanguage.th: 'th',
            TOSLanguage.ru: 'ru',

        }[value]
    @staticmethod
    def to_full_string(value):
        return {
            TOSLanguage.en: 'English',
            TOSLanguage.ja: 'Japanese',
            TOSLanguage.ko: 'Korean',
            TOSLanguage.zh: 'Taiwanese',
            TOSLanguage.pt: 'Portuguese',
            TOSLanguage.de: 'German',
            TOSLanguage.th: 'Thai',
            TOSLanguage.ru: 'Russian',
        }[value]
    @staticmethod
    def value_of(string):
        return {
            'en': TOSLanguage.en,
            'ja': TOSLanguage.ja,
            'ko': TOSLanguage.ko,
            'zh': TOSLanguage.zh,
            'pt': TOSLanguage.pt,
            'de': TOSLanguage.de,
            'th': TOSLanguage.th,
            'ru': TOSLanguage.ru,
            '': None
        }[string]
class TOSRegion(TOSEnum):
    iTOS = 0
    jTOS = 1
    kTEST = 2
    kTOS = 3
    twTOS = 4

    @staticmethod
    def to_string(value):
        return {
            TOSRegion.iTOS: 'iTOS',
            TOSRegion.jTOS: 'jTOS',
            TOSRegion.kTEST: 'kTEST',
            TOSRegion.kTOS: 'kTOS',
            TOSRegion.twTOS: 'twTOS',
        }[value]

    @staticmethod
    def value_of(string):
        return {
            'iTOS': TOSRegion.iTOS,
            'jTOS': TOSRegion.jTOS,
            'kTEST': TOSRegion.kTEST,
            'kTOS': TOSRegion.kTOS,
            'twTOS': TOSRegion.twTOS,
            '': None
        }[string]


class TOSElement(TOSEnum):
    DARK = 0
    EARTH = 1
    FIRE = 2
    HOLY = 3
    ICE = 4
    LIGHTNING = 5
    MELEE = 6
    POISON = 7
    SOUL = 8
    MAGIC = 9
    @staticmethod
    def to_string(value):
        return {
            None:"None",
            TOSElement.DARK: 'Dark',
            TOSElement.EARTH: 'Earth',
            TOSElement.FIRE: 'Fire',
            TOSElement.HOLY: 'Holy',
            TOSElement.ICE: 'Ice',
            TOSElement.LIGHTNING: 'Lightning',
            TOSElement.MELEE: 'None',
            TOSElement.POISON: 'Poison',
            TOSElement.SOUL: 'Soul',
            TOSElement.MAGIC:'Magic',
        }[value]

    @staticmethod
    def value_of(string):
        return {
            'DARK': TOSElement.DARK,
            'EARTH': TOSElement.EARTH,
            'FIRE': TOSElement.FIRE,
            'HOLY': TOSElement.HOLY,
            'ICE': TOSElement.ICE,
            'LIGHTING': TOSElement.LIGHTNING,
            'LIGHTNING': TOSElement.LIGHTNING,
            'MELEE': TOSElement.MELEE,
            'POISON': TOSElement.POISON,
            'SOUL': TOSElement.SOUL,
            'MAGIC':TOSElement.MAGIC,
            '': None
        }[string.upper()]


class TOSAttackType(TOSEnum):
    BUFF = 0
    MAGIC = 1
    MISSILE = 2
    MISSILE_BOW = 3
    MISSILE_CANNON = 4
    MISSILE_GUN = 5
    MELEE = 6
    MELEE_PIERCING = 7
    MELEE_SLASH = 8
    MELEE_STRIKE = 9
    MELEE_THRUST = 10
    TRUE = 11
    UNKNOWN = 12
    RESPONSIVE = 13
    PAD=14
    @staticmethod
    def to_string(value):
        return {
            TOSAttackType.BUFF: 'Buff',
            TOSAttackType.MAGIC: 'Magic',
            TOSAttackType.MISSILE: 'Missile',
            TOSAttackType.MISSILE_BOW: 'Bow',
            TOSAttackType.MISSILE_CANNON: 'Cannon',
            TOSAttackType.MISSILE_GUN: 'Gun',
            TOSAttackType.MELEE: 'Physical',
            TOSAttackType.MELEE_PIERCING: 'Piercing',
            TOSAttackType.MELEE_SLASH: 'Slash',
            TOSAttackType.MELEE_STRIKE: 'Strike',
            TOSAttackType.MELEE_THRUST: 'Thrust',
            TOSAttackType.TRUE: 'True Damage',
            TOSAttackType.RESPONSIVE: 'Responsive',
            TOSAttackType.PAD:'Ground',
            TOSAttackType.UNKNOWN: '',
        }[value]

    @staticmethod
    def value_of(string):
        return {
            'ARIES': TOSAttackType.MELEE_PIERCING,
            'ARROW': TOSAttackType.MISSILE_BOW,
            'CANNON': TOSAttackType.MISSILE_CANNON,
            'GUN': TOSAttackType.MISSILE_GUN,
            'HOLY': None,  # HotFix: obsolete skill #40706 uses it
            'MAGIC': TOSAttackType.MAGIC,
            'MELEE': TOSAttackType.MELEE,
            'MISSILE': TOSAttackType.MISSILE,
            'MISSLE': None,             # bug
            'SLASH': TOSAttackType.MELEE_SLASH,
            'STRIKE': TOSAttackType.MELEE_STRIKE,
            'THRUST': TOSAttackType.MELEE_THRUST,
            'TRUEDAMAGE': TOSAttackType.TRUE,
            'RESPONSIVE':TOSAttackType.RESPONSIVE,
            'PAD':TOSAttackType.PAD,
            '': TOSAttackType.UNKNOWN
        }[string.upper()]
