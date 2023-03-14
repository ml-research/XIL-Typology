import util
from data_store.datasets import decoy_mnist_all_revised
from learner.learner import Learner
from learner.models import dnns
import torch

import logging
logging.basicConfig(level=logging.INFO)


SEED = [1, 10, 100, 1000, 10000]
SHUFFLE = True
BATCH_SIZE = 250
LEARNING_RATE = 0.001
WEIGHT_DECAY = 0.0001
EPOCHS = 50
SAVE_BEST_EPOCH = True
MODELNAME = 'SuperMODEL3000'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
logging.info(f"Compute DEVICE={DEVICE}")

from rtpt import RTPT
rtpt = RTPT(
    name_initials='EW',
    experiment_name='main_MNIST', 
    max_iterations=EPOCHS
)

torch.set_printoptions(linewidth=150)
torch.set_num_threads(5)
util.seed_all(SEED[0])  # TODO allow seed selection

train_loader, test_loader = decoy_mnist_all_revised(
    fmnist=True,
    train_shuffle=SHUFFLE,
    device=DEVICE,
    batch_size=BATCH_SIZE,
    generate_counterexamples=True,
    reduced_training_size=BATCH_SIZE
)

model = dnns.SimpleConvNet().to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

learner = Learner(
    model,
    optimizer,
    DEVICE,
    MODELNAME,
    loss_rrr_weight=1.0,
    loss_weight_rrr_gc=torch.Tensor([1.] * 10),
    loss_weight_cdep=torch.Tensor([1.] * 10),
    loss_weight_hint=torch.Tensor([1.] * 10),
    # loss_weight_hint_ig=torch.Tensor([1.] * 10),
    loss_weight_rbr=torch.Tensor([1.] * 10),
)

learner.fit(
    train_loader,
    test_loader,
    EPOCHS,
    save_best_epoch=SAVE_BEST_EPOCH
)
# avg0.append(learner.score(test_dataloader, nn.CrossEntropyLoss())[0])
