#!/bin/bash

mode=gen

experiment=dstc3-da
data_root=../dstc3-st/manual-da/
memory_path=tmp/memory.pt
train_file=dstc3.seed
valid_file=dstc3.valid

load_model=tmp.dstc2train.M2.pt
save_model=tmp.dstc2train.M2.pt

deviceid=1

epochs=50
batchs=20

optim=adam
lr=0.001
maxnorm=5

test_file=new.value.test.templete
class_file=ttp/m1.v2.3
save_file=ttp/m1.v2.3.0.3best.train
nbest=3

python da/templete-M2/main.py -mode $mode -experiment $experiment -data_root $data_root \
    -memory_path $memory_path -train_file $train_file -valid_file $valid_file \
    -save_model $save_model -deviceid $deviceid \
    -epochs $epochs -batch_size $batchs \
    -optim $optim -lr $lr -max_norm $maxnorm \
    -test_file $test_file -save_file $save_file -nbest $nbest -class_file $class_file \
    -load_word_emb -load_model $load_model
