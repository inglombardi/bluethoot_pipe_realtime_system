# Bluethoot_pipe_realtime_system creation, management, optimization and discussion by Nicola Lombardi
READ THE LICENCE TO AVOID LEGAL PROBLEM

____________________________________
Request to me to share this project.
____________________________________




Author Nicola Lombardi, SW HW Engineer
Computer and Telecommunications Engineer & Senior Python Dev.
DATE: February 2025
NAME OF THE PROJECT: REAL TIME BLE TRACKER SYSTEM


# [1] CONTEXT of the PROJECT : Real-Time 1D Position Tracking Using Named Pipes in a Bluethoot LOW ENERGY Scenario with different cows.

A company request me to design an **automated system** with innovation and a scalable approach.

Here is shown only a **DEMO** of my software but it's not OPEN source.


The high **UHF** band contains ISM band [ particular sub-band centered on 2.4 GHz] and has similar characteristics to the medium UHF band, but allows a further reduction in the size of the antenna and therefore of the Tag (due to the link between the size of the antenna and the wavelength). However, it is a band very crowded with other technologies (Wi-Fi, Bluetooth, ZigBee).
The specific frequency taken into consideration for the simulations is 2.45 GHz, and it is the central one for the ISM band that goes from 2.4 GHz to 2.5 GHz. The acronym ISM stands for “Industrial, Scientific and Medical” and refers to the type of applications that work in that specific spectrum with limitations regarding power and use only in non-public places: some examples of applications in the industrial field can be heaters, by induction or microwave for the treatment of plastic material. In the medical field, however, there are devices for the transfer of heat inside tissues, both with the aim of regenerating them from trauma (Tecar) and to try to eliminate cancer cells. There are also other applications, which however do not fall within the literal definition of ISM, such as for example Bluetooth, NFC, RFID, WiFi; the latter are all low-power, short-range and therefore usable without a license, but still operate within the band between 2.4 GHz and 2.5 GHz. From an ethical point of view, considering for example the medical field, for a patient to own a bone implant can be seen as discrimination, as he is denied the possibility of benefiting from a treatment, perhaps the only possible one, just because of a foreign body.

## Project Description

This project implements a "real-time data processing pipeline" to track (TRACKER SYSTEM) the 1D position of a cow equipped with a Bluetooth tag. The pipeline connects multiple components via **Linux named pipes (FIFOs)** and manages the flow of data from raw measurements to a filtered output.

The underlying application is the real-time tracking of a cow’s position, in one dimension only: the cow is wearing a Bluetooth tag (yellow tag in the picture below) 
which acts as a Bluetooth beacon, broadcasting packets; a Bluetooth anchor is  mounted in a fixed position and it computes the angle of arrival α for each Bluetooth transmission from the tag.

The cow transmits Bluetooth packets through a tag; a fixed anchor receives these transmissions and computes their **Angle of Arrival (AoA)**. By knowing both the anchor's and tag's height, and after applying filtering to smooth the data, the system computes the 1D position of the cow in real time.


A system described in this scenario must be able to handle several elements:
- the storage system must be reliable and fast.
- the data must be subjected to previously tested and validated data cleaning procedures, since the "Anchor" module could calculate coordinates based on angles that make no sense, for example, with incorrect signs or anomalous values, or abrupt variations that the cow cannot have.
- the system needs to receive and analyze the data, but cattle are diverse, so coordinates need to be distinguished using an ID tag. Each animal can be equipped with an RFID tag containing a unique identification number.
- For conversion operations, maximum processing speed is required.
- For data analysis, a semi-structured data type and an appropriate data cleaning algorithm must be used.
- Process 1 (P1 - PreProcessing Phase 1) must be coordinated with the communication opening.
- Process 2 (P2 - PreProcessing Phase 2) must be coordinated with process P1, which will pass the data to it using a data structure that is not a text file or other data structure that increases latency.
- The system must be controlled by an additional process that creates and tests the pipeline, continuously verifying its correct functioning. All situations in which anomalous behavior occurs must be defined.
 
In order to improve the system, it definetively must have:
a controller unit that build and test the pipeline in order to follow all test plan phases ==> this implies to write a test_pipe.py
a stochastic communication protocol ( an adaptive ALOHA collision–arbitration algorithm ) to deal data collisions using solution from literature ==> this implies to modify pipeline.py
an extended "anchor" module with 3D geometry using real data in x, y and z coordinates --> this implies to modify aoa_to_1d.c


## Project Analysis and Specifications
The primary goal of this project is to develop a real-time position tracking system for livestock (specifically cows) using Bluetooth Low Energy (BLE) technology. The system is designed to estimate the 1D position of a tagged cow by computing the Angle of Arrival (AoA) of BLE signals. This estimation is refined using signal preprocessing and filtering techniques. The project architecture prioritizes scalability, low-latency, and modularity, and is implemented using a hybrid software stack: C for real-time signal transformation and Python for data orchestration and filtering.

The overall system is designed to be automated, maintainable, and easily testable, with a strong emphasis on data integrity and inter-process communication (IPC) via Linux named pipes (FIFOs).

The architecture supports horizontal scaling, where additional anchors and tag IDs can be added with minimal code changes. The use of named pipes ensures modularity, making it easy to plug in additional filters or transform stages. This design anticipates integration into edge computing platforms or cloud-streaming pipelines with real-time analytics.

The system assumes a Linux-based environment (native or via WSL).

Input data is expected to be mostly well-formed; malformed lines are ignored without crashing.

The AoA → 1D mapping relies on fixed anchor height and BLE tag height.

Real-time behavior is emulated using CSV input streams but designed for hardware integration.

The project does not strictly follow SOLID or OOP patterns due to the procedural nature of the real-time processing.

The system MUST includes:

1. Error handling for missing or malformed input data.

2. Automated cleanup of temporary files and processes.

3. A comprehensive test suite with test cases covering: Named pipe creation, Data integrity across pipes, Output correctness, Performance on large datasets, Robustness under malformed or concurrent input scenarios



## Data Source

input.csv : input samples of the Data Processor ---> Not Available (NDA)
output.csv : output filtered samples of the Data Processor ---> Not Available (NDA)
expected_output.csv : expected output samples of the Data Processor ---> Not Available (NDA)

## Acronym
NDA = Non Disclosure Agreement 
BLE = Bluethoot Low Energy
TC = Test Case


# [2] My PROJECT IMPLEMENTATION: Global Solution
In this README.md I show a global solution of SOFTWARE DESIGN AND TESTING FOR QUALITY ASSURANCE with:

1. workflow in a Single Responsibility Principle Overview (for each phase) (see section #2, this section)
2. technologies chosen for this project  (see section #3)
3. software modules and coupling architecture (dependency) (see section #7)
4. Test plan and test cases to test this global system (see section #4)
5. Comment about source code (NOT OPEN SOURCE, but you must request me to share it)  (see section #5, #6, #7 and #8)
6. Pills about Linux and Programming languages  (see section #9 and #10)


______________________________________
The workflow is composed by 5 phases:
______________________________________

1. **CREATION PHASE** - Creates Linux named pipes, to facilitate communication between the 
components. 
2. **PREPROCESSING PHASE** - Starts the Preprocessing with aoa_to_1d and median_filter.py processes, ensuring they read 
from and write to the correct pipes.
aoa_to_1d.c receives pipes from Python script (pipeline.py) that is the called by test_pipe.

**==>** aoa_to_1d: A C program that converts the angle to a 1D position.
Note that: you must see the document --->  pandas_insight/README__median_filter_algorithm.pdf

**==>** median_filter.py: A Python script that filters the data using the median.
Note that: you must see the document --->  pandas_insight/README__median_filter_algorithm.pdf


3. **I / O PHASE** - Reads input data from input.csv, writes it to the aoa_to_1d input pipe, and 
ensures the process is properly notified when input is finished. 
4. **POSTPROCESSING PHASE** Reads the final filtered output from median_filter.py and writes it to an 
output CSV file (output.csv). 
5. **FLUSH PHASE** - Handles process cleanup and removes the named pipes after execution.


## Work planning to follow (not the runtime but the code writing before testing)

________________________________________
1. Creating named pipes (FIFO)  [Python]
________________________________________

Create 2 pipes: one for aoa_to_1d and one for median_filter.py.

________________________________________
2. Starting processes with Python
________________________________________
Compile and run aoa_to_1d. [C language with GCC using Ubuntu shell with WSL]

Start median_filter.py with its parameters.
________________________________________
3. Data flow management
________________________________________

Read data from input.csv.
Write it to the aoa_to_1d pipe.
Read the output of aoa_to_1d and pass it to the median_filter.py pipe.
Write the final result to output.csv.

________________________________________
4. Shutdown and cleanup
________________________________________


Shut down all files and processes.

Delete named pipes.
________________________________________
5. Test
________________________________________

Write a test plan with several cases to cover.
Implement at least one automated test.




# [3] Static Components (Software Module) and Matrix of Software Requirements

| File | Description |
|-------------------------|----------------------------------------------------------------------------------------------------------------|
| `aoa_to_1d.c` |         A C program that computes the 1D position from angle and height values. It reads from and writes to named pipes. |
| `median_filter.py` |    A Python script that applies a median filter on the last second's worth of position data. |
| `pipeline.py` |         The main orchestrator that creates FIFOs, launches processes, manages data flow, and handles cleanup. |
| `input.csv` |           Sample input data in CSV format. |
| `output.csv` |          Final filtered output generated by the pipeline. |
| `test_pipe.py` |        A test suite that verifies the correctness, robustness, and performance of the system. |
| `run_all.sh` |          A Bash script that automates compilation, execution, and testing. |
| `Makefile` |            Compiles `aoa_to_1d.c` into an executable using `make`. |



## [3.1] Input Format

Each row in `input.csv` contains a timestamped angle measurement:

_________________________________________________________________________________
timestamp [seconds],     tag_id [string],        angle [deg.] , tag_height [m] 
1733062840000      ,4baf351178aa9b0e               ,-30 ,  1.2
_________________________________________________________________________________



# [4] TEST PLAN 

__________
Test phase
__________

Write a test plan with various cases to cover.
Implement at least one automatic test: the one I choose is y(x) = x case then OUTPUT == EXPECTED ???

Test Plan for pipeline.py using test_pipe.py as CALLER

********************************************************************************************
1. Test Named Pipes Creation [Setup test]

TASK: Verify that all named pipes are created correctly before running the program.

Success Criteria: After pipeline.py is started, the files input_pipe.fifo, output_pipe_aoa.fifo
and output_pipe_filter.fifo must exist 3/3

********************************************************************************************

********************************************************************************************
2. Process Startup Test

TASK: Check that aoa_to_1d and median_filter.py are started correctly.

==> first run gcc -o aoa_to_1d aoa_to_1d.c -lm
like:
gcc -c script.c
gcc -o exe script.c

fix the "bug": I consulted the linux documentation

/usr/bin/ld: /tmp/cca4wrEa.o: in function `main':
aoa_to_1d.c:(.text+0x202): undefined reference to `tan'
collect2: error: ld returned 1 exit status
********************************************************************************************

I have set the "Success Criterion" for both processes that must be active in the system after the execution of pipeline.py.
i.e. processes Pi and Pj are exactly aoa_to_1d.c and median_filter.py




__________________________________________________________________________________________________________________________________________
TC 1: Read and Write Tests on Named Pipes that gave me problems and therefore you should implement on files
____________________________________________________________________________________________________________________________________________

TASK: Verify that data flows correctly between named pipes.

Success Criterion: Data written to input_pipe.fifo must be correctly read by aoa_to_1d, and
the results must be correctly transferred to median_filter.py.

_________________________________________
TC 2: Data Processing Tests
_________________________________________

TASK: Verify that aoa_to_1d correctly calculates the position and that median_filter.py correctly applies the median filter.

In the Dataframe test I found: (example with df.head(5) )

Input DataFrame:
 timestamp tag_id angle tag_height
0 1733062840000 4baf351178aa9b0e -30 1.2
1 1733062840100 4baf351178aa9b0e -28 1.2
2 1733062840200 4baf351178aa9b0e -39 1.2
3 1733062840300 4baf351178aa9b0e -27 1.2
4 1733062840400 4baf351178aa9b0e -4 1.2

 ########################################

 Test Number 1 Preview
 ########################################


Filtered DataFrame:
 timestamp tag_id angle tag_height
0 1733062840000 4baf351178aa9b0e -30.0 1.2
1 1733062840100 4baf351178aa9b0e -29.0 1.2
2 1733062840200 4baf351178aa9b0e -30.0 1.2
3 1733062840300 4baf351178aa9b0e -29.0 1.2
4 1733062840400 4baf351178aa9b0e -28.0 1.2
##############################################################################################################################
Check of the Length:
Input csv DF: 42
Output csv DF: 42

Success Criteria: For a given known input, the output must match the expected calculations.

_________________________________________
TC 3: Final Output Generation Test
_________________________________________

TASK: Ensure that the output.csv file is generated correctly and contains valid data.

Success Criterion: The output.csv file should be populated with the filtered data
without any formatting errors. This test can be simply
automated using dataframes and then casting the dataframe to a
csv so there is no need to worry about it

_________________________________________
TC 4: Cleanup and Termination Test
_________________________________________

TASK: Ensure that, at the end of the execution, the processes are properly terminated and that the named pipes are deleted.

Success Criterion: After the execution of pipeline.py, the processes should terminate and the FIFO files should be removed or the files should be deleted.

(Garbage collector logic in Java)

_________________________________________
TC 5: Robustness Testing with Bad Inputs [not managed!]
_________________________________________

TASK: Check that the system correctly handles bad or incorrectly formatted inputs.

Success Criterion: The system should ignore bad rows and continue processing without interruption.

_________________________________________
TC 6: Performance Testing
_________________________________________

TASK: Evaluate the processing time for a large dataset.

Success Criterion: The system should process and a large input file within a reasonable time without crashing
and a not well solution could be the chuncks-subdivision of the input.csv.

_________________________________________
TC 7: Concurrency Testing
_________________________________________

TASK: Check the behavior of the system under multiple simultaneous inputs.

Success Criterion: The system must continue to run without deadlocks or data loss.

_________________________________________
Example of Automated Test for CASE 3
_________________________________________

Test: Output Verification for a Test Case

Objective: Automate a test that verifies that the generated output matches the expected output for a known input.

Method:

1. Create an input_test.csv file with known data, and you have that.
2. Run pipeline.py with input_test.csv.
3. Compare the generated output.csv to a reference file that you can create, but don't have now.
4. Success Criteria: The generated output must be identical to the expected file because this proves that the system is working correctly.



# [5] How to Run the global system

### 1. Compilation

To compile the C component:

Run the bash script 
make
Alternatively, manually:
gcc -o aoa_to_1d aoa_to_1d.c -lm


### 2. Execute the Pipeline
Run the main Python orchestrator:

python3 pipeline.py

This creates the FIFO pipes, starts the sub-processes, streams input and output, and performs cleanup.


## How to Run the Testing for the Test Plan

A comprehensive test plan is provided in test_pipe.py, covering the following areas:

1. Creation of FIFO pipes

2. Launching of external processes

3. Data transmission between components (via files instead of FIFOs, where needed)

4. Correct processing of known input data

5. Validation of generated output

6. Cleanup of processes and FIFOs

7. Robustness to malformed or corrupted input

8. Performance under large datasets

9. Concurrency with simultaneous inputs

10. Automated test of one complete known case

Run All Tests

python3 test_pipe.py

Or run the full automation: bash

./run_all.sh

# FIFO Architecture


[input.csv]
    ↓
[input_pipe.fifo]
    ↓
[aoa_to_1d]
    ↓
[output_pipe_aoa.fifo]
    ↓
[median_filter.py]
    ↓
[output_pipe_filter.fifo]
    ↓
[output.csv]

# [6] Assumptions
1. The system runs on Linux or WSL, with FIFO support.

2. CSV inputs are assumed to be mostly well-formed.

3. Processes properly handle EOF and pipe input.

4. Malformed lines are skipped without halting processing.

5. The pipeline is linear and sequential, but concurrency is tested in parallel scenarios.

# [7] Requirements: Technologies
Skills in Named Pipe both in C and Python
Python 3.7 or higher in PyCharm Community Edition
GCC (to compile the C source)
Linux or WSL environment
Setup of the WSL
SOLID Principles are not mandatory in this application


# Cleanup
Temporary files and named pipes are automatically removed by pipeline.py and run_all.sh.


# [8] Summary of the Processes (High level sorting)

--- High
### BASH: run_all.sh ----------> the automation of the whole process
### Python: test_pipe.py ------> the implementation of the test plan for pipeline.py
### Python: pipeline.py -------> the real "main"
### Python: median_filter.py --> Preprocessing phase #2
### C    : aoa_to_1d.c --> Preprocessing phase #1
--- Low


# [9] APPENDIX: Linux pills

The typical C compiler in Linux system is gcc (GNU C Compiler).

Syntax to reach /mnt:
cd /mnt/c/Users/....../AAA_Tool_development_workspace/Routing  (in my case)

However remember that each path in Windows is mapped in Ubuntu (WSL) in this way:

C:\Users\...\PycharmProjects   ==> WINDOWS

/mnt/c/Users/.../PycharmProjects/ ==> WSL (Ubuntu)

In alternative you can create a Virtual Environment using PyCharm (venv) or WSL shell:
nicola@LAPTOP:~$ python3 -m venv nome_env
nicola@LAPTOP:~$ source nome_env/bin/activate

Using Bash Programming you can use:
cmd.exe /c start notepad.exe
++++++++++++++++++++++++++++++++
Linux CMD    |	Effects
++++++++++++++++++++++++++++++++	
**ifconfig**     |	Display network configuration information
**ip addr show ** |	Both show the type of interface, protocols, hardware and IP addresses, network masks and various other information about each of the active interfaces on the system.
**route ** |	To view a table that describes where network packages are sent. Other numeric version with "route -n" or "ip route show". 
**ping**   |	determine if another machine is reachable
**netstat**|  display information about network connections as well as display the routing table similar to the route command
**netstat** -i  |	display statistics regarding network traffic
**netstat** -r  |	routing information
**netstat** -tln |	-t stands for TCP (recall this protocol from earlier in this chapter), -l stands for listening (which ports are listening) and -n stands for show numbers, not names.
**ss**  |	show socket statistics and supports all the major packet and socket types. Meant to be a replacement for and to be similar in function to the netstat command, it also shows a lot more information and has more features.
**dig**	  |  performs queries on the DNS server to determine if the information needed is available on the server ( resolve the IP address  )
**host**  |	requires to DNS server to giv e back the IP from the <host, IP> association tuple
**ssh**   |	"connect to another machine across the network, log in and then perform tasks on the remote machine.

If you only provide a machine name or IP address to log into, the ssh command assumes you want to log in using the same username that you are currently logged in as."
grep 127.0.0.1 /etc/hosts	Verify that the IP address 127.0.0.1 has an entry in the /etc/hosts file
ping -c4 localhost	Send only 4 pkts
netstat --help	how you can read documentation
start_webserver	Use it followed by "ss" ti display network statistics
service network restart	the networking for the system is stopped and then started back up.


**jobs**  |	verify running processes
ping localhost > /dev/null &	Using ps -o pid,tty,time,%cpu,cmd the command shows information
**top**	View the processes data structure with information such as PID, User, resource, %CPU, %MEM, timestamp, commands
**sleep**	choose the PID of the process which you want to asleep
**free**	command outputs statistics about
ls /var/log	where to see logs





### [9.1] C language pills...

Syntax to build a binary executable
 $ gcc-o <exec_name> <source_code>.c

Syntax to produce object code
 $ gcc-c <source_code>.c
 the output file is named <source_code>.o

Syntax to both build a binary executable and run it:
$ gcc <source_code>.c -o exe_name && ./exe_name

Syntax to install gcc:
$ sudo apt update && sudo apt install build-essential


### atof()
The atof() function converts a C-style string, passed as an argument to atol() function, to double. 
It converts the C-string str to a value of type double by interpreting the characters of the string as numerical values. It discards the leading whitespace characters until a non-whitespace character is found.

### fopen() and fclose()
fopen() and fclose() : similar to
open() and close() Linux C language system calls but interact with files and allow you to act in a "formatted" way


### fscanf() and fprintf()
fprintf() and fscanf() : similar to
printf() and scanf() but interact with files and allow you to act in a "formatted" way



### fgets() and fflush()

fgets() and stdin: the fgets() function can therefore be used to read a line from the keyboard (overcoming the limits of the input from the file to the keyboard (stdin).

s=fgets(vector,DIM,fileptr);
s -> vector address
vector -> vector that will contain the read line
DIM -> vector size
fileptr -> pointer to the file to read
The fgets() function adds the character \0
end of string to the end of the line

fflush(fileptr): flushes to disk all the writings
contained in the buffer



### [9.2] Python language pills...

Syntax to install python:
$ sudo apt install python3-pip

Syntax to see it:
which python3
(you should see /usr/bin/python3)

Syntax to discover python version
$ python3 --version

Syntax to upgrade the pip, e.g. if  new release of pip is available: 23.2.1 -> 25.0.1
$ python.exe -m pip install --upgrade pip

Syntax to upgrade the library used in this project:
$ pip install -r requirements.txt

Syntax to install pandas:
$ sudo apt install python3-pandas

Syntax to check the pandas version:
python3 -c "import pandas; print(pandas.__version__)"

Syntax to verify process running:
ps aux | grep aoa_to_1d
ps aux | grep python3

You can see the list of all active processes in your machine using
 ps-el

Syntax to run python script on bash (shell):
$ python3 pipeline.py

Syntax to know the state of WSL (e.g. Docker) on Windows PowerShell:
> wsl -l -v


### [9.3] C language syntax pills - Particular case: aoa_to_1d.c  contains math.h (see below)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


Including  library  functions into  a program
gcc-o <exec> <source>.c -L<dir> -l<name>

The -l options is used to tell the compiler that  some functions in the source code have their 
object code in the lib<name>.a
 
the library is not in a standard directory, the directory must be specified through the  -L <dir>
option.

Standard libraries are part of the Operating System, while other 
libraries are distributed with the compiler; libcis the default C library containing input and output functions 
such as printf, scanf, open, read, write, etc.

Indeed, at first glance the syntax:

gcc -o aoa_to_1d aoa_to_1d.c

should be sufficient to correctly compile the file aoa_to_1d.c. However, in this case, it is necessary to add the -lm flag to link the math library (libm), and here is why "  gcc -o aoa_to_1d aoa_to_1d.c -lm  " is correct and mandatory!



# [10] APPENDIX C language: PIPES

In C, you can operate on files only in terms of sequences
of bytes: stream
There are no high-level functions like in other languages ​​such as Python that mimics the write() and read() of C.
In the C code of the project we use pointers.

To read and write to files, a pointer to a derived type is used
FILE *fileptr; //pointer to the file

This procedure is identical whether you use a file or a pipe.


(1) Example of pipe: When a process opens a file, a non-negative integer is returned, 
called file descriptor.  I/O redirection allows writing a program where data are read from 
stdinand written on stdout
 During program execution it is possible to duplicate the file 
descriptor used to refer to an open file so that a standard file 
descriptor can also be used to refer to that file.
 By closing the files associated to the standard file descriptors 
0(stdin)
 1(stdout)
 2(stderr)
 and then calling dup, it is possible to use 0, 1, or 2 to access the file 
whose descriptor is passed to dup



----------------------------------------------------------
unnamed pipes: allow interprocess communication between 
processes in a parent-child relationship
----------------------------------------------------------


#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>//for open()
#include <string.h> //for sprintf() : the output is a string
#include <sys/stat.h>

int main(){
	int x;
	int fd_pipe[2];//one for reading and one for writing
	char str[100];
	
	pipe(fd_pipe);//creating of communication channel in the parent channel
	printf("Please type an integer number: ");
	scanf("%d",&x);

	switch(fork()){
		case 0:
			//Parent's fd inheritance
			close(fd_pipe[0]);//because it has to write
			sprintf(str,"[CHILD] The new number is %d\n",x+5);
			write(fd_pipe[1],str,strlen(str));
			
			return 0;
		default:
			close(fd_pipe[1]);//because it has to read
			read(fd_pipe[0],str,sizeof(str));//I dont need to loop
			printf("[PARENT] The Child says: %s\n",str);
	}
}


## Half duplex
Parent		    ___________________________________________________       Child
  fd[1]--->read ---------------------------------------------------fd[1]--->write
  fd[0]--->write---------------------------------------------------fd[0]--->read          
		         ___________________________________________________

## Full duplex

/*		BIDIRECTIONAL pipe

					CHANNEL
Parent		___________________________________________________                   Child
                <-----------------------------------------------------------fd_pipe_c2p[0]--->read
                <-----------------------------------------------------------fd_pipe_c2p[1]--->write         
fd_pipe_p2c[0]--->read--------------------------------------------------->
fd_pipe_p2c[1]--->write-------------------------------------------------->
		___________________________________________________


*/



(2) Another example of pipe: my script oao_to_1d.c



----------------------------------------------------------
named pipes: allow interprocess communication between any pair 
of unrelated processes (aoa_to_1d.c <--> median_filter.py)
----------------------------------------------------------


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_LINE_LENGTH 256

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <input_pipe> <output_pipe> <h_anchor>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *input_pipe = argv[1];
    const char *output_pipe = argv[2];
    double h_anchor = atof(argv[3]);

    FILE *input_fp = fopen(input_pipe, "r");
    if (!input_fp) {
        perror("Error opening input pipe");
        return EXIT_FAILURE;
    }

    FILE *output_fp = fopen(output_pipe, "w");
    if (!output_fp) {
        perror("Error opening output pipe");
        fclose(input_fp);
        return EXIT_FAILURE;
    }

    char line[MAX_LINE_LENGTH];
    while (fgets(line, sizeof(line), input_fp)) {
        unsigned long long timestamp;
        char tag_id[17];
        double angle, h_tag, x;
        
        if (sscanf(line, "%llu,%16[^,],%lf,%lf", &timestamp, tag_id, &angle, &h_tag) != 4) {
            fprintf(stderr, "Error parsing line: %s", line);
            continue;
        }

        double alpha_rad = angle * M_PI / 180.0;
        x = (h_anchor - h_tag) * tan(alpha_rad);

        fprintf(output_fp, "%llu,%s,%.2f\n", timestamp, tag_id, x);
        fflush(output_fp);
    }

    fclose(input_fp);
    fclose(output_fp);
    return EXIT_SUCCESS;
}


In C you can operate on files only in terms of sequences
of bytes: stream
There are no high-level functions like in other languages ​​such as Python that mimics the write() and read() of C.
In the C code of the project we use pointers.

To read and write to files we use a pointer to a derived type
FILE *fileptr; //pointer to the file

This procedure is identical whether you use a file or a pipe.

==> Script 2: aoa_to_1d.c <==
--Features: It uses named pipes (FIFO), i.e. special files in the filesystem.

The program takes the names of the pipes as command line arguments.

It communicates between separate processes (not necessarily parent-child) via FIFO files created before running the script.

--How it works:

FILE *input_fp = fopen(input_pipe, "r");
FILE *output_fp = fopen(output_pipe, "w");
These pipes must already exist, for example created with:

mkfifo pipe_input
mkfifo pipe_output


The process reads from one pipe (input_pipe) and writes the processing to another (output_pipe).

There is no fork() in the code → the processes involved are launched separately but communicate with each other via these special files.

==> Key concept:
Persistent inter-process communication, based on FIFO files in the filesystem.

==> Script 1: pipe.c <==
--Features:
Uses unnamed pipes, i.e. anonymous pipes created with pipe(fd_pipe).

It works internally between a parent process and its child process created with fork().

It is all autonomous, no files in the filesystem.

--How it works:

pipe(fd_pipe);
fork();

Child writes to pipe (fd_pipe[1])

Father reads from pipe (fd_pipe[0])

Data (integer plus 5) is passed directly into shared memory via pipe.

--Key concept:
Parent-child communication based on anonymous pipes in RAM. It is temporary and limited to the lifetime of the process.

## Differences summary:
Feature                        aoa_to_1d.c   (2)            pipe.c  (1)
Pipe type                      Named pipe (FIFO)             Unnamed pipe (anonymous pipe)
Communication                  between separate processes    Parent process ↔ child (fork)
Pipe creation                  Externally with mkfifo        Internally with pipe()
I/O mechanism                  fopen(), fprintf(), fgets()   read(), write()

Persistence Can persist in filesystem, Temporary, exists only in RAM



# [11] Bibliography and Sitography

1) Kaggle for Pandas
2) GitHub
3) Cisco Academy: Linux Essentials (my badge to https://www.credly.com/badges/7eaeeba1-b530-4d8b-a5b9-933588064a8c)
4) Edutecnica https://www.edutecnica.it/informatica
5) Learn C++ – Skill up with our free tutorials
6) RFId: https://www.researchgate.net/publication/375717478_Wireless_Systems_-_Progettazione_di_un'antenna_su_tessuto_per_Wireless_Local_Area_Network

   






