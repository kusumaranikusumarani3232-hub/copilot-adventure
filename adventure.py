"""A text-based choose-your-own-adventure game with colored output and inventory.

Install Colorama before running:
    python -m pip install colorama
"""

from colorama import Fore, Style, init


# Reset styles automatically after each printed line. This also helps make
# colors work in Windows terminals.
init(autoreset=True)


STORY = {
    "start": {
        "text": (
            "You wake beneath a sky full of unfamiliar stars. "
            "A lantern glows beside a fork in the road."
        ),
        "choices": [
            {"text": "Follow the path into the forest", "next": "forest"},
            {"text": "Take the road toward the distant village", "next": "village"},
        ],
    },
    "forest": {
        "text": "The forest grows quiet. You find a hollow tree and a stone doorway.",
        "choices": [
            {
                "text": "Take the silver key from the hollow tree",
                "next": "crossroads",
                "gives": "silver key",
            },
            {
                "text": "Open the stone door with the silver key",
                "next": "treasure",
                "requires": "silver key",
            },
            {"text": "Follow a trail of lights", "next": "lights"},
        ],
    },
    "village": {
        "text": (
            "The village is dark, but a baker waves from a lit window. "
            "They offer you a warm loaf and a brass travel token."
        ),
        "choices": [
            {
                "text": "Accept the brass token",
                "next": "market",
                "gives": "brass token",
            },
            {"text": "Explore the old watchtower", "next": "tower"},
            {"text": "Head back to the forest", "next": "forest"},
        ],
    },
    "crossroads": {
        "text": "You reach a fork in the forest path. The stone doorway is nearby.",
        "choices": [
            {
                "text": "Unlock the stone door with the silver key",
                "next": "treasure",
                "requires": "silver key",
            },
            {"text": "Return to the forest path", "next": "forest"},
            {"text": "Follow a trail of lights", "next": "lights"},
        ],
    },
    "market": {
        "text": "At the village market, a ship is preparing to leave the harbor.",
        "choices": [
            {
                "text": "Use the brass token to board the ship",
                "next": "voyage",
                "requires": "brass token",
            },
            {"text": "Return to the village", "next": "village"},
        ],
    },
    "treasure": {
        "text": (
            "The key turns. Inside the stone room, you discover a treasure chest "
            "and a note naming you its new keeper."
        ),
        "choices": [],
    },
    "lights": {
        "text": (
            "The lights lead you to a hidden spring. You drink, feel your "
            "strength return, and find your way safely home."
        ),
        "choices": [],
    },
    "tower": {
        "text": (
            "At the top of the watchtower, you spot a ship waiting in the harbor. "
            "You sail away toward a new adventure."
        ),
        "choices": [],
    },
    "voyage": {
        "text": (
            "The token earns you a place aboard the ship. You set sail beneath "
            "the stars, bound for a distant shore."
        ),
        "choices": [],
    },
}


def show_banner():
    """Display the game's opening banner."""
    print(Fore.CYAN + Style.BRIGHT + "=" * 44)
    print(Fore.YELLOW + Style.BRIGHT + "        THE STARRY ROAD")
    print(Fore.CYAN + Style.BRIGHT + "=" * 44)
    print(Fore.WHITE + "A small adventure under unfamiliar stars.\n")


def available_choices(node, inventory):
    """Return choices whose required items are in the player's inventory."""
    return [
        choice
        for choice in node["choices"]
        if "requires" not in choice or choice["requires"] in inventory
    ]


def get_choice(options):
    """Prompt until the player enters a valid numbered choice."""
    while True:
        answer = input(Fore.YELLOW + "\nYour choice: ").strip()

        try:
            choice_number = int(answer)
        except ValueError:
            print(Fore.RED + "Please enter the number of one of the choices.")
            continue

        if 1 <= choice_number <= len(options):
            return choice_number - 1

        print(Fore.RED + f"Please choose a number from 1 to {len(options)}.")


def play():
    """Play from the beginning until an ending is reached."""
    current_node = "start"
    inventory = set()

    while True:
        node = STORY[current_node]
        print(Fore.WHITE + "\n" + node["text"])

        if inventory:
            items = ", ".join(sorted(inventory))
            print(Fore.GREEN + f"Inventory: {items}")
        else:
            print(Fore.GREEN + "Inventory: empty")

        options = available_choices(node, inventory)

        if not options:
            print(Fore.MAGENTA + Style.BRIGHT + "\nThe End!")
            return

        for number, choice in enumerate(options, start=1):
            print(Fore.CYAN + f"{number}. {choice['text']}")

        selected_choice = options[get_choice(options)]

        if "gives" in selected_choice:
            item = selected_choice["gives"]
            inventory.add(item)
            print(Fore.GREEN + Style.BRIGHT + f"\nYou picked up: {item}.")

        current_node = selected_choice["next"]


def main():
    """Show the banner and offer to restart after each playthrough."""
    show_banner()

    while True:
        play()

        while True:
            restart = input(
                Fore.YELLOW + "\nWould you like to play again? (y/n): "
            ).strip().lower()

            if restart in ("y", "yes"):
                print()
                break
            if restart in ("n", "no"):
                print(Fore.CYAN + "Thanks for playing!")
                return

            print(Fore.RED + "Please enter y or n.")


if __name__ == "__main__":
    main()
