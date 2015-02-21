#!/usr/bin/env python2
import snapext, os
handler = snapext.SnapHandler

data = dict()

@handler.route('/')
def main():
    return 'Ich bin online!'

@handler.route('/check')
def key_in_data(key):
    return key in data

@handler.route('/get')
def get_data(key):
    return data[key] if key_in_data(key) else ''

@handler.route('/put')
def set_data(key, value):
    data[key] = value

@handler.route('/list')
def list_data():
    return '\n'.join(data.keys())

@handler.route('/bye')
def shutdown():
    with open('data', 'w+') as _:
        _.write(str(data))
    exit(1)
    #os.system('shutdown -hP now')

if __name__ == '__main__':
    if os.path.isfile('data'):
        with open('data') as _:
            s = _.read()
            try:
                data = eval(_.read())
            except:
                pass

    snapext.main(handler, 80)
