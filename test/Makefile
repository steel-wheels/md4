
MD4_CMD	= python3 ../src/md4.py

all: test0 test1 test2 test3 test4

clean:
	rm -f *.tmp

test0: dummy
	$(MD4_CMD) test_0.txt | tee test_0.txt.tmp
	diff test_0.txt test_0.txt.tmp
	$(MD4_CMD) < test_0.txt | tee test_0.txt.tmp
	diff test_0.txt test_0.txt.tmp
	rm test_0.txt.tmp

test1: dummy
	$(MD4_CMD) test_1.txt | tee test_1.txt.tmp
	diff test_1.txt.tmp test_1.exp
	rm test_1.txt.tmp

test2: dummy
	$(MD4_CMD) test_2.txt | tee test_2.txt.tmp
	diff test_2.txt.tmp test_2.exp
	rm test_2.txt.tmp

test3: dummy
	$(MD4_CMD) --output test_3.txt.tmp test_3.txt
	diff test_3.txt.tmp test_3.exp
	rm test_3.txt.tmp

test4: dummy
	$(MD4_CMD) --output test_4.txt.tmp test_4.txt
	diff test_4.txt.tmp test_4.exp
	rm test_4.txt.tmp

dummy:
	
