#/bin/sh

g++ single.cc -o single.o
g++ multithread.cc -o multithread.o
g++ multiprocess.cc -o multiprocess.o

echo "Python"
echo "Single thread version"
python3 single.py
echo 
echo "Multi thread version"
python3 multithread.py
echo 
echo "Multi process version"
python3 multiprocess.py
echo 

echo "C++"
echo "Single thread version"
./single.o
echo 
echo "Multi thread version"
./multithread.o
echo 
echo "Multi process version"
./multiprocess.o
echo
