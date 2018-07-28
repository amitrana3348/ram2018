from firebase import firebase
fb = firebase.FirebaseApplication('https://ramkarde-3348.firebaseio.com/', None)
fb.put('ram',"count",65) #"path","property_Name",property_Value
