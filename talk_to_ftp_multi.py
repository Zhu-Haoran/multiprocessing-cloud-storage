import os
from ftplib import FTP
from logger import Logger
from multiprocessing import Pool
from talk_to_ftp import TalkToFTP

class TalkToFTPMulti(TalkToFTP):

    def __init__(self, ftp_website, pool):
        TalkToFTP.__init__(self, ftp_website)
        self.pool = pool

    def file_transfer_multi(self, path, srv_path, file_name):
        self.pool.apply_async(self.file_transfer(path, srv_path, file_name))
        Logger.log_info("File created / updated : srv {0} file {1}".format(srv_path, file_name ))

    def create_folder_multi(self, folder):
        self.pool.apply_async(self.ftp.mkd(folder))
        Logger.log_info("Folder created : " + folder)

    def remove_folder_multi(self, folder):
        self.pool.apply_async(self.ftp.rmd(folder))
        Logger.log_info("Folder removed : " + folder)

    def remove_file_multi(self, file):
        self.pool.apply_async(self.ftp.delete(file))
        Logger.log_info("File removed : %s" + file)
