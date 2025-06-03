/*

  ======================================================================================
 |	Author	of	the	Project	-	Engineer	Nicola	Lombardi	|
  ======================================================================================
 |	MSc.	in	Telecommunications	and	Internet	of	Things	|
 |	Telecommunications Engineering    	|	SW HW	ENGINEER	        |
  ======================================================================================
 |Professional	Profile
 |		it.linkedin.com/in/nicola-lombardi-09046b205

This program reads AoA (Angle of Arrival) data from an input pipe, computes a 3D 
position using azimuth and elevation (zenith) angles, and writes the result to an output pipe.

Instructions

###########################
1- Compile the source code:
###########################
---bash---

gcc aoa_to_3d.c -o aoa_to_3d -lm

#################################################################################
2- Create named pipes (FIFOs): (this step is performed by pipeline.py)
#################################################################################
---bash---

mkfifo input_pipe
mkfifo output_pipe

#################################################################################
3- Run the program in the background:
#################################################################################
---bash---
$ ./aoa_to_3d input_pipe output_pipe 2.00 30.0 &

______________________________________
2.00 is the anchor height (in meters).

30.0 is the fixed elevation angle (in degrees).
______________________________________

#################################################################################
4- Send data to the input pipe (simulate a line of data):
#################################################################################
---bash---
$ echo "1234567890,ABC123,45.0,1.50" > input_pipe

______________________________________
45.0 = azimuth angle (degrees)

1.50 = tag height (meters)
______________________________________

#################################################################################
5- Read the result from the output pipe:
#################################################################################
---bash---
$ cat output_pipe

You will get a result like:

______________________________________
1234567890,ABC123,0.87,0.87,1.50,2.00

This means the 3D position has been calculated as:

______________________________________
x = 0.87 m
y = 0.87 m
z = 1.50 m
module -> 2.00 m
______________________________________

*/


// #################
// # Library(s) sec #
// #################

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// #################
// # Constants sec #
// #################

#define MAX_LINE_LENGTH     256
#define DIM_3D              3
const char read_permission = 'r';
const char write_permission = 'w';
char line[MAX_LINE_LENGTH];
char str_header_sep[] = "\n*********************************************************************************\n";
char mem_err[] = "[OS] Memory allocation failed\n";
char new_vec_alert[] = "[OS] Memory allocation successful\n";

// #################
// # Typedef(s) sec#
// #################

typedef struct vector {
    float v[DIM_3D]; // v = vx i + vy j + vz k
    int N;
    float id;
} vec_t;

// #################
// # Prototypes    #
// #################

// Main functions
float module(vec_t vx);
FILE *input_handler_txt(const char *txt_or_pipe);
FILE *output_handler_txt(const char *txt_or_pipe);
vec_t create_and_set_vector(double azimuth_rad, double distance, double h_tag);
void display_log(char *msg);

// #################
// # Main Program  #
// #################

int main(int argc, char *argv[]) {

    if (argc != 5) {
        fprintf(stderr, "Usage: %s <input_pipe> <output_pipe> <h_anchor> <angle_elevation_deg>\n", argv[0]);
        return EXIT_FAILURE;
    }

    // Dynamic upgrade for each test
    const char *input_pipe_name = argv[1];
    const char *output_pipe_name = argv[2];
    double h_anchor = atof(argv[3]);
    double elevation_deg = atof(argv[4]);

    FILE *input_fp = input_handler_txt(input_pipe_name);
    FILE *output_fp = output_handler_txt(output_pipe_name);

    while (fgets(line, sizeof(line), input_fp)) {

        // Data Record Field  < timestamp, tag_id, azimuth_deg, h_tag >
        unsigned long long timestamp;
        char tag_id[17];
        double azimuth_deg, h_tag;

        // Data record acquisition
        if (sscanf(line, "%llu,%16[^,],%lf,%lf", &timestamp, tag_id, &azimuth_deg, &h_tag) != 4) {
            fprintf(stderr, "Error parsing line: %s", line);
            continue;
        }

        double delta_h = h_anchor - h_tag;
        double elevation_rad = elevation_deg * M_PI / 180.0;
        double azimuth_rad = azimuth_deg * M_PI / 180.0;
        double distance = delta_h * tan(elevation_rad);

        vec_t position = create_and_set_vector(azimuth_rad, distance, h_tag);

        display_log("New parsed outcome : ");

        fprintf(output_fp, "%llu,%s,%.2f,%.2f,%.2f,%.2f\n",
                timestamp, tag_id,
                position.v[0], position.v[1], position.v[2], position.id);

        fflush(output_fp);
    }

    fclose(input_fp);
    fclose(output_fp);
    return EXIT_SUCCESS;
}

// #################
// # Declarations  #
// #################

float module(vec_t vx) {
    float result = 0;
    int i;
    for (i = 0; i < vx.N; i++) {
        result += powf(vx.v[i], 2);
    }
    return sqrtf(result);
}

FILE *input_handler_txt(const char *txt_or_pipe) {
    FILE *input_fp = fopen(txt_or_pipe, "r");
    if (!input_fp) {
        perror("Error opening input pipe");
        exit(EXIT_FAILURE);
    }
    return input_fp;
}

FILE *output_handler_txt(const char *txt_or_pipe) {
    FILE *output_fp = fopen(txt_or_pipe, "w");
    if (!output_fp) {
        perror("Error opening output pipe");
        exit(EXIT_FAILURE);
    }
    return output_fp;
}

vec_t create_and_set_vector(double azimuth_rad, double distance, double h_tag) {
    vec_t position;
    position.N = DIM_3D;
    position.v[0] = distance * cos(azimuth_rad);  // x coord
    position.v[1] = distance * sin(azimuth_rad);  // y coord
    position.v[2] = h_tag;                        // z (tag's quote)
    position.id = module(position);               // module as ID
    return position;
}

/* Used to print a log */
void display_log(char *msg) {
    printf("%s%s%s", str_header_sep, msg, str_header_sep);
}
