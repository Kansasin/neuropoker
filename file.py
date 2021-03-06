import json
import os

class File:
    @staticmethod
    def save_settings(game, train_settings):
        with open('./game_settings.json', 'w+') as f: f.write(json.dumps(game.SAVABLE))
        with open('./train_settings.json', 'w+') as f: f.write(json.dumps(train_settings.SAVABLE))

    @staticmethod
    def load_settings(game, train_settings):
        if os.path.exists('./game_settings.json'):
            with open('./game_settings.json', 'r') as f:
                for key, value in json.loads(f.read()).items():
                    game.SAVABLE[key] = value
        if os.path.exists('./train_settings.json'):
            with open('./train_settings.json', 'r') as f:
                for key, value in json.loads(f.read()).items():
                    train_settings.SAVABLE[key] = value

    @staticmethod
    def save_brains(train_settings):
        with open(train_settings.SAVABLE['IMPORT_PATH'], 'w+') as f: f.write(json.dumps(train_settings.SAVABLE['BEST_BRAINS']))

    @staticmethod
    def load_brains(train_settings):
        if os.path.exists(train_settings.SAVABLE['EXPORT_PATH']):
            with open(train_settings.SAVABLE['EXPORT_PATH'], 'r') as f:
                train_settings.SAVABLE['BEST_BRAINS'] = json.loads(f.read())
