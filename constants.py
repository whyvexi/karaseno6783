from dataclasses import dataclass


@dataclass(frozen=True)
class Tariff:
    id: str
    name: str
    days: int
    price_rub: int
    price_stars: int
    price_usdt: float


TARIFFS: list[Tariff] = [
    Tariff(id="sprint", name="Спринт", days=7,
           price_rub=199, price_stars=130, price_usdt=2.2),
    Tariff(id="pro", name="Месячный Pro", days=30,
           price_rub=499, price_stars=320, price_usdt=5.5),
    Tariff(id="semester", name="Семестр", days=90,
           price_rub=999, price_stars=650, price_usdt=11.0),
]

TARIFFS_BY_ID: dict[str, Tariff] = {t.id: t for t in TARIFFS}


@dataclass(frozen=True)
class SubjectDef:
    id: int
    name: str
    slug: str
    emoji: str


SUBJECTS: list[SubjectDef] = [
    SubjectDef(id=1, name="Программирование Python", slug="python", emoji="🐍"),
    SubjectDef(id=2, name="Базы данных SQL", slug="sql", emoji="🗄️"),
    SubjectDef(id=3, name="Веб-разработка", slug="web", emoji="🌐"),
]

SUBJECTS_BY_ID: dict[int, SubjectDef] = {s.id: s for s in SUBJECTS}
SUBJECTS_BY_SLUG: dict[str, SubjectDef] = {s.slug: s for s in SUBJECTS}
