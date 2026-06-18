import json
from NoIdeaGamePygame.Word.generationWord.GenerationWordMain import GenerationWord


class SaveWord:
    def __init__(self, word_name: str, *layer):
        self.word_name = f'../Word/SaveWord/{word_name}'
        self.data = None
        self.layer = [layer]

    def open_file_word(self):
        try:
            with open(self.word_name, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {
                "word": {
                    "position-all-layer": {},
                    "texture-layer": {},
                    "name": "defaultName",
                    "playerPosition": []
                }
            }
            with open(self.word_name, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        return self.data

    def save_word(self):
        for x in self.layer:
            print(self.layer, '---')
        self.open_file_word()
        print(self.data)



