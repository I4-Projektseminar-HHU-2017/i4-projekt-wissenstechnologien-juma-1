import asyncio

from src.const import BASE_URL

from src.urlhook import UrlHook


class RunCmd:

    def __init__(self):
        command = str(input("Enter test command (use !help to see commands): "))
        loop = asyncio.get_event_loop()

        if command == "!help":
            print("!help\n!ping <url> (e.g. !ping " + BASE_URL + ")")

        elif command.startswith("!ping"):
            hook = UrlHook(urls=command.split(" ")[1])
            print(str(loop.run_until_complete(hook.make_soup())))

if __name__ == "__main__":
    cmd = RunCmd()
