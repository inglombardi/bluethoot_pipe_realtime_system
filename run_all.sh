#!/bin/bash
echo "⏳ Compiling aoa_to_1d.c..."
gcc -o aoa_to_1d aoa_to_1d.c -lm
if [ $? -ne 0 ]; then
    echo "❌ Compilation failed. Check aoa_to_1d.c"
    exit 1
fi
echo "✅ Compilation completed."

echo "🚀 START the test suite..."
python3 test_pipe.py
if [ $? -eq 0 ]; then
    echo "✅ ALL TESTS PASS!"
else
    echo "❌ SOME TESTS FAILED."
    exit 1
fi

echo "🧹temporary files cleaning..."
rm -f aoa_to_1d
rm -f *.fifo
rm -f output.csv expected_output.csv input.csv

echo "✅ Clean completed."
