import hashlib
import tensorflow as tf

from update_rules import hebbian, anti_hebbian, random_walk


class TPM:
    '''
    A tree parity machine.
    The machine can be described by the following parameters:
    K - The number of hidden neurons
    N - Then number of input neurons connected to each hidden neuron
    L - Defines the range of each weight ({-L, ..., -2, -1, 0, 1, 2, ..., +L })
    W - The weight matrix between input and hidden layers. Dimensions: [K, N]
    '''

    def __init__(self, name, K=8, N=12, L=4):
        '''
        Arguments:
        K - The number of hidden neurons
        N - Then number of input neurons connected to each hidden neuron
        L - Boundaries of each weight ({-L, ..., -2, -1, 0, 1, 2, ..., +L })'''
        self.name = name
        with tf.name_scope(name):
            self.K = tf.constant(K)
            self.N = tf.constant(N)
            self.L = tf.constant(L)
            self.W = tf.Variable(tf.random.uniform(
                (K, N), minval=-L, maxval=L + 1, dtype=tf.int64),
                trainable=True)

    def get_output(self, X):
        '''
        Returns a binary digit tau for a given random vecor.
        Arguments:
        X - Input random vector
        '''

        W = self.W
        tf.reshape(X, [self.K, self.N])

        # Compute inner activation sigma Dimension:[K]
        sigma = tf.math.sign(tf.math.reduce_sum(
            tf.math.multiply(X, W), axis=1))
        tau = tf.math.reduce_prod(sigma)  # The final output

        with tf.name_scope(self.name):
            self.X = X
            self.sigma = sigma
            self.tau = tau

        return tau

    def __call__(self, X):
        return self.get_output(X)

    def update(self, tau2, update_rule='hebbian'):
        '''
        Updates the weights according to the specified update rule.
        Arguments:
        tau2 - Output bit from the other machine;
        update_rule - The update rule.
        Should be one of ['hebbian', 'anti_hebbian', random_walk']
        '''
        if (self.tau == tau2):
            if update_rule == 'hebbian':
                hebbian(self.W, self.X, self.sigma, self.tau, tau2, self.L)
            elif update_rule == 'anti_hebbian':
                anti_hebbian(self.W, self.X, self.sigma,
                             self.tau, tau2, self.L)
            elif update_rule == 'random_walk':
                random_walk(self.W, self.X, self.sigma,
                            self.tau, tau2, self.L)
            else:
                raise Exception("Invalid update rule. Valid update rules are: "
                                + "\'hebbian\', "
                                + "\'anti_hebbian\' and "
                                + "\'random_walk\'."
                                )

    def makeKey(self, key_length, iv_length):
        '''
        weight matrix to key and iv : use sha512 on concatenated weights
        '''
        key = ""
        iv = ""

        # generate key
        for i in tf.range(self.K):
            for j in tf.range(self.N):
                if i == j:
                    iv += tf.as_string(self.W[i, j])
                key += tf.as_string(self.W[i, j])

        def convert_to_hex_dig(input, is_iv=True):
            return hashlib.sha512(
                str(input).encode('utf-8')).hexdigest()[0:int(iv_length / 4
                                                              if is_iv else
                                                              key_length / 4)]

        return (convert_to_hex_dig(key, is_iv=False),
                convert_to_hex_dig(iv, is_iv=True))
