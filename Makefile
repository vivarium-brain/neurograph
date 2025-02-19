all:
	@mkdir build
	@make --no-print-directory clean
	@mkdir build/lib build/obj build/bin
	@make --no-print-directory libneurograph
	@make --no-print-directory main

clean:
	@echo -e "\033[0;32mcleaning\033[0m"
	rm -rf build/* test.ng

main: build/lib/libneurograph.so src/main.cpp
	@echo -e "\033[0;32mbuilding main\033[0m"
	g++ -g src/main.cpp -Lbuild/lib -lneurograph -Iinclude -o build/bin/main

libneurograph: src/neurograph/Neurograph.cpp src/neurograph/versions/NGv1.cpp
	@echo -e "\033[0;32mbuilding libneurograph.so objects\033[0m"
	g++ -g -fPIC -Iinclude -c src/neurograph/Neurograph.cpp -o build/obj/neurograph.o 
	g++ -g -fPIC -Iinclude -c src/neurograph/versions/NGv1.cpp -o build/obj/ng_ver1.o
	@echo -e "\033[0;32mbuilding libneurograph.so\033[0m"
	g++ -g -shared -Wl,-soname,libneurograph.so -o build/lib/libneurograph.so \
		build/obj/neurograph.o build/obj/ng_ver1.o

run:
	@echo -e "\033[0;32mrunning main\033[0m"
	LD_LIBRARY_PATH=build/lib build/bin/main

debug:
	@echo -e "\033[0;32mdebugging main\033[0m"
	LD_LIBRARY_PATH=build/lib gdb build/bin/main

