def get_auth():
    if check_storage():
        return read_config()
    else:
        build_config()
        return get_auth()


def check_storage():
    try:
        f = open('config', 'r')
        f.close()
    except IOError:
        return False
    return True


def read_config():
    f = open('config', 'r')
    name = f.readline()
    password = f.readline()
    f.close()
    return {
        'name': name,
        'pass': password
    }


def build_config():
    auth = enter_id_pass()
    f = open('config', 'w')
    f.write(auth['name'] + '\n')
    f.write(auth['pass'])
    f.close()


def enter_id_pass():
    name = input("请输入学号")
    password = input("请输入校园网密码")
    return {
        'name': name,
        'pass': password
    }
