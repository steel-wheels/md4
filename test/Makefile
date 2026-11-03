
MD4_CMD	= python3 ../src/md4.py

all: test0 test1

test0: dummy
	$(MD4_CMD) test_0.txt | tee test_0.txt.tmp
	diff test_0.txt test_0.txt.tmp
	$(MD4_CMD) < test_0.txt | tee test_0.txt.tmp
	diff test_0.txt test_0.txt.tmp
	rm test_0.txt.tmp

test1: dummy
	$(MD4_CMD) test_1.txt 

dummy:
	
