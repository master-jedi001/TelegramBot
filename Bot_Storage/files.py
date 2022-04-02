from os import stat, path
import re
import json


regex_title = re.compile(r'^.*?\.[A-Za-z]{1,4}$')


class File:

    def __init__(self, file_id, title, caption):
        self.__file_id = file_id
        self.title = title
        self.caption = caption

    def __dict__(self):
        return {'file_id': self.__file_id, 'title': self.title, 'caption': self.caption}

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        if re.fullmatch(regex_title, title):
            self.__title = title
        else:
            raise ValueError('Invalid title')

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    def caption(self, caption):
        self.__caption = caption

    def get_file_id(self):
        return self.__file_id

    def add_file(self, chat_id):
        file = str(chat_id) + '_files.json'
        if not path.exists(file):
            files_list = list()
        elif stat(file).st_size == 0:
            files_list = list()
        else:
            files_list = json.load(open(file))
        files_list.append(self.__dict__())
        data_base_files = open(file, 'w+')
        json.dump(files_list, data_base_files, ensure_ascii=False)
        data_base_files.close()
        return f'Файл {self.title} успешно загружен.'

    def delete_file(self, chat_id):
        file = str(chat_id) + '_files.json'
        files_list = json.load(open(file))
        files_list.remove(self.__dict__())
        data_base_files = open(file, 'w+')
        json.dump(files_list, data_base_files, ensure_ascii=False)
        data_base_files.close()
        return f'Файл {self.title} успешно удален.'

    @staticmethod
    def get_files_list(chat_id):
        file = str(chat_id) + '_files.json'
        try:
            data_base_files = open(file, 'r')
            if stat(file).st_size == 0:
                files_list = list()
            else:
                files_list = json.load(data_base_files)
            data_base_files.close()
            return files_list
        except FileNotFoundError:
            return list()


class Class(File):
    def __init__(self, my_dict):
        field_1 = my_dict.get('file_id')
        field_2 = my_dict.get('title')
        field_3 = my_dict.get('caption')
        super().__init__(field_1, field_2, field_3)
