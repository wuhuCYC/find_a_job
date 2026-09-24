"""地点分类：把各家 ATS 五花八门的地点字符串归到区域。

区域：OC（橙县）/ LA（洛杉矶及周边）/ SD（圣地亚哥）/ BAY（湾区）/ CA_OTHER / REMOTE_US / OTHER
"""
from __future__ import annotations

import re

OC_CITIES = [
    "irvine", "newport beach", "costa mesa", "santa ana", "tustin", "anaheim", "fullerton",
    "lake forest", "aliso viejo", "mission viejo", "laguna hills", "laguna niguel", "laguna beach",
    "huntington beach", "fountain valley", "garden grove", "brea", "cypress", "buena park",
    "rancho santa margarita", "san clemente", "dana point", "foothill ranch", "yorba linda",
    "seal beach", "westminster", "placentia", "la palma", "orange county", "ladera ranch",
    "san juan capistrano", "los alamitos", "stanton", "la habra",
]
# 注意：单独的 "Orange" 城市容易误判（Orange Street / Orange County），用下面的正则单独处理
_ORANGE_CITY = re.compile(r"\borange,\s*(?:ca|california)\b", re.I)

LA_CITIES = [
    "los angeles", "santa monica", "culver city", "pasadena", "glendale", "burbank", "beverly hills",
    "west hollywood", "el segundo", "playa vista", "marina del rey", "venice", "torrance", "long beach",
    "westlake village", "woodland hills", "sherman oaks", "calabasas", "century city", "manhattan beach",
    "redondo beach", "hermosa beach", "hawthorne", "inglewood", "downey", "monrovia", "arcadia",
    "el monte", "alhambra", "irwindale", "city of industry", "diamond bar", "pomona", "thousand oaks",
    "agoura hills", "moorpark", "carson", "gardena", "van nuys", "north hollywood", "encino",
    "studio city", "chatsworth", "northridge", "valencia", "santa clarita", "cerritos", "whittier",
    "san gabriel", "rosemead", "monterey park", "west covina", "covina", "la canada", "universal city",
    "hollywood", "westwood", "brentwood", "downtown la", "dtla", "greater los angeles", "simi valley",
    "camarillo", "oxnard", "ventura", "lancaster", "san pedro", "wilmington", "el monte",
]
_LA_ABBR = re.compile(r"(?:^|[\s,(/-])l\.?a\.?(?:$|[\s,)/-])", re.I)

SD_CITIES = [
    "san diego", "la jolla", "carlsbad", "del mar", "sorrento valley", "encinitas", "oceanside",
    "escondido", "poway", "chula vista", "rancho bernardo", "san marcos", "vista, ca",
]
BAY_CITIES = [
    "san francisco", "oakland", "berkeley", "emeryville", "san jose", "palo alto", "menlo park",
    "mountain view", "sunnyvale", "santa clara", "redwood city", "san mateo", "foster city",
    "cupertino", "south san francisco", "burlingame", "pleasanton", "fremont", "milpitas",
    "walnut creek", "san ramon", "los gatos", "san bruno", "bay area", "silicon valley",
]
CA_OTHER_HINTS = [
    "sacramento", "riverside", "ontario, ca", "rancho cucamonga", "corona", "fresno", "santa barbara",
    "san luis obispo", "temecula", "irvine",  # irvine 已归 OC，这里只是兜底
]

