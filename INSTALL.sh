wget https://mirror.oxfordnanoportal.com/software/analysis/ont-guppy_3.4.5_linux64.tar.gz 
tar -zvxf ont-guppy_3.4.5_linux64.tar.gz
mkdir bin/ont-guppy_3.4.5_linux64
mv ont-guppy bin/ont-guppy_3.4.5_linux64
cd bin
ln -s ont-guppy_3.4.5_linux64/ont-guppy/bin/guppy_* .
cd ../
rm -fr ont-guppy_3.4.5_linux64.tar.gz
