SHELL=/bin/bash

all:
	# Documentation
	# goals:
	# 	- (spm)(fs)pretokenize
	# 	- (spm)(fs)tokenize
	# 	- preprocess
	# 	- preprocess_old
	# 	- train

run_all: run_synCFG run_metrics show_src_freq

run_synCFG:
	@echo "Running synCFG_generator.py..."
	python3 synCFG_generator.py

run_metrics:
	@echo "Running metrics.py..."
	python3 metrics/metrics.py

show_src_freq:
	@echo "Displaying p_src_freq..."
	cat db/train/prove/p_src_freq

.PRECIOUS: spm_pretokenize
spm_pretokenize: 
	spm_train \
    --input=db/train/sr.clean,db/train/tg.clean \
    --model_prefix=subword \
    --vocab_size=1700 \
    --character_coverage=1.0 \
    --model_type=bpe

.PRECIOUS: spm_tokenize
spm_tokenize:
	/usr/bin/spm_encode --model=subword.model --output_format=piece < db/train/sr.clean > db/train/bpe/bpe_sr.tok
	/usr/bin/spm_encode --model=subword.model --output_format=piece < db/train/tg.clean > db/train/bpe/bpe_tg.tok

.PRECIOUS: preprocess
preprocess:
	fairseq-preprocess \
		--source-lang sr \
		--target-lang tg \
		--trainpref train.bpe \
		--testpref test.bpe \
		--destdir data-bin \
		--workers 2 \
		--srcdict subword.vocab \
		--tgtdict subword.vocab 
	touch preprocess_new


.PRECIOUS: preprocess_old
preprocess_old:
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