from launchpad import ModelInterface, ModelMakerInterface
import logging

logger = logging.getLogger(__name__)

# Train this example from the command line:
# python clitool.py -c examples/addition_cfg.yml -t
#
# Start REST API:
# python clitool.py -c examples/addition_cfg.yml -a
#
# Example API call:
# http://127.0.0.1:5000/add/v0?x1=3&x2=2


class MyAdditionExampleModelMaker(ModelMakerInterface):
    """Creates a model which adds (this can't really be called training)
    """

    def createTrainedModel(self, model_conf, data_sources, old_model=None):

        # We can get info from the model's config dictionary if necessary
        my_name = model_conf['name']
        logger.info("%s is doing lots of important preparation for addition...", my_name)

        # Imagine we are preparing data and training a sklearn or some other model here
        my_lame_predictor = lambda x1, x2: x1 + x2

        # Usually, we put one or several trained regressors/classifiers into the
        # model, but in this example we just use our function.
        modelContents = {'lame_pred': my_lame_predictor}
        # In addition to regressors/classifiers/etc., you can also use this to
        # tell prediction about e.g. calculated parameters, thresholds, etc.
        # that have been calculated during the training process.
        # For (near) constant parameters, please
        # use the config's model: prediction_config/training_config instead.

        # We instantiate our model class. This will be the object that will be
        # saved and later loaded to run in the API. You can get "modelContents"
        # at prediction time using the self.content property.
        finishedModel = MyAdditionExampleModel(content=modelContents)

        # We make sure that our model also comes with some test metrics
        metrics = self.testTrainedModel(model_conf, data_sources, finishedModel)

        # First return value: model instance, second value: metrics dict
        return finishedModel, metrics


    def testTrainedModel(self, model_conf, data_sources, model):

        # Okay, this is a stupid stand-in for preparing test data (usually you
        # have a specific data source for that)
        x1_test = 3
        x2_test = 7
        y_test = 10

        # Prediction happens here. Usually (though you *can*), you will not call
        # your own predict method, but get the inner model (classifier/regressor/...)
        # and use it directly.
        lame_predictor = model.content['lame_pred']
        y = lame_predictor(x1_test, x2_test)

        # Calculate some metrics
        acc = 1 if y == y_test else 0  # haha, I know

        # Adhere to consistent lower-case naming (accuracy, confusion_matrix, f1, etc.),
        # don't invent new names for common test metrics that will possibly be read
        # automatically in the model's life cycle management. You can add new
        # metrics if you want, just don't invent abbreviations like "acc" or such.
        metrics = {'accuracy': acc, 'precision': 'whatever'}

        return metrics


class MyAdditionExampleModel(ModelInterface):
    """Simplest possible "Data Science Model" example, without using data sources.
    """

    def predict(self, model_conf, data_sources, argsDict):

        # We can optionally get info from the model's config dictionary
        my_name = model_conf['name']
        logger.info("Hey, look at me, %s -- I'm adding two numbers!", my_name)

        # Get the parameters/arguments from the API call
        x1 = int(argsDict['x1'])
        x2 = int(argsDict['x2'])

        # Get the predictor from the dict that we stuffed into this model when training
        my_lame_predictor = self.content['lame_pred']

        # Our sophisticated model does its magic here
        y = my_lame_predictor(x1, x2)

        # We usually return a dict with prediction results
        return {"my_addition_result": y}
