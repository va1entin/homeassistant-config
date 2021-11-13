#!/usr/bin/env python3

# shell_command.yaml:
# wakeup_light_call: /config/scripts/fade_in_light.py -k {{ states('input_text.deconz_api_key') }} -p {{ states('input_number.deconz_port') | int }} -g "{{ state_attr('light.bedroom', 'friendly_name') }}" -b {{ states('input_number.wakeup_final_brightness') | int }} -t {{ states('input_number.wakeup_duration') | int }}


import argparse
import requests


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--group', help='deCONZ group name', required=True)
    parser.add_argument('-b', '--brightness', help='Brightness level', type=int, required=True)
    parser.add_argument('-t', '--time', help="Transition time in minutes", type=int, required=True)
    parser.add_argument('-p', '--port', help="deCONZ port", type=int, required=True)
    parser.add_argument('-k', '--api-key', help="API key", required=True)
    parser.add_argument('-H', '--host', help="deCONZ host", default="localhost")
    args = parser.parse_args()
    return args


def main(args):
    response = requests.get(f'http://{args.host}:{args.port}/api/{args.api_key}/groups')
    groups = response.json()

    for group_id, group in groups.items():
        if group['name'] == args.group:
            my_id = group_id

    time = args.time * 60 * 10

    requests.put(f'http://{args.host}:{args.port}/api/{args.api_key}/groups/{my_id}/action', data=f'{{"on": true, "bri": {args.brightness}, "transitiontime": {time}}}')


if __name__ == "__main__":
    args = setup_parser()
    main(args)
