from benedict.core.engine import Engine

if __name__ == "__main__":
    engine = Engine()
    while True:
        msg = input("< ")
        result = engine.handle_message({"text": msg})
        print("> {}".format(result))