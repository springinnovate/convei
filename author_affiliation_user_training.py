"""Track author affiliation by topic."""
import argparse
import os
import random
import secrets

import keyboard

CHOICES = {
    'u': 'university',
    'r': 'research',
    'p': 'practice',
}


def print_choices(affiliation):
    print('choose:\n\t' + '\n\t'.join([f'{key}: {classification_id}' for key, classification_id in CHOICES.items()]))
    print('"ESC" to quit')
    print('\n' + affiliation)


def process_key(context, classification_file, affiliation_list):
    def _process_key(event):
        print(event)
        choice = event.name
        if choice in CHOICES:
            classification_file.write(f'{CHOICES[choice]}: {context["affiliation"]}\n')
            context['affiliation'] = affiliation_list[random.randrange(len(affiliation_list))]
            context['count'] += 1
            os.system('cls')
            if context['count'] > 0:
                print(f'great job, you have classified {context["count"]} affiliations so far!')
            print_choices(context['affiliation'])
        else:
            print(f'!ERROR, unknown choice "{choice}" try again!\n')
    return _process_key


def main():
    parser = argparse.ArgumentParser(description='Train affilition classifier')
    parser.add_argument('affiliation_file', help='Path to affiliation list')
    args = parser.parse_args()

    with open(args.affiliation_file, 'r', encoding='utf-8') as file:
        affiliation_list = file.read().rstrip().split('\n')

    classified_filename = f'classified_{os.path.basename(os.path.splitext(args.affiliation_file)[0])}_{secrets.token_urlsafe(10)}.txt'
    with open(classified_filename, 'w', encoding='utf-8') as classification_file:
        affiliation = affiliation_list[random.randrange(len(affiliation_list))]
        context = {
            'affiliation': affiliation,
            'count': 0,
        }
        os.system('cls')
        print_choices(affiliation)
        keyboard.on_press(process_key(context, classification_file, affiliation_list))
        keyboard.wait('esc')
        keyboard.unhook_all()
        print(f'classifications in {classified_filename}')

if __name__ == '__main__':
    main()
