/* Main function of the C program. 

  ======================================================================================
 |	Author	of	the	Project	-	Engineer	Nicola	Lombardi	|
  ======================================================================================
 |	MSc.	in	Telecommunications	and	Internet	of	Things	|
 |	Telecommunications Engineering    	|	SW HW	ENGINEER	        |
  ======================================================================================
 |Professional	Profile
 |		it.linkedin.com/in/nicola-lombardi-09046b205

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

#define DIM_3D      3  // to have the template v = (v1, v2, v3)
#define DIM_string 256


// ########################
// # Glob. variable(s) sec#
// ########################


char str_header_sep[] = "\n*********************************************************************************\n";
char mem_err[] = "[OS] Memory allocation failed\n";
char new_vec_alert[] = "[OS] Memory allocation successful\n";
char buffer[DIM_string]; // used to print and avoid for cycle with snprintf
float precision_angle = 1e-6; // 1 / 10^6
float angle_pi_deg = 180.0;

// Built-in C language used in this program:

// -- Math.h
// pow(base, exponent);
// acos()

// -- String.h
// strcat(str1, str2); // Concatenate str2 to str1: str1 on the left (1st)
// snprintf(str, size, format, ...) // Instead to use ForLoop to print char by char a string of N char

// fprintf
// fopen
// fclose

// System Calls

// perror
// exit


// #################
// # Typedef(s) sec#
// #################

typedef struct vector{
    float v[DIM_3D]; // v = vx i + vy j + vz k
    int N;           // This is the chosen N dynamically with the constrain N < DIM_3D
    float id;        // needs to be filled with the Module used as "label id"
} vec_t;

/* Example about vec_t type scope:
vec_t vector;
vector.N = 3;
vector.v[0] = -1.5;   // xyz.x = -1.5;
vector.v[1] = 2.2;   // xyz.y = 2.2;
vector.v[2] = -3.5;   // xyz.z= -3.5;
*/

typedef struct Geometry_template{
    vec_t vec1;
    vec_t vec2;
    float dot_prod;     // < vec1 , vec2 >
    float mutual_angle; // arccos { <u,v> / [ ||u|| * ||v|| ] }
    float area;         // norm of vec1 x vec2
} geometry_plane;


// #################
// # Prototypes    #
// #################

// Main functions
void double_check(vec_t u, vec_t v);
void fill_vector(vec_t *vec);
vec_t* create_and_set_vector();
void fill_array(int size, vec_t* vec);
int* create_array(int size);
float dot_product(vec_t vx, vec_t vy);
float module(vec_t vx);
float angle_estimation(vec_t vx, vec_t vy);
int vec_size_handler(int N);
void start();
void display_log(char *msg);
float area_vectors(vec_t vx, vec_t vy); 
void print_vector(vec_t *vec);
void print_array(vec_t* vx);
void print_geometry_plane(geometry_plane *g);
void save_geometry_csv(geometry_plane *g, const char *filename);


// Support functions (no prototype defined being optional)

int custom_string_len(char *str){
    int count=0;
    // using termination character 
    while(str[count] != '\0'){
        count++;
    } 
    return count; // it corresponds to the length
}


// #################
// # Main Program  #
// #################

int main(){
    int i = 0;
    vec_t u, v;
    geometry_plane u_v_plane;
    
    puts("Start the Program Calculation! \t\t implements theta = arccos { <u,v> / [ ||u|| * ||v|| ] }  with θ c [0, pi]");
    
    display_log("Creating first vector:");
    fill_vector(&u);
    print_vector(&u);

    display_log("Creating second vector:");
    fill_vector(&v);
    print_vector(&v);
    
    double_check(u, v);
    
    float dot = dot_product(u, v);
    float angle_rad = 0.0, angle_deg = 0.0, area = 0.0;

    if (fabs(dot) > precision_angle) {
        angle_rad = angle_estimation(u, v);
        angle_deg = angle_rad * angle_pi_deg / M_PI;
        area = abs(area_vectors(u, v)); // e.g. the round of -0.00002 could be represented as -0.00, but in this way 0.00 as expected.

        snprintf(buffer, sizeof(buffer), "Mutual angle θ = %.2f radians (%.2f degrees)", angle_rad, angle_deg);
        display_log(buffer);

        snprintf(buffer, sizeof(buffer), "Area = ||u|| * ||v|| * sin(θ) = %.2f", area);
        display_log(buffer);
    } else {
        display_log("Vectors are orthogonal: angle = near or equivalent to π/2 or 90 degrees");
    }

    // Fill the geometry_plane struct
    u_v_plane.vec1 = u;
    u_v_plane.vec2 = v;
    u_v_plane.dot_prod = dot;
    u_v_plane.mutual_angle = angle_rad;
    u_v_plane.area = area;

    display_log("Geometry plane template has been created successfully.");
    
    display_log("FINAL GEOMETRY PLANE REPORT:");
    print_geometry_plane(&u_v_plane);

    // CSV save
    save_geometry_csv(&u_v_plane, "geometry_plane.csv");

    return EXIT_SUCCESS;
}


// #################
// # Declarations  #
// #################

