__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Smith, Steven", "Siraj, Ambareen",
                    "Hope, Shelby"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

#importing the library
import pandas as pd

#importing the data set
dataset = pd.read_excel("Updated_Final_Processed_Data_Set_TCP_Seq_12_12_2018.xlsx")

# X and Y
Y = dataset.iloc[:, -1].values
X = dataset.iloc[:,:-1].values

# Spliting the dataset into the Training and Test Set
from sklearn.cross_validation import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

'''# Fitting SVM (Linear Kernel) to the Training Set
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, Y_train)'''

# Fitting SVM (Gaussian RBF Kernel) to the Training Set
from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0)
classifier.fit(X_train, Y_train)

# Predicting the Test set results
Y_pred = classifier.predict(X_test)

# Making the confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, Y_pred)

# Knowing accuracy result
from sklearn.metrics import accuracy_score
print(accuracy_score(Y_test, Y_pred))