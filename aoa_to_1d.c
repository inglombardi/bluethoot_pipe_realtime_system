/*

 =================================================================
 |	Author	of	the	Project	-	Engineer	Nicola	Lombardi	|
 =================================================================
 |	MSc.	in	Telecommunications	and	Internet	of	Things	|
 |	Telecommunications Engineering    	|	SW HW	ENGINEER	|

 |Professional	Profile
 |		it.linkedin.com/in/nicola-lombardi-09046b205


*/

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
