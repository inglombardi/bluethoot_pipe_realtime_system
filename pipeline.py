"""

 @author:	Nicola	Lombardi	-	Hardware, Software and Firmware Engineer
 This	script	is	created	to	solve	a Coding Challenge

  =================================================================
 |	Author	of	the	Project	-	Engineer	Nicola	Lombardi	|
 =================================================================
 |	MSc.	in	Telecommunications	and	Internet	of	Things	|
 |	Telecommunications Engineering    	|	SW HW	ENGINEER	|

 |Professional	Profile
 |		it.linkedin.com/in/nicola-lombardi-09046b205
    The CALLED CODE (called by test_pipe.py)

    :DOCUMENTATION:
    This is a known issue. WSL does not handle named pipes (mkfifo) well, so my choice to use files as
    a workaround makes sense. An alternative solution would be to use /dev/shm/, which
    I have already tried, or to use socat to create a bridge between WSL and Linux.


Extracted from pipeline_called [bug fixing]:
    # It's a problem with WSL
    # input_pipe = "input_pipe.fifo"
    # output_pipe_aoa = "output_pipe_aoa.fifo"
    # output_pipe_filter = "output_pipe_filter.fifo"

    #input_pipe = "/dev/shm/input_pipe.fifo"
    #output_pipe_aoa = "/dev/shm/output_pipe_aoa.fifo"
    #output_pipe_filter = "/dev/shm/output_pipe_filter.fifo"

    #input_pipe = "/mnt/wsl/input_pipe.fifo"
    #output_pipe_aoa = "/mnt/wsl/output_pipe_aoa.fifo"
    #output_pipe_filter = "/mnt/wsl/output_pipe_filter.fifo"

_________
WORKFLOW:
_________

(1) Create named pipes (FIFO)

Create 2 pipes: one for aoa_to_1d and one for median_filter.py.
Start processes

(2) Compile and run aoa_to_1d.

Start median_filter.py with its parameters.
Data flow management

(3)
Read data from input.csv.
Write it to the pipe of aoa_to_1d.

(4)
Read the output of aoa_to_1d and pass it to the pipe of median_filter.py.

(5)
Write the final result to output.csv.
Shutdown and cleanup

Shut down all files and processes.
Delete named pipes.

"""
import pandas as pd
import os
import subprocess # to use the ubuntu cmd python3 bla_bla.py
import time
import logging
from constant import *
# from constant import USE_FILES, h_anchor



#  logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Boolean Path for pipes or filer [Dynamic Binding]
PIPE_INPUT = "input_pipe.txt" if USE_FILES else "input_pipe.fifo"
PIPE_AOA = "output_pipe_aoa.txt" if USE_FILES else "output_pipe_aoa.fifo"
PIPE_FILTER = "output_pipe_filter.txt" if USE_FILES else "output_pipe_filter.fifo"


