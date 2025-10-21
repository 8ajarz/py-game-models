import init_django_orm  # noqa: F401
from json import load, JSONDecodeError

from db.models import Race, Skill, Player, Guild


def main() -> None:
    try:
        with open("players.json", "r") as file:
            data = load(file)
    except FileNotFoundError:
        print("Error: 'players.json' not found. Please create the file.")
    except JSONDecodeError:
        print("Error: Invalid JSON format in 'players.json'.")

    for entity, chars in data.items():
        players_race, _ = Race.objects.get_or_create(
            name=chars["race"]["name"],
            description=chars["race"]["description"]
        )
        for skill in chars["race"]["skills"]:
            Skill.objects.get_or_create(
                name=skill["name"],
                bonus=skill["bonus"],
                race=players_race
            )
        try:
            players_guild, _ = Guild.objects.get_or_create(
                name=chars["guild"]["name"],
                description=chars["guild"]["description"]
            )
        except TypeError:
            players_guild = None
        Player.objects.create(
            nickname=entity,
            email=chars["email"],
            bio=chars["bio"],
            race=players_race,
            guild=players_guild
        )


if __name__ == "__main__":
    main()
