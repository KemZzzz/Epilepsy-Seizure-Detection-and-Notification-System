from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import seaborn as sns
import matplotlib.pyplot as plt
from preprocessing import X_test_reshaped, y_test_reshaped
from main import EMGClassifier


class ModelEvaluator:
    def __init__(self, model):
        self.model = model

    def evaluate_model(self, X_test, y_test):
        loss, accuracy = self.model.evaluate(X_test, y_test)
        print('Test loss:', loss)
        print('Test accuracy:', accuracy)

        return loss, accuracy

    def plot_confusion_matrix(self, y_test, y_pred, class_names=['Negative', 'Positive']):
        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.show()

    def plot_roc_curve(self, X_test, y_test):
        y_pred_proba = self.model.predict(X_test)
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)

        plt.figure(figsize=(5, 4))
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.show()


if __name__ == '__main__':
    classifier = EMGClassifier()
    evaluator = ModelEvaluator(classifier.model)
    loss, accuracy = evaluator.evaluate_model(X_test_reshaped, y_test_reshaped)
    test_pred = (classifier.model.predict(X_test_reshaped) > 0.5)
    print(classification_report(y_test_reshaped, test_pred))
    evaluator.plot_confusion_matrix(y_test_reshaped, test_pred)
    evaluator.plot_roc_curve(X_test_reshaped, y_test_reshaped)