_REMOTE = re.compile(r"\bremote\b|\banywhere\b|\bwork from home\b|\bwfh\b|\bdistributed\b|\bvirtual\b", re.I)
_NON_US = re.compile(
    r"\b(canada|toronto|vancouver|london|united kingdom|\buk\b|ireland|dublin|india|bangalore|bengaluru|"
    r"hyderabad|pune|singapore|hong kong|sydney|australia|germany|berlin|amsterdam|netherlands|poland|"
    r"mexico|brazil|philippines|kenya|nairobi|japan|tokyo|china|shanghai|beijing|israel|tel aviv|"
    r"france|paris|spain|lisbon|portugal|emea|apac|latam|europe)\b",
    re.I,
)
_US = re.compile(r"\b(us|u\.s\.|usa|united states|u\.s\.a\.|north america|americas)\b", re.I)
_CA_STATE = re.compile(r"(?:,|\s|-|^)(ca|california)(?:\b|$)", re.I)
# 明确写了「别的州」：用来排除 Glendale, AZ / Carson City, NV / Long Beach, NY 这类同名城市。
# 故意不收 or / in / me / hi / ok / de / la / id / al / co 这些同时是英文单词或有歧义的缩写。
_OTHER_STATE = re.compile(
    r"(?:,\s*|\bus-|\busa-)(ny|nj|tx|il|ma|wa|fl|ga|nc|va|pa|az|mn|mi|oh|ut|tn|md|dc|ct|ne|mo|wi|ky|sc|"
    r"ks|ar|nv|nm|nh|vt|mt|nd|wv|wy|ms|ri|ia|ak)\b"
    r"|\b(new york|new jersey|texas|illinois|massachusetts|florida|georgia|colorado|north carolina|"
    r"virginia|pennsylvania|arizona|oregon|minnesota|michigan|ohio|utah|tennessee|maryland|"
    r"connecticut|nevada|washington state|missouri|wisconsin|indiana|louisiana)\b",
    re.I,
)


def _contains_any(text: str, names: list[str]) -> bool:
    return any(re.search(r"\b" + re.escape(n) + r"\b", text) for n in names)


def classify_location(loc: str) -> set[str]:
    """把单个地点字符串分到区域集合（一个字符串可能同时写了多个城市）。"""
    s = (loc or "").strip().lower()
    if not s:
        return set()
    regions: set[str] = set()
    # 写了别的州、又没写 CA → 同名城市（Glendale, AZ）不算加州
    other_state_only = bool(_OTHER_STATE.search(s)) and not _CA_STATE.search(s)
    if not other_state_only:
        if _contains_any(s, OC_CITIES) or _ORANGE_CITY.search(s):
            regions.add("OC")
        if _contains_any(s, LA_CITIES) or _LA_ABBR.search(" " + s + " "):
            regions.add("LA")
        if _contains_any(s, SD_CITIES):
            regions.add("SD")
        if _contains_any(s, BAY_CITIES):
            regions.add("BAY")
    if _REMOTE.search(s):
        if _NON_US.search(s) and not _US.search(s):
            pass  # 例如 "Remote - Canada"：不算
        elif other_state_only and not _US.search(s):
            pass  # "Remote - Texas"：只招德州居民，不算
        else:
            regions.add("REMOTE_US")
    if not regions and not other_state_only and (_CA_STATE.search(s) or _contains_any(s, CA_OTHER_HINTS)):
        regions.add("CA_OTHER")  # 写了 California / CA，但城市不在列表里
    if not regions:
        regions.add("OTHER")
    return regions


def classify_locations(locations: list[str], remote: bool | None = None) -> list[str]:
    """一个职位的所有地点 → 区域列表（去掉 OTHER，除非只有 OTHER）。"""
    regions: set[str] = set()
    for loc in locations or []:
        regions |= classify_location(loc)
    if remote and not (regions - {"OTHER"}):
        # ATS 标了 remote 但地点字段是空的/只写了美国
        joined = " ".join(locations or []).lower()
        if not _NON_US.search(joined) or _US.search(joined):
            regions.add("REMOTE_US")
    useful = regions - {"OTHER"}
    return sorted(useful) if useful else sorted(regions)


def is_unresolved(locations: list[str]) -> bool:
    """Workday 常见的「2 Locations」/ Greenhouse 的「Multiple Locations」—— 需要看详情才知道。"""
    joined = " ".join(locations or []).lower()
    return bool(re.search(r"\b\d+\s+locations?\b|multiple locations|various locations", joined))
