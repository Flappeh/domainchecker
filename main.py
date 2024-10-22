import whois 
import multiprocessing
from modules.utils import get_logger
from typing import List
import random
import string
import numpy as np
import os

PROC_COUNT = 5
logger = get_logger()


def store_error_log(err):
    with open("data/error.log", 'a') as f:
        f.write(err)

def open_file():
    domain = []
    try:
        logger.info("Getting data from domains.txt file")
        with open(file='data/domains.txt',mode='r',encoding='utf8') as f:
            count = 0
            for i in f:
                # if count > 100:
                #     break
                if i == "" or i == None:
                    continue
                data = i.rstrip()
                count += 1
                domain.append(data)
        return domain
    except Exception as e:
        logger.error("Error opening domains.txt file")
        store_error_log(e)
        raise

def check_domain_job(list):
    availabile = []
    unavailabile = []
    total = 0
    for i in list:
        try:
            for x in range(3):
                try:
                    info = whois.whois(i)
                    logger.info(f"Domain : {i} UNAVAILABLE")
                    unavailabile.append(i)
                    break
                except Exception as e:
                    if x == 2:
                        raise
                    pass
        except Exception as e:
            # logger.error(f"Error on looking up : {i}\n Details: {e}")
            logger.debug(f"Domain : {i} AVAILABILE")
            availabile.append(i)
        try:
            total += 1
            if total == 5:
                total = 0
                store_results(unavailabile, availabile)
                availabile, unavailabile = [], []
        except:
            logger.error("Error storing data file")
    store_results(unavailabile, availabile)
def split_chunks(list,n):
    return np.array_split(list, n)


def start_parsing_process():
    taken = []
    process_list = []
    availabile = []
    try:
        # Start opening input file
        # manager = multiprocessing.Manager()
        # results = manager.dict()
        # results['availabile'] = []
        # results['taken'] = []
        
        domain_list = open_file()
        if len(domain_list) < PROC_COUNT:
            data_chunks = domain_list
        else:
            data_chunks = split_chunks(domain_list,PROC_COUNT)
        for i in data_chunks:
            proc = multiprocessing.Process(target=check_domain_job, args=(i,))
            process_list.append(proc)
            proc.start()
            
        for i in process_list:
            i.join()
        # for i in results:
        #     if 'taken-' in i:
        #         taken.append(results[i])
        #     if 'availabile-' in i:
        #         availabile.append(results[i])

    except:
        logger.error("Error occured on parsing process")
        pass
    finally:
        logger.info("Finished parsing process")
        # store_results(taken, availabile)
        
def store_results(taken, availabile):
    with open('data/unavailabile.txt', 'a') as f:
        for i in taken:
            f.write(i + '\n')
    with open('data/availabile.txt', 'a') as f:
        for i in availabile:
            f.write(i + '\n')
        
def remove_old_files():
    if os.path.exists('./data/unavailabile.txt'):
        os.remove('./data/unavailabile.txt')
    if os.path.exists('./data/availabile.txt'):
        os.remove('./data/availabile.txt')
    
if __name__ == "__main__":
    multiprocessing.freeze_support()
    # if sys.platform.startswith('win'):
    #     # On Windows calling this function is necessary.
    logger.info("Initializing application")
    remove_old_files()
    start_parsing_process()
    
    logger.info("Done processing domains list")