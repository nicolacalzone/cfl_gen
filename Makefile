SHELL=/bin/bash

all:
        # Documentation
        #
        # goals:
        #       preprocess: preprocess the data
        #       (clean_and_preprocess: clean old saves and preprocess it)
        #       train: train the model
        #       generate: generate outputs
        #       score: score the output
        #       --> run: run all the goals
        #
        # utils:
        #       run_all: run all the goals
        #       run_synCFG: run the synCFG_generator.py
        #       run_metrics: run the metrics.py
        #       clean_logs: clean the logs
        #       create_files_for_score: create files for scoring

run_all: run_synCFG run_metrics

clean_logs:
	@echo "Cleaning the logs..." 
	rm -r logs
        mkdir logs

run_synCFG:
        @echo "Running synCFG_generator.py..."
        python3 synCFG_generator.py

run_metrics:
        @echo "Running metrics.py..."
        python3 metrics/metrics.py


####################
#### PREPROCESS ####
####################

.PRECIOUS: preprocess
preprocess:
        @echo "Preprocessing..." 
        fairseq-preprocess \
                --source-lang src \
                --target-lang tgt \
                --trainpref output/train \
                --validpref output/valid \
                --testpref output/test \
                --destdir data-bin \
                --workers 20
        touch preprocess

.PRECIOUS: clean_and_preprocess
clean_and_preprocess: 
        @echo "Cleaning and Preprocessing..." 
        rm -rf data-bin/
        make -B preprocess


####################
##### TRAINING #####
####################

.PRECIOUS: train
train:
        @echo "Training..." 
        fairseq-train data-bin \
                --arch transformer --share-decoder-input-output-embed \
                --encoder-layers 6 --decoder-layers 6 \
                --encoder-embed-dim 512 --decoder-embed-dim 512 \
                --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 1.0 \
                --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
                --dropout 0.3 --max-tokens 4096 \
                --eval-bleu \
                --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
                --save-dir data-bin/training_checkpoints 
        touch train

.PRECIOUS: train_grok
train_grok:
	fairseq-train data-bin/grok \
		--arch transformer_iwslt_de_en \
		--share-decoder-input-output-embed \
		--optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
		--lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
		--dropout 0.3 --weight-decay 0.0001 \
		--criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
		--max-tokens 4096 \
		--eval-bleu \
		--eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}' \
		--eval-bleu-detok moses \
		--eval-bleu-remove-bpe \
		--best-checkpoint-metric bleu --maximize-best-checkpoint-metric
	touch train_grok


####################
#### GENERATION ####
####################

.PRECIOUS: generate
generate:
	fairseq-generate data-bin/training_checkpoints/results/generate_output.txt \
		--path data-bin/training_checkpoints/checkpoint_best.pt \
		--batch-size 128 \
		--beam 5
                --source-lang gen_sr --target-lang gen_tg
	touch generate_iwslt14

####################
####### SCORE ######
####################

create_files_for_score:
        grep ^H gen.out | cut -f3- > gen.out.sys
	grep ^T gen.out | cut -f2- > gen.out.ref

.PRECIOUS: score
score:
        fairseq-score --sys gen.out.sys --ref gen.out.ref



####################
#####   ALL   ######
####################
.PRECIOUS: run
run:
        make -B run_all
        make -B clean_and_preprocess
        make -B train
        make -B generate
        make -B score