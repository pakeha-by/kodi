import re
import base64
import helpers
from operator import itemgetter

BK_SEP = '//_//'
BK_BLOCKS = [
    'JCQhIUAkJEBeIUAjJCRA',
    'QEBAQEAhIyMhXl5e',
    'IyMjI14hISMjIUBA',
    'Xl5eIUAjIyEhIyM=',
    'JCQjISFAIyFAIyM='
]


def parse_streams(salted):
    origin = salted
    try:
        salted = salted.replace('\\', '')
        for bk in BK_BLOCKS:
            salted = salted.replace(BK_SEP + bk, '')

        helpers.log('Stripped salted string')
        helpers.log(salted)
        decoded_streams = base64.b64decode(salted[2:]).decode('utf-8')

    except Exception as e:
        decoded_streams = origin

    parsed_streams = []
    for name, quality, url in re.findall(r'\[((\d+)[^]]+)].+?(http.+?mp4)', decoded_streams):
        parsed_streams.append((
            name, int(quality), url
        ))
    return sorted(parsed_streams, key=itemgetter(1), reverse=True)
