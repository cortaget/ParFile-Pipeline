


def append_jecna_postfix(name):
    name += '@spsejecna.cz'
    return name
def append_seznam_postfix(name):
    name += '@seznam.cz'
    return name

def create_email(appender_function, username):
    print(appender_function(username))
    return appender_function(username)

if __name__ == '__main__':
    appender_postfix = append_jecna_postfix
    create_email(appender_postfix, "novak")
    # ma vratit novak@spsejecna.cz
    appender_postfix = append_seznam_postfix
    create_email(appender_postfix, "novak")
    # ma vratit novak@seznam.cz
