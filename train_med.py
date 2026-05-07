out_dir = 'out-medical-scratch'
eval_interval = 250
log_interval = 10
eval_iters = 100
always_save_checkpoint = True

dataset = 'med'
gradient_accumulation_steps = 1
batch_size = 32
block_size = 256

n_layer = 6
n_head = 6
n_embd = 384
dropout = 0.1
bias = False

learning_rate = 6e-4
max_iters = 5000
weight_decay = 0.1
beta1 = 0.9
beta2 = 0.95
grad_clip = 1.0

decay_lr = True
warmup_iters = 200
lr_decay_iters = 5000
min_lr = 6e-5

init_from = 'scratch'

device = 'cuda'
dtype = 'bfloat16'
compile = False

wandb_log = True
wandb_project = 'nanogpt-med'
wandb_run_name = 'med-scratch-run'
