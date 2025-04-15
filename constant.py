"""
 =================================================================
 |	Author	of	the	Project	-	Engineer	Nicola	Lombardi	|
 =================================================================
 |	MSc.	in	Telecommunications	and	Internet	of	Things	|
 |	Telecommunications Engineering    	|	SW HW	ENGINEER	|

 |Professional	Profile
 |		it.linkedin.com/in/nicola-lombardi-09046b205


"""
import datetime


####################################
# I / O pipe and file variables
####################################
# Selection for two kind of solution: text file and pipe
USE_FILES = True # flag


"""
:About: USE_FILES
If you use: USE_FILES = False # flag
OSError: [Errno 95] Operation not supported

Stackoverflow:
succede perché stai cercando di creare una named pipe (con os.mkfifo) all'interno di un filesystem montato da Windows (es. /mnt/c/...), e WSL 
non supporta le FIFO (mkfifo) su filesystem non nativi Linux come quelli montati da Windows.
"""


####################################
# Geometric variables
####################################


# height of the  Bluetooth tag
# which acts as a Bluetooth beacon, broadcasting packets
h_anchor = "1.5"  # 1.5 [m] reasonable

"""
:About: h_anchor
By knowing the fixed height of the anchor and the assessed 
height of the tag, and after applying some smoothing/filtering, the application uses this 
information to update the cow’s 1-D position xT in real-time:

The Geometry is describe in a x-y plane:

    d(A, T) = | A(x,y) - T(x,y) |
    A = x * 0 + y * h_anchor = ( 0 , h_anchor)
    T = x * tan (alpha) * (h_anchor - h_tag) + y * 0 = ( tan (alpha) * (h_anchor - h_tag) , 0)

The input.csv stores < timestamp , tag_id , angle , tag_height > and the pipeline.py creates pipes for aoa_to_1d.c to
obtain geometric data with the code fragment below:

    unsigned long long timestamp;
    char tag_id[17];
    double angle, h_tag, x;
    
    if (sscanf(line, "%llu,%16[^,],%lf,%lf", &timestamp, tag_id, &angle, &h_tag) != 4) {
        fprintf(stderr, "Error parsing line: %s", line);
        continue;
    }

    double alpha_rad = angle * M_PI / 180.0;
    x = (h_anchor - h_tag) * tan(alpha_rad);

"""

####################################
# Generic scope variables
####################################

timing = 0.01

####################################
# CSV name files variables
####################################

INPUT_CSV = "input.csv"
OUTPUT_CSV = "output.csv"
EXPECTED_CSV = "expected_output.csv"


####################################
# Header variables
####################################

new_plot_test_number = "###############################################################################\n"
header = """
				#####################################\n
					Test	Number	{0}	Preview
			    #####################################\n"""
clock_string = f"[{datetime.datetime.now()}]"
sep = "#################################################################################################"

dataframe_plot = (" ###########################################################\n"
                  "                     [DataFrame plotting ... ]"
                  " ###########################################################\n")