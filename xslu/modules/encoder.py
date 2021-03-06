import torch
import torch.nn as nn
import torch.nn.functional as F

from xslu.modules.embedding import Embedding

class EncoderRNN(nn.Module):
    r"""
    Applies a multi-layer RNN to an input sequence.

    Args:
        rnn_type (str): type of RNN cell, one of [RNN, GRU, LSTM]
        bidirectional (bool): if True, becomes a bidirectional encodr 
        num_layers (int): number of recurrent layers 
        hidden_dim (int): the dimensionality of the hidden state `h`
        embedding (nn.Module): predefined embedding module
        dropout (float, optional): If non-zero, introduces a dropout layer on the outputs of each RNN layer except the last layer (default: 0)
    """

    def __init__(self, rnn_type, bidirectional, num_layers, hidden_dim,
            embedding, dropout=0):

        super(EncoderRNN, self).__init__()

        self.rnn_type = rnn_type
        if self.rnn_type not in ["GRU", "LSTM"]:
            raise Exception("Unsupported RNN Type in decoder")
        self.embedding = embedding
        self.hidden_dim = hidden_dim
        self.rnn = getattr(nn, rnn_type)(embedding.emb_dim, hidden_dim, num_layers,
                batch_first=True, bidirectional=bidirectional, dropout=dropout)
        
        self.init_params()

    def forward(self, src, lengths=None, h0=None):
        """
        Applies a multi-layer RNN to an input sequence.

        Args:
            src (batch_size, seq_len): tensor containing the features of the input sequence.
            lengths (LongTensor, optional): A tensor that contains the lengths of sequences
              in the mini-batch
            h0 (tensor, optional): tensor containing the initial hidden state. Default to zero.

        Returns: output, hidden
            - **output** (batch, seq_len, hidden_dim * num_directions): tensor containing the encoded features of the input sequence
            - **hidden** (num_layers * num_directions, batch, hidden_dim): tensor containing the features in the hidden state h
        """
        emb = self.embedding(src)  # batch_size * seq_len * emb_dim

        if lengths is not None:
            lengths = lengths.view(-1).tolist()
            emb = nn.utils.rnn.pack_padded_sequence(emb, lengths, batch_first=True)
        output, hidden = self.rnn(emb, h0)
        if lengths is not None:
            output, _ = nn.utils.rnn.pad_packed_sequence(output, batch_first=True)
        return output, hidden

    def init_params(self):
        for name, param in self.named_parameters():
            if 'weight' in name:
                nn.init.uniform_(param, -0.1, 0.1)
            elif 'bias' in name:
                nn.init.constant_(param, 0)
