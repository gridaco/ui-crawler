import pathlib
import json

current_dir: pathlib.PurePath = pathlib.Path(__file__).parent

google_credentials_file = "./google_browser_login_credentials.json"
google_credentials_file = current_dir.joinpath(google_credentials_file)
print(google_credentials_file)


def load_google_credentials():
    with open(str(google_credentials_file)) as f:
        data = json.load(f)

    return {"ID": data["ID"], "PW": data["PW"]}




def test():
    c = load_google_credentials()
    print(c)



if __name__ == '__main__':
    test()