void double_check(vec_t u, vec_t v){
    if (vec_size_handler(u.N) == -1 || vec_size_handler(v.N) == -1) {
        exit(EXIT_FAILURE);
    }
}


vec_t* create_and_set_vector(){
    vec_t* v_pointer = (vec_t*) malloc(sizeof(vec_t));
    if (!v_pointer) {
        perror(mem_err);
        display_log(mem_err);
        exit(EXIT_FAILURE);
    }

    display_log("New Vector will be created:\n");
    fill_vector(v_pointer);
    print_vector(v_pointer);
    return v_pointer;
}


// Function to display an existing array
void print_array(vec_t* vx){
    display_log("Received array:\n");
    float x = vx->v[0];
    float y = vx->v[1];
    float z = vx->v[2];
    printf("v = x (%0.2f) + y (%0.2f) + z (%0.2f)\n", x, y, z);
}


// Function to create and return an array using dynamic memory allocation [customization]
int* create_array(int size){
    int* array = (int*)malloc(size * sizeof(int));
    if (array == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    return array;
}


// Input helper for vector array
void fill_array(int size, vec_t* vec){
    display_log("Fill the array:\n");
    int i = 0;
    for (i = 0; i < size; i++){
        scanf("%f", &vec->v[i]);
    }
}


/* Used to print a log */
void display_log(char *msg){
    printf("%s%s%s", str_header_sep, msg, str_header_sep);
}


/* Used to print the program scope */
void start(){
    printf("%s", str_header_sep);
    printf("This program considers two vectors as defined below\n\t\t v = vx i + vy j + vz k");
    printf("%s", str_header_sep);
}


/* Fill vector */
void fill_vector(vec_t *vec){
    display_log("Fill the array:\n");
    int i = 0;
    vec->N = DIM_3D;
    for (i = 0; i < vec->N ; i++){
        scanf("%f", &vec->v[i]);
    }
    vec->id = module(*vec);
}


/* Print vector */
void print_vector(vec_t *vec){
    display_log("Printout of the array:\n");
    snprintf(buffer, sizeof(buffer), "Vector (ID = %.2f):", vec->id);
    display_log(buffer);
    int i;
    for (i = 0; i < vec->N ; i++){
        printf("v [%d] = %f\n", i, vec->v[i]);
    }
}


/* Check vector dimension */
int vec_size_handler(int N){
	if(N == DIM_3D) return 0;
	else{
		perror("[Error] Vector has an incorrect dimension to estimate mutual angle.\n");
        return -1;
	}
}


/* Dot product */
float dot_product(vec_t vx, vec_t vy){
    float dot_p_res = 0;
    int i;
    if (vx.N != vy.N){
        perror("[Error] Vectors have different dimensions.");
        return 0.0;
    }
    for (i = 0; i < vx.N ; i++){
        dot_p_res += vx.v[i] * vy.v[i];
    }
    printf("Dot Product result ->  <u,v> = %0.2f\n", dot_p_res);
    return dot_p_res;
}


/* Norm ||.||2 */
float module(vec_t vx){
    int i;
    float result = 0;
    for (i = 0; i < vx.N ; i++){
        result += pow(vx.v[i], 2);
    }
    return sqrt(result);
}


/* θ = arccos { <u,v> / [ ||u|| * ||v|| ] } */
float angle_estimation(vec_t vx, vec_t vy){
    return acos(dot_product(vx, vy) / (module(vx) * module(vy)));
}


/* Area = ||u|| * ||v|| * sin(θ) */
float area_vectors(vec_t vx, vec_t vy){
    float angle_rad = angle_estimation(vx, vy);
    return module(vx) * module(vy) * sin(angle_rad);
}


void print_geometry_plane(geometry_plane *g) {
    printf("Vector u:\n");
    print_vector(&g->vec1);
    printf("\nVector v:\n");
    print_vector(&g->vec2);
    printf("\nResults:\n");
    printf("  Dot product: <u,v> = %.2f\n", g->dot_prod);
    printf("  Angle θ: %.4f radians = %.2f degrees\n", g->mutual_angle,
           g->mutual_angle * angle_pi_deg / M_PI);
    printf("  Area: %.2f\n", g->area);
}

void save_geometry_csv(geometry_plane *g, const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        perror("File open failed");
        return;
    }

    fprintf(fp, "Vector,Component 1,Component 2,Component 3,Modulo\n");
    fprintf(fp, "u,%.2f,%.2f,%.2f,%.2f\n", g->vec1.v[0], g->vec1.v[1], g->vec1.v[2], g->vec1.id);
    fprintf(fp, "v,%.2f,%.2f,%.2f,%.2f\n", g->vec2.v[0], g->vec2.v[1], g->vec2.v[2], g->vec2.id);
    fprintf(fp, "\nDot Product,%.2f\n", g->dot_prod);
    fprintf(fp, "Angle (radians),%.4f\n", g->mutual_angle);
    fprintf(fp, "Angle (degrees),%.2f\n", g->mutual_angle * angle_pi_deg / M_PI);
    fprintf(fp, "Area,%.2f\n", g->area);

    fclose(fp);
    display_log("Geometry plane data saved to 'geometry_plane.csv'");
}

