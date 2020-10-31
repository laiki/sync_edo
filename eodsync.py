#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:26:48 2020

@author: wgo
"""
import os, sys, argparse, logging, time
from trains import Task
from autologging import traced, TRACE


@traced
class EODSync:
    def __init__(self, project_name='EODData synchronizer'):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-v', '--verbose',
            dest='verbose',
            type=int,
            help='increase output verbosity, defaults to 1',
            default=1)
        self.parser.add_argument(
            '-s', '--server',
            dest='server',
            type=str,
            help='ftp server to get data, defaults to ftp.eod.com',
            default='ftp.eoddata.com')
        self.parser.add_argument(
            '-P', '--directory-prefix',
            dest='directory_prefix',
            type=str,
            help='output directory to sync files to, defaults to ./result/ftp.eod.com/',
            default='./result/ftp.eoddata.com/')
        self.parser.add_argument('-u', '--user',
                                 dest='user',
                                 type=str,
                                 help='ftp user name, defaults to laiki',
                                 default='laiki')
        self.parser.add_argument('-p', '--password',
                                 dest='password',
                                 type=str,
                                 help='password of ftp user',
                                 default=None)
        self.parser.add_argument(
            '--use-trains',
            dest='use_trains',
            action='store_true',
            help='enables the use of a Trains task',
            default=False)
        self.parser.add_argument(
            '--use-tracing',
            dest='use_tracing',
            action='store_true',
            help='enables tracing almost all function calls',
            default=False)
        
        self.args = self.parser.parse_args()
        if self.args.verbose:
            print('processing:', self.args)

        if True == self.args.use_tracing:
            logging.basicConfig(level=TRACE, stream=sys.stdout, 
                                format="%(levelname)s:%(funcName)s")

        if self.args.use_trains:
            self.task = Task.init(
                project_name=project_name,
                task_name='wget sync',
                task_type='custom',
                reuse_last_task_id=True,
                output_uri='result')
        
        if None == self.args.password:
            print('Please define password!')
            self.parser.print_help()
            sys.exit(1)


        if not os.path.exists(self.args.directory_prefix):
            os.makedirs(self.args.directory_prefix)

        
    def start(self):
        start_time = time.process_time()
        ret = 0
        
        cmd = f'wget -m ftp://{self.args.user}@{self.args.server} \
            --password=\'{self.args.password}\' \
                --directory-prefix={self.args.directory_prefix}'
        if 2 <= self.args.verbose: print('calling', cmd)
        ret = os.system(cmd)

        if self.args.verbose:
            print(
                f'Time ellapse: {round(time.process_time() - start_time, 2)}sec'
            )
        
        return ret



#%%


def main():
    sync = EODSync()
    ret = sync.start()
    return ret


#%%
if __name__ == '__main__':
    main()



