out_dir = 'out-medical-finetune'
eval_interval = 250
log_interval = 10
eval_iters = 100
always_save_checkpoint = True

dataset = 'med'
gradient_accumulation_steps = 4
batch_size = 8
block_size = 1024

n_layer = 12
n_head = 12
n_embd = 768
dropout = 0.1
bias = True

learning_rate = 3e-5
max_iters = 5000
weight_decay = 0.1
beta1 = 0.9
beta2 = 0.95
grad_clip = 1.0

decay_lr = True
warmup_iters = 100
lr_decay_iters = 2000
min_lr = 3e-6

init_from = 'gpt2'

device = 'cuda'
dtype = 'bfloat16'
compile = False

wandb_log = True
wandb_project = 'nanogpt-med'
wandb_run_name = 'med-finetune-gpt2'