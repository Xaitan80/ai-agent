
fish_data = {
    "salmon": "A fish that is born in freshwater and migrates to the ocean, then returns to freshwater to reproduce.",
    "tuna": "A saltwater fish that is an important food source.",
    "cod": "A popular fish often used in fish and chips.",
}

def get_fish_definition(fish_name):
    if fish_name in fish_data:
        return fish_data[fish_name]
    else:
        return "Definition not found."

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        fish_name = sys.argv[1]
        definition = get_fish_definition(fish_name)
        print(definition)
    else:
        print("Please provide a fish name as an argument.")
