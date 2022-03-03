import pdb
import torch
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import Node2Vec 
from utils import *
# from draw_graph import get_connection_weight

index2food = read_dict_from_json('data/h_index2food.json')
all_connection_dict = read_dict_from_json('data/sorted_all_connection_dict.json')
all_connection_list = list(all_connection_dict.keys())
idx_connection_list = [string2tuple(pair) for pair in all_connection_list]
idx_connection_list = [[int(x1), int(x2)] for x1, x2 in idx_connection_list]

edge_index = torch.tensor(idx_connection_list, dtype=torch.long)
edge_index = torch.t(edge_index)
edge_index_ = edge_index[[1, 0], :]
new_edge_index = torch.concat((edge_index, edge_index_), dim=1)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = Node2Vec(edge_index=new_edge_index, embedding_dim=64, walk_length=20,
             context_size=10, walks_per_node=10,
             num_negative_samples=1, p=1, q=1, sparse=True).to(device)

loader = model.loader(batch_size=128, shuffle=True, num_workers=0)
optimizer = torch.optim.SparseAdam(list(model.parameters()), lr=0.01)

nodes = edge_index.numpy()
nodes = np.unique(list(nodes[0, :]) + list(nodes[1, :]))
print(nodes.shape)

# np.random.seed(10)
# # get the nodes
# np.random.shuffle(nodes) # shuffle node order
# print(len(nodes))

# get train test and val sizes: (70% - 15% - 15%)
train_size = int(len(nodes)*0.7)
test_size = int(len(nodes)*0.85) - train_size
val_size = len(nodes) - train_size - test_size

# get train test and validation set of nodes
train_set = nodes[0:train_size]
test_set = nodes[train_size:train_size+test_size]
val_set = nodes[train_size+test_size:]

print(len(train_set), len(test_set), len(val_set))
# build test train val masks

train_mask = torch.zeros(len(nodes),dtype=torch.long, device=device)
for i in train_set:
    train_mask[i] = 1.

test_mask = torch.zeros(len(nodes),dtype=torch.long, device=device)
for i in test_set:
    test_mask[i] = 1.
    
val_mask = torch.zeros(len(nodes),dtype=torch.long, device=device)
for i in val_set:
    val_mask[i] = 1.
    
data = Data(edge_index=new_edge_index)
data.train_mask = train_mask
data.test_mask = test_mask
data.val_mask = val_mask

def train():
    model.train()
    total_loss = 0
    for pos_rw, neg_rw in loader:
        optimizer.zero_grad()
        loss = model.loss(pos_rw.to(device), neg_rw.to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


@torch.no_grad()
def test():
    model.eval()
    z = model()
    acc = model.test(z[data.train_mask], data.y[data.train_mask],
                     z[data.test_mask], data.y[data.test_mask],
                     max_iter=10)
    return acc


for epoch in range(1, 101):
    loss = train()
    # acc = test()
    if epoch % 10 == 0:
        print(f'Epoch: {epoch:02d}, Loss: {loss:.4f}')


z = model()
# from tensor to numpy
emb_64 = z.detach().cpu().numpy()

from sklearn.decomposition import PCA
# fit and transform using PCA
pca = PCA(n_components=2)
emb2d = pca.fit_transform(emb_64)
print(emb2d.shape)

plt.title("ingredient embedding in 2D")
plt.scatter(emb2d[:,0],emb2d[:,1])

for idx, ing in enumerate(list(index2food.values())[:20]):
    plt.scatter(emb2d[int(idx), 0],emb2d[int(idx), 1], label=ing)
    plt.legend()

plt.savefig('ingredient_embedding_2d.png')
plt.show()