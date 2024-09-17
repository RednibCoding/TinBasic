import basic

while True:
    text = input("basic > ")
    result, err = basic.run("test.bas", text)

    if err:
        print(err)
    else:
        print(result)