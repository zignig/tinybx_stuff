git clone https://github.com/m-labs/migen.git lib/migen
git clone https://github.com/YosysHQ/nextpnr.git lib/nextpnr
git clone https://github.com/m-labs/nmigen lib/nmigen
git clone https://github.com/cliffordwolf/yosys.git lib/yosys
git clone https://github.com/cliffordwolf/icestorm.git lib/icestorm
git clone https://github.com/enjoy-digital/litex lib/litex
git clone https://github.com/FPGAwars/apio lib/apio

apt-get install libboost-all-dev qt5-default libftdi-dev

cd lib/migen
python setup.py install


cd ../nextpnr
cmake -DARCH=ice40 .
make install

cd ../nmigen 
python setup.py install 

cd ../yosys
make
make install 

cd ../icestorm
make
make install

cd ../migen
python setup.py install

cd ../litex
python setup.py install

cd ../apio
python setup.py install


