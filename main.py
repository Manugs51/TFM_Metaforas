from secrets import secrets

def get_text() -> str:
    return input()

def find_metaphors(text: str) -> str:
    return text

def show_metaphors(text:str) -> None:
    print(text)
    pass

if __name__ == '__main__':
    while True:
        text = get_text()
        metaphors_found = find_metaphors(text)
        show_metaphors(metaphors_found)