def compile_c_program():
    """
    Compile aoa_to_1d.c in aoa_to_1d (executable in .exe).
    if it already exists, it's not a problem
    """
    c_file = "aoa_to_1d.c"   # MANDATORY !
    exe_file = "aoa_to_1d"

    if not os.path.exists(c_file):
        raise FileNotFoundError(f"File sorgente {c_file} non trovato!")

    logging.info("Compilation MIN GW with gcc command in WSL ...")
    result = subprocess.run(
        ["gcc", c_file, "-o", exe_file, "-lm"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logging.error(f"Error in  Compilation C:\n{result.stderr}")
        raise RuntimeError("Compilation failed !")
    else:
        logging.info("Compilation SUCCESSFUL")



def create_file(file_name):
    """ Single Responsibility Principle Function
    (I) Features: Version with files
    (II)Target: create an empty file if it doesn't exist
    :param file_name: file name to name the txt
    :return: NONE
    """
    if not os.path.exists(file_name):
        open(file_name, 'w').close()


def create_fifo(fifo_name):
    """ Single Responsibility Principle Function
    (I) Features: Version with pipes
    (II)Target: create an empty pipe
    :param fifo_name:
    :return: NONE
    """
    if not os.path.exists(fifo_name):
        os.mkfifo(fifo_name)


def create_channel(name):
    """ Single Responsibility Principle Function
    (I) Features: Create a channel
    (II)Target: create a pipe or file
    :param name: file or pipe name
    :return: NONE
    """
    if not USE_FILES:
        create_fifo(fifo_name=name)
    else:
        create_file(file_name=name)



def cleanup_files():
    """ Single Responsibility Principle Function
    (I) Features:
    (II)Target: Remove  files/pipes from  execution
    :param: NONE
    :return: NONE
    """
    for file in [PIPE_INPUT, PIPE_AOA, PIPE_FILTER, OUTPUT_CSV, EXPECTED_CSV]:
        if os.path.exists(file):
            os.remove(file)

def stream_input_to_pipe():
    """ Single Responsibility Principle Function
    (I) Features: modularity write -> flush -> sleep
    (II)Target: Remove  files/pipes from  execution
    :param: NONE
    :return: NONE
    """
    with open(INPUT_CSV, "r") as infile, open(PIPE_INPUT, "w") as pipe:
        for line in infile:
            pipe.write(line)
            pipe.flush()
            time.sleep(timing)

def pipeline_called():
    """
    (I) Features: Pipeline orchestrator
    (II)Target: Method to create the pipe or file based on the flag

    Writes input.csv to input_pipe.txt before running the aoa_to_1d process.
    Waits for aoa_to_1d to finish before running median_filter.py.
    Waits for median_filter.py to finish before writing output.csv.


    aoa_to_1d : Preprocessing step 1
    :return: NONE
    """
    logging.info("[START THE PREPROCESSING]...")

    try:
        compile_c_program()

        # Simulate data streaming from input.csv to input_pipe.txt
        # Remember this code does not deal the EXCEL opened exception
        for pipe in [PIPE_INPUT, PIPE_AOA, PIPE_FILTER]:
            create_channel(pipe)
        # ---------------------------------------------------------------------------
        # Racking the csv content
        with open("input.csv", "r") as infile, open(PIPE_INPUT, "w") as pipe_in:
            for line in infile:
                pipe_in.write(line)
                pipe_in.flush()
                time.sleep(timing)  # Networking stream simulation 10 milliseconds
        # ---------------------------------------------------------------------------

        logging.info("PREPROCESSING PHASE 1 (USE BASH PROGRAMMING SYNTAX)...")
	    # COUPLING with if (argc != 4) { fprintf(stderr, "Usage: %s <input_pipe> <output_pipe> <h_anchor>\n", argv[0]);
        aoa_proc = subprocess.Popen(["./aoa_to_1d", PIPE_INPUT, PIPE_AOA, h_anchor])

        # Simulation of the WAIT(0)
        # Wait for the first process to finish before proceeding
        aoa_proc.wait()

        logging.info("PREPROCESSING PHASE 2 (USE THE LINUX CMD WITH PYTHON 3.12)...")
        # Remember : Usage syntax in Linux -> python median_filter.py <input_pipe> <output_pipe> [time_window_ms]
        filter_proc = subprocess.Popen(["python3", "median_filter.py",
                                        PIPE_AOA, PIPE_FILTER])
        filter_proc.wait()

        # test with the code from https://docs.python.org/3/library/subprocess.html
        if aoa_proc.returncode != 0 or filter_proc.returncode != 0:
            logging.error("[FAULT THE PROCESSING]...Data Analysis Error!")

        # example
        # subprocess.run(["ls", "-l"])  # doesn't capture output
        # CompletedProcess(args=['ls', '-l'], returncode=0)


        with open(PIPE_FILTER, "r") as filter_out, open("output.csv", "w") as final_out:
            final_out.writelines(filter_out.readlines())

        # here the succesful could be displayed
        logging.info("[FINISH THE PREPROCESSING]...Processing COMPLETED ")

        aoa_proc.terminate()
        filter_proc.terminate()

    finally:

        # In C the memory management is dealt by programmer
        # os.remove(input_pipe)
        # os.remove(output_pipe_aoa)
        # os.remove(output_pipe_filter)
        for file in [PIPE_INPUT, PIPE_AOA, PIPE_FILTER]:
            if os.path.exists(file):
                os.remove(file)


if __name__ == "__main__":
    pipeline_called()
