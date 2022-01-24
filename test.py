# -*- coding: utf-8 -*-
import logging
import os
import shutil
import filecmp
import datetime
import time
import argparse


class Imagemaker:

    def __init__(self, source_folder, copy_folder, name_log, step):
        self.step = int(step)
        self.name_log = name_log
        logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(self.name_log, 'w', 'utf-8')], )
        self.source_folder = source_folder
        self.copy_folder = copy_folder

    def folder_search(self, folder, folder_check, action_name='copy'):
        path = os.path.dirname(__file__)
        path_source_folder = os.path.normpath(os.path.join(path, folder))
        path_copy_folder = os.path.normpath(os.path.join(path, folder_check))
        for dirpath, dirnames, filenames in os.walk(path_source_folder):
            if os.path.isdir(dirpath):
                folder_path = dirpath.split(f'{folder}')[-1]
                new_path = path_copy_folder + folder_path
                if not os.path.exists(new_path):
                    if action_name == 'copy':
                        """копируем из исходника папки в копию, только те которых нет"""
                        shutil.copytree(dirpath, new_path)
                        logging.info(f'копируем в: {self.copy_folder}, каталог: {folder_path}')
                    elif action_name == 'delete':
                        """удаляем из папки копии, папки которых нет в исходнике"""
                        shutil.rmtree(dirpath)
                        logging.info(f'удаляем из: {self.copy_folder}, каталог: {folder_path}')

            for filename in filenames:
                full_filename = os.path.join(dirpath, filename)
                if os.path.isfile(full_filename):
                    folder_path = full_filename.split(f'{folder}')[-1]
                    new_path = path_copy_folder + folder_path
                    if not os.path.exists(new_path) or not filecmp.cmp(full_filename, new_path):
                        if action_name == 'copy':
                            """копируем из исходника файлы в копию, только те которых нет"""
                            shutil.copy2(full_filename, new_path)
                            logging.info(f'копируем в: {self.copy_folder}, файл: {folder_path}')
                        elif action_name == 'delete':
                            """удаляем из папки копии, файлы которых нет в исходнике"""
                            os.remove(full_filename)
                            logging.info(f'удаляем из {self.copy_folder}, файл: {folder_path}')

    def run(self):
        logging.info(f'запуск программы - {datetime.datetime.now()}')
        while True:
            self.folder_search(folder=self.copy_folder, folder_check=self.source_folder, action_name='delete')
            self.folder_search(folder=self.source_folder, folder_check=self.copy_folder, action_name='copy')
            time.sleep(self.step)


def image_maker(source_folder, copy_folder, name_log, step):
    image = Imagemaker(source_folder=source_folder, copy_folder=copy_folder, name_log=name_log, step=step)
    image.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder')
    parser.add_argument('copy_folder')
    parser.add_argument('name_log')
    parser.add_argument('step')
    # args = parser.parse_args('source_folder copy_folder primes.log 5'.split())
    args = parser.parse_args()
    image_maker(args.source_folder, args.copy_folder, args.name_log, args.step)

