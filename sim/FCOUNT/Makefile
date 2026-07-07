## Mixed-signal frequency-counter demo: analog LELO_VCO + RTL fcount counter.
## Compiles the Verilog to a d_cosim shared object, generates the SPICE
## instance, co-simulates in ngspice, and plots the count staircase.
##
## Run:  make count

CELL=LELO_VCO

## Compile RTL -> fcount.so and generate svinst.spi (the d_cosim instance).
## The generated .so path is made absolute so ngspice can dlopen it when run
## standalone from this directory.
rtl:
	-rm -rf fcount.so fcount_obj_dir svinst.spi
	ngspice vlnggen ../../rtl/fcount.v
	perl ../../tech/script/gensvinst ../../rtl/fcount.v fcount
	sed -i 's#"../fcount.so"#"$(CURDIR)/fcount.so"#' svinst.spi

count: rtl
	ngspice -b tran.spi 2>&1 | grep -E "MEASURED_COUNT" || true
	python3 plot_count.py

## Digital transfer curve: counter code vs Vin (ADC characteristic)
sweep: rtl
	python3 sweep_count.py

clean:
	-rm -rf fcount.so fcount_obj_dir svinst.spi fcount_wave.dat __pycache__
