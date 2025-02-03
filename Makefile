SHELL=/bin/bash

all:
        # Documentation
        # runs:
        #       - run_synCFG
        #       - run_metrics
        #       - show_src_freq
        #
        # goals:
        #       - preprocess
        #       - train
		# 	 	- train_grok
		# 		- generate_grok
		#       - generate
		#       - generate_try
		#
		# utilities:
		#       - clean_logs
		#       - preprocess
		#       - clean_and_preprocess

run_all: run_synCFG run_metrics show_src_freq

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

show_src_freq:
        @echo "Displaying p_src_freq..."
        cat db/train/prove/p_src_freq


.PRECIOUS: preprocess
preprocess:
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
        rm -rf data-bin/
        make -B preprocess

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

.PRECIOUS: generate_grok
generate_grok:
	fairseq-generate data-bin \
		--path data-bin/training_checkpoints/checkpoint_best.pt \
		--beam 5 --remove-bpe \
		--results-path data-bin/training_checkpoints/results
	touch generate_grok

.PRECIOUS: generate
generate:
        fairseq-generate data-bin \
                --path databin/training_checkpoints/checkpoint_best.pt \
        --beam 5 --batch-size 128 \
                --source-lang gen_sr --target-lang gen_tg 
        touch generate

.PRECIOUS: generate_try
generate_try:
        fairseq-generate data-bin \
                --path data-bin/training_checkpoints/checkpoint_best.pt \
                --batch-size 128 \
                --beam 5 \
                --remove-bpe \
                --max-len-a 1.0 \
                --max-len-b 50 \
                --lenpen 1.0 \
                --no-repeat-ngram-size 3 \
                --replace-unk \
                --sacrebleu
        touch generate