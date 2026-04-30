    out_dir = 'out-medical'
    eval_interval = 500
    log_interval = 10

    dataset = 'med'   
    batch_size = 32
    block_size = 128

    n_layer = 6
    n_head = 6
    n_embd = 384
    dropout = 0.1

    learning_rate = 3e-4
    max_iters = 5000
    lr_decay_iters = 5000
    min_lr = 3e-5
    warmup_iters = 100

    weight_decay = 0.1
    beta1 = 0.9
    beta2 = 0.95

    device = 'cuda'  

    wandb_log = True
    wandb_project = 'nanogpt-med'
    wandb_run_name = 'med-run-1'