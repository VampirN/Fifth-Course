from class_dbmanager import DBManager
import config


def main():
    params = config()
    bd = DBManager(**params)


if __name__ == "__main__":
    main()
