# import tensorflow as tf
# from tensorflow import keras
import tensorflow.keras as keras

def create_neural_network(len_input):
	number_neurons = [6, 5, 4]
	model = keras.models.Sequential()
	model.add( keras.layers.Dense(number_neurons[0], input_shape=(len_input, )))
	model.add( keras.layers.Activation("sigmoid") )
	model.add( keras.layers.Dropout(0.4) )
	model.add( keras.layers.Dense(number_neurons[1], input_shape=(number_neurons[0], )))
	model.add( keras.layers.Activation("sigmoid") )
	model.add( keras.layers.Dropout(0.4) )
	model.add( keras.layers.Dense(number_neurons[2], input_shape=(number_neurons[1], )))
	model.add( keras.layers.Activation("sigmoid") )
	model.add( keras.layers.Dropout(0.4) )
	#last layer
	model.add( keras.layers.Dense(3, input_shape=(number_neurons[2], )) )
	
	#configuring the learning process
	model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])	
	
	return model
	
def training(model, epochs, inputs, outputs):
	"train the model to fit the data"
	model.fit(inputs, outputs, epochs=epochs, batch_size=10)
	#see validation data arg
	
	
	