from share import *

import pytorch_lightning as pl
from torch.utils.data import DataLoader
from tutorial_dataset import MyDataset
from cldm.logger import ImageLogger
from cldm.model import create_model, load_state_dict
import torch
from ldm.modules.diffusionmodules.openaimodel import TimestepEmbedSequential
from pytorch_lightning.callbacks import ModelCheckpoint

# Configs
#resume_path = './models/control_sd15_ini.ckpt'
resume_path = './lightning_logs/POG_5_VITON_low_match/epoch=26-step=157247.ckpt'
batch_size = 1
logger_freq = 300
learning_rate = 1e-5
sd_locked = True
only_mid_control = False


# First use cpu to load models. Pytorch Lightning will automatically move it to GPUs.
model = create_model('./models/cldm_v15.yaml').cpu()



model.control_model.set_new_hint_block()
for i in model.control_model.zero_convs.modules():
    if isinstance(i, torch.nn.Conv2d):
        for p in i.parameters():
            p.detach().zero_()
    elif isinstance(i, TimestepEmbedSequential):
        for j in i.modules():
            for p in j.parameters():
                p.detach().zero_()


model.load_state_dict(load_state_dict(resume_path, location='cpu'))

#model.control_model.input_blocks.load_state_dict(model.model.diffusion_model.input_blocks.state_dict())
#model.control_model.middle_block.load_state_dict(model.model.diffusion_model.middle_block.state_dict())


model.learning_rate = learning_rate
model.sd_locked = sd_locked
model.only_mid_control = only_mid_control

# save checkpoints
checkpoint_callback = ModelCheckpoint(
#                save_top_k=-1,
#                monitor="epoch",
#                mode="max",
                dirpath="lightning_logs/result/test_10",
                every_n_train_steps=5824,
                save_weights_only=False
            )


# Misc
dataset = MyDataset()
#dataloader = DataLoader(dataset, num_workers=0, batch_size=batch_size, shuffle=True)
dataloader = DataLoader(dataset, num_workers=0, batch_size=batch_size, shuffle=False)

logger = ImageLogger(batch_frequency=logger_freq)
trainer = pl.Trainer(gpus=1, precision=32, callbacks=[logger, checkpoint_callback])


# Train!
trainer.fit(model, dataloader)

