# This script should be run at s5/

if [ ! -d "exp" ]; then
    echo "Missing exp/"
    exit 1
fi 

if [ "$#" -ne 2 ]; then
    echo "Missing required arguments. Please provide the following:"
    echo "1: path to directory which has final.mdl,"
    echo "2: path to directory which has HCLG.fst"
    exit 1
fi

ln -s ../../wsj/s5/steps .
ln -s ../../wsj/s5/utils .
ln -s ../../../src .

src="pretrained_decode"

if [ ! -d "${src}/audio" ]; then
    mkdir -p $src/audio
    echo "Created ${src}/audio/"
fi

if [ ! -f "${src}/decode_execution.log" ]; then
    touch $src/decode_execution.log
    echo "Created ${src}/decode_execution.log"
fi

if [ ! -d "data" ]; then
    mkdir -p data
    echo "Created data/"
fi

if [ ! -d "data/${src}" ]; then
    mkdir -p data/$src
    echo "Created data/${src}"
fi

mkdir -p data/$src/conf
cp conf/mfcc.conf data/$src/conf/
echo "Copied mfcc.conf to data/${src}/conf"

if [ ! -d "mfcc" ]; then
    mkdir -p mfcc
    echo "Created mfcc/"
fi

if [ ! -d "exp/make_mfcc" ]; then
    mkdir -p exp/make_mfcc
    echo "Created exp/make_mfcc/"
fi

if [ ! -d "exp/${src}" ]; then
    mkdir -p exp/$src
    echo "Created exp/${src}/"
fi

if [ ! -d "exp/${src}/pretrained_exp" ]; then
    mkdir -p exp/$src/pretrained_exp
    echo "Created exp/${src}/pretrained_exp/"
fi

if [ ! -d "exp/${src}/pretrained_exp/graph" ]; then
    mkdir -p exp/$src/pretrained_exp/graph
    echo "Created exp/${src}/pretrained_exp/graph"
fi

if [ ! -d "exp/$src/decode_${src}/log" ]; then
    mkdir -p exp/$src/decode_${src}/log
    echo "Created exp/${src}/decode_${src}/log/"
fi

mdlDir=$1
HCLGDir=$2

cp $mdlDir/final.mdl ./exp/$src/pretrained_exp
cp $mdlDir/final.mat ./exp/$src/pretrained_exp
if [ -f "${mdlDir}/splice_opts" ]; then
    cp $mdlDir/splice_opts ./exp/$src/pretrained_exp
fi
if [ -f "${mdlDir}/cmvn_opts" ]; then
    cp $mdlDir/cmvn_opts ./exp/$src/pretrained_exp
fi
if [ -f "${mdlDir}/delta_opts" ]; then
    cp $mdlDir/delta_opts ./exp/$src/pretrained_exp
fi

cp -a $HCLGDir/. ./exp/$src/pretrained_exp/graph