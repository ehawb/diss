from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, add
from tensorflow.keras.layers import Input, Dense, Flatten
from tensorflow.keras.models import Model

def conv_bn_relu_block(name, activation = True, filters = 256,
                       kernel_size = (3, 3), strides = (1, 1),
                       padding = 'same', init = 'he_normal'):
    
    def f(inputs):
        conv = Conv2D(filters = filters,
                      kernel_size = kernel_size,
                      strides = strides,
                      padding = padding,
                      kernel_initializer = init,
                      data_format = 'channels_first',
                      name = f'{name}_conv_block')(inputs)
        batch_norm = BatchNormalization(axis = 1,
                                        name = f'{name}_batch_norm')(conv)
        return Activation('relu', name = f'{name}_relu')(batch_norm) if activation else batch_norm
    
    return f


def residual_block(block_num, **args):
    
    def f(inputs):
        res = conv_bn_relu_block(name = f'residual_1_{block_num}', activation = True, **args)(inputs)
        res = conv_bn_relu_block(name = f'residual_2_{block_num}', activation = False, **args)(inputs)
        res = add([inputs, res], name = f'add_{block_num}')
        return Activation('relu', name = f'{block_num}_relu')(res)
    
    return f

def residual_tower(blocks):
    
    def f(inputs):
        x = inputs
        for i in range(blocks):
            x = residual_block(block_num = i)(x)
        return x
    return f

def dual_residual_network(num_edges, input_shape, blocks = 20):
    inputs = Input(shape = input_shape)
    first_conv = conv_bn_relu_block(name = 'init')(inputs)
    res_tower = residual_tower(blocks = blocks)(first_conv)
    policy = policy_head(num_edges)(res_tower)
    value = value_head()(res_tower)
    return Model(inputs = inputs, outputs = [policy, value])

def policy_head(num_edges):
    def f(inputs):
        conv = Conv2D(filters = 2,
                      kernel_size = (3, 3),
                      strides = (1, 1),
                      padding = 'same',
                      name = 'policy_head_conv_block')(inputs)
        batch_norm = BatchNormalization(axis = 1, name = 'policy_head_batch_norm')(conv)
        activation = Activation('relu', name = 'policy_head_relu')(batch_norm)
        flat = Flatten()(activation)
        return Dense(units = num_edges*2, name = 'policy_head_dense', activation = 'softmax')(flat)
    
    return f

def value_head():
    def f(inputs):
        conv = Conv2D(filters = 1,
                      kernel_size = (1, 1),
                      strides = (1, 1),
                      padding = 'same',
                      name = 'value_head_conv_block')(inputs)
        batch_norm = BatchNormalization(axis = 1, name = 'value_head_batch_norm')(conv)
        activation = Activation('relu', name = 'value_head_relu')(batch_norm)
        flat = Flatten()(activation)
        dense = Dense(units = 256, name = 'value_head_dense', activation = 'relu')(flat)
        return Dense(units = 1, name = 'value_head_output', activation = 'tanh')(dense)
    
    return f