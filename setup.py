from cx_Freeze import setup, Executable

setup(
    name="Solitario",
    version = "1.0",
    description = "Trabajo Práctico Final - Arano, Portillo, Prieto, Zinni",
    options={"build_exe":{"packages":["pygame", "random"],
                        "include_files":["background.jpg","flip.wav", "shuffle.wav", "PlayingCards"]}},
    executables = [Executable("Game.py"), Executable("Card.py"), Executable("Deck.py"), Executable("Foundation.py"), Executable("Table.py"), Executable("Waste.py")]
    )
#"excludes": ["tkinter"],
