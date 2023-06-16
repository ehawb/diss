from tensorflow.keras.layers import Activation, BatchNormalization, Conv2D
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.models import Model

def fresh_model(encoder, value_hidden, policy_hidden):
    value_hidden_layer = value_hidden
    policy_hidden_layer = policy_hidden
    board_input = Input(shape=encoder.shape(), name='board_input')

    pb = board_input
    conv_filters = [32]*4
    conv_kernels = [(3, 3)]*4
    for i in range(4):
        pb = Conv2D(conv_filters[i], conv_kernels[i],
            padding='same')(pb)
        pb = BatchNormalization(axis=1)(pb)
        pb = Activation('relu')(pb)
    
    # Policy output
    policy_conv = Conv2D(2, (1, 1),)(pb)
    policy_batch = BatchNormalization(axis=1)(policy_conv)
    policy_relu = Activation('relu')(policy_batch)
    policy_flat = Flatten()(policy_relu)
    policy_hidden = Dense(policy_hidden_layer, activation='relu')(policy_flat)
    policy_output = Dense(encoder.num_points(), activation='softmax')(
        policy_hidden)
    
    # Value output
    value_conv = Conv2D(1, (1, 1),)(pb)
    value_batch = BatchNormalization(axis=1)(value_conv)
    value_relu = Activation('relu')(value_batch)
    value_flat = Flatten()(value_relu)
    value_hidden = Dense(value_hidden_layer, activation='relu')(value_flat)
    value_output = Dense(1, activation='tanh')(value_hidden)
    
    model = Model(
        inputs=[board_input],
        outputs=[policy_output, value_output])
    
    return model