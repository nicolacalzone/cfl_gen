SHELL=/bin/bash

all:
	# Documentation
	# goals:
	# - preprocessing
	# - training
	# - generation

.PRECIOUS: preprocess
preprocess:
	fairseq-preprocess --source-lang sr --target-lang tg \
	   --trainpref db/train --testpref db/test \
	   --destdir data-bin/preprocessed_ds \
	   --workers 20
	touch preprocess

.PRECIOUS: train
train:
	fairseq-train data-bin \
		--arch transformer --share-decoder-input-output-embed \
		--encoder-layers 6 --decoder-layers 6 \
		--encoder-embed-dim 512 --decoder-embed-dim 512 \
		--optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 1.0 \
		--lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
		--dropout 0.3 --max-tokens 4096 \
		--criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
		--save-dir data-bin/training_checkpoints 
	touch train

.PRECIOUS: generate
generate:
	fairseq-generate <data-bin-dir> \
		--path <output-model-dir>/checkpoint_best.pt \
    	--beam 5 --batch-size 128 \
		--source-lang gen_sr --target-lang gen_tg 
	touch generate