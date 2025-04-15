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

 The CALLER CODE

The Test Plan tests each single phase of the workflow:
_________
WORKFLOW
_________

(1) Create named pipes (FIFO)

Create 2 pipes: one for aoa_to_1d and one for median_filter.py.
Start processes

(2) Compile and run aoa_to_1d.

Start median_filter.py with its parameters.
Data flow management

(3) Preprocessing 1

Read data from input.csv.
Write it to the pipe of aoa_to_1d.

(4) Preprocessing 2

Read the output of aoa_to_1d and pass it to the pipe of median_filter.py.

(5) Data Postprocessing and pipes removing

Write the final result to output.csv.
Shutdown and cleanup

Shut down all files and processes.
Delete named pipes.
"""
import subprocess
import os
import filecmp
import time
import logging
import pandas as pd

FIFO_FILES = ["input_pipe.fifo", "output_pipe_aoa.fifo", "output_pipe_filter.fifo"]

#  logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    """ Pipeline Launcher
        (I)  Features: Pipeline orchestrator
        (II) Target: Method to start the Preprocessing phases
        :return: NONE
    """
    if os.path.exists("output.csv"):
        os.remove("output.csv")

    # Run the cmd : python3 pipeline.py in Ubuntu (WSL)
    logging.info("[PIPE PROCESSOR] STARTING THE PROCESSING ")
    subprocess.run(["python3", "pipeline.py"]) # the called (pipeline.py) by the caller (test_pipe.py)

    # stdout, stderr = subprocess.communicate()

    # use check_call instead of returncode
    if subprocess.check_call(["ls", "-l"])  != 0:
        # logging.error(f"PIPE ERROR: {stderr.decode()}")
        logging.error("ERROR")
    else:
        logging.info("Pipeline completed !!!!!!!!!!")

# *****************************************************************************
# --------------------------  TEST PLAN --------------------------------------
# *****************************************************************************

def test_pipeline_output():
    """ Workflow phase to test: (5) Data Postprocessing and pipes removing
        (I)  Features: Pipeline orchestrator emulation using DataFrame, Simulates the expected data flow
         and compares the output.csv file with an expected_output.csv
        (II) Target: Method to finish the Preprocessing and Filter phases
        :return: NONE

        Example of alternative comparison:


        import pandas as pd

        # Simulazione dei due file CSV
        df1 = pd.DataFrame({
            "timestamp": [1733062840000, 1733062840100],
            "tag_id": ["4baf351178aa9b0e", "4baf351178aa9b0e"],
            "angle": [-30.0, -28.0],
            "tag_height": [1.2, 1.2]
        })

        df2 = pd.DataFrame({
            "timestamp": [1733062840000, 1733062840100],
            "tag_id": ["4baf351178aa9b0e", "4baf351178aa9b0e"],
            "angle": [-30.0, -28.0],
            "tag_height": [1.2, 1.2]
        })

        # Salva i file (simulazione)
        df1.to_csv("output.csv", index=False, header=False)
        df2.to_csv("expected_output.csv", index=False, header=False)

        df_out = pd.read_csv("output.csv", header=None)
        df_exp = pd.read_csv("expected_output.csv", header=None)

        assert df_out.equals(df_exp), "Output not matching with the expected DataFrame"

    """
    run_pipeline()
    time.sleep(2)

    # Input data Simulation
    expected_data = {
        "timestamp": [1733062840000, 1733062840100, 1733062840200, 1733062840300, 1733062840400],
        "tag_id": ["4baf351178aa9b0e"] * 5,
        "angle": [-30, -28, -39, -27, -4],
        "tag_height": [1.2] * 5
    }
    df = pd.DataFrame(expected_data)
    df.to_csv("expected_output.csv", index=False, header=False)
    assert os.path.exists("output.csv"), "Error output.csv not created"
    assert filecmp.cmp("output.csv", "expected_output.csv"), "Error: unexpected output"
    print("Test: PASS")
    logging.info("Test: PASS")

def compile_aoa():
    """ Workflow phase to test: (2) Compile and run  aoa_to_1d.c
        (I)  Features: Pipeline orchestrator
        (II) Target: Method to start the Preprocessing phases
        https://stackoverflow.com/questions/64638010/compare-csv-files-content-with-filecmp-and-ignore-metadata
        :return: NONE
    """
    result = subprocess.run(["gcc", "-o", "aoa_to_1d", "aoa_to_1d.c", "-lm"], capture_output=True)
    assert result.returncode == 0, f"Compilation failure: {result.stderr.decode()}"
    logging.info("[TEST] aoa_to_1d compiled correctly.")


def test_named_pipes_creation():
    """ Workflow phase to test: (1) Create named pipes (FIFO)
        (I)  Features: Pipeline creation
        (II) Target: Method to start the Preprocessing phases

        It has an inherent problem:

        Pipes are created and immediately removed at the end of pipeline.py, so by the time you get to assert os.path.exists(f) they are often gone.

        Additionally, if USE_FILES = True, pipes will not be created at all.

        :return: NONE
    """
    subprocess.Popen(["python3", "pipeline.py"])
    time.sleep(10)  # Waiting for pipeline.py creates pipes
    for f in FIFO_FILES:
        assert os.path.exists(f), f"Named pipe missing: {f}"
    logging.info("[TEST] Named pipes created correctly.")


def test_processes_start():
    """ Workflow phase to test: (2) Compile and run  aoa_to_1d.c
        (I)  Features: Process check-in
        (II) Target: Method to control the Preprocessing phases #1 and #2
        :return: NONE
    """
    compile_aoa()
    proc = subprocess.Popen(["python3", "pipeline.py"])
    time.sleep(2)

    ps_output = subprocess.check_output(["ps", "aux"]).decode()
    assert "aoa_to_1d" in ps_output, "aoa_to_1d.c does not work"
    assert "median_filter.py" in ps_output, "median_filter.py does not work"
    logging.info("[TEST] Process run correctly")
    proc.terminate()


def test_output_csv_generation():
    if os.path.exists("output.csv"):
        os.remove("output.csv")

    subprocess.run(["python3", "pipeline.py"])
    time.sleep(2)

    assert os.path.exists("output.csv"), "output.csv is not generated"
    df = pd.read_csv("output.csv", header=None)
    assert not df.empty, "output.csv is EMPTY"
    logging.info("[TEST] Output.csv generated correctly.")


def test_data_processing_correctness():
    expected_data = {
        "timestamp": [1733062840000, 1733062840100, 1733062840200, 1733062840300, 1733062840400],
        "tag_id": ["4baf351178aa9b0e"] * 5,
        "angle": [-30.0, -29.0, -30.0, -29.0, -28.0],
        "tag_height": [1.2] * 5
    }
    df_expected = pd.DataFrame(expected_data)
    df_expected.to_csv("expected_output.csv", index=False, header=False)

    subprocess.run(["python3", "pipeline.py"])
    time.sleep(2)

    assert filecmp.cmp("output.csv", "expected_output.csv"), "Output not matching with the Expected"
    logging.info("[TEST] Correct output verified with dataframe comparison.")


def test_cleanup():
    subprocess.run(["python3", "pipeline.py"])
    time.sleep(2)
    for f in FIFO_FILES:
        assert not os.path.exists(f), f"Pipe not removed: {f}"
    logging.info("[TEST] Cleanup completed: pipe removed.")


def test_robustness_wrong_input():
    with open("input.csv", "w") as f:
        f.write("timestamp,tag_id,angle,tag_height\n")
        f.write("not_a_timestamp,xyz,invalid_angle,??\n")
        f.write("1733062840000,4baf351178aa9b0e,-30,1.2\n")

    subprocess.run(["python3", "pipeline.py"])
    time.sleep(2)
    df = pd.read_csv("output.csv", header=None)
    assert len(df) >= 1, "Valid data not processed"
    logging.info("[TEST] Robustness: Handled incorrect inputs.")


def test_performance_large_file():
    df = pd.DataFrame({
        "timestamp": range(1000000, 1000500),
        "tag_id": ["4baf351178aa9b0e"] * 500,
        "angle": [-30 + (i % 10) for i in range(500)],
        "tag_height": [1.2] * 500
    })
    df.to_csv("input.csv", index=False)
    start = time.time()
    subprocess.run(["python3", "pipeline.py"])
    end = time.time()
    assert (end - start) < 5, "Performance not sufficient (>5s)"
    logging.info("[TEST] Performance ok on 500 rows.")




if __name__ == "__main__":
    # test_pipeline_output()

    # test_named_pipes_creation()
    test_processes_start()
    test_output_csv_generation()
    test_data_processing_correctness()
    test_cleanup()
    test_robustness_wrong_input()
    test_performance_large_file()
