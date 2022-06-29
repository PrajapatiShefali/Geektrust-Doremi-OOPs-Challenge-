@echo off
pip install -r requirements.txt --ignore-installed
python -m geektrust sample_input\input1.txt
python -m unittest -v tests.test
