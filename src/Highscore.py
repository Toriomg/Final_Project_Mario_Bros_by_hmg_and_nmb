import fileinput
import Constants as c
from mario_module import Mario


class highscore:
    def __init__(self):
        self.__highsc = []
        self.__list = [0]
        self.__score = 0
        self.__updated = False
        for line in fileinput.input(files=c.Highscores_path):
            self.__highsc.append(int(line.strip()))

    @property
    def list(self) -> list:
        return self.__list

    @list.setter
    def list(self, new_highscore):
        self.__list = new_highscore

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, new_score):
        if type(new_score) != int:
            raise ValueError('Punctuation must be an integer')
        elif not new_score >= 0:
            raise ValueError('Punctuation must be positive')
        elif new_score > c.max_punctuation:
            self.__score = c.max_punctuation
        else:
            self.__score = new_score

    def sort_highscore(self):
        """The list of the scores is sorted, so the highscore is placed into the top.
         It must be placed into the update part"""
        self.__list.clear()
        self.__list = self.__highsc.copy()
        self.__list.append(self.__score)
        n = len(self.__list)
        for i in range(n - 1):  # Bubble sort
            for j in range(0, n - i - 1):
                # Swap if the element found is greater than the next element
                if self.__list[j] < self.__list[j + 1]:
                    self.__list[j], self.__list[j + 1] = self.__list[j + 1], self.__list[j]


    def write_score(self):
        """The score of the game is written into the .txt so the value is saved"""
        if not self.__updated:
            open(c.Highscores_path, 'a').write(f"{self.__score}\n")
            self.__updated = True
