from tensorflow.keras.layers import Activation, BatchNormalization, Conv2D
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.models import Model

def eight_block_model(encoder, value_hidden, policy_hidden):
    data_format = 'channels_first'
    value_hidden_layer = value_hidden
    policy_hidden_layer = policy_hidden
    board_input = Input(shape=encoder.shape(), name='board_input')

    pb = board_input
    conv_filters = [32]*8
    conv_kernels = [(3, 3)]*8
    for i in range(8):
        pb = Conv2D(conv_filters[i], conv_kernels[i],
            padding='same', data_format = data_format)(pb)
        pb = BatchNormalization(axis=1)(pb)
        pb = Activation('relu')(pb)
    
    # Policy output
    policy_conv = Conv2D(2, (1, 1), data_format = data_format, name = 'policy_conv')(pb)
    policy_batch = BatchNormalization(axis=1, name = 'policy_batchnorm')(policy_conv)
    policy_relu = Activation('relu', name = 'policy_relu')(policy_batch)
    policy_flat = Flatten(name = 'policy_flat')(policy_relu)
    policy_hidden = Dense(policy_hidden_layer, activation='relu', name = 'policy_hidden')(policy_flat)
    policy_output = Dense(encoder.num_points(), activation='softmax', name = 'policy_out')(
        policy_hidden)
    
    # Value output
    value_conv = Conv2D(1, (1, 1), data_format = data_format, name = 'value_conv')(pb)
    value_batch = BatchNormalization(axis=1, name = 'value_batchnorm')(value_conv)
    value_relu = Activation('relu', name = 'value_relu')(value_batch)
    value_flat = Flatten(name = 'value_flat')(value_relu)
    value_hidden = Dense(value_hidden_layer, activation='relu', name = 'value_hidden')(value_flat)
    value_output = Dense(1, activation='tanh', name = 'value_out')(value_hidden)
    
    model = Model(
        inputs=[board_input],
        outputs=[policy_output, value_output])
    
    return model