# -*- coding: utf-8 -*-
"""
Mining Assignment 1
"""

import math

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # metric:
    # metric is in the form of a string. it can be any of the following:
    # "minkowski", "cosine", "pearson"
    #     recall that manhattan = minkowski with r=1, and euclidean = minkowski with r=2
    # defaults to "pearson"
    #
    # r:
    # minkowski parameter
    # set to r for minkowski, and ignored for cosine and pearson
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    def __init__(self, usersItemRatings, metric='pearson', r=1, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings

        # set self.metric and self.similarityFn
        if metric.lower() == 'minkowski':
            self.metric = metric
            self.similarityFn = self.minkowskiFn
        elif metric.lower() == 'cosine':
            self.metric = metric
            self.similarityFn = self.cosineFn
        elif metric.lower() == 'pearson':
            self.metric = metric
            self.similarityFn = self.pearsonFn
        else:
            print ("    (DEBUG - metric not in (minkowski, cosine, pearson) - defaulting to pearson)")
            self.metric = 'pearson'
            self.similarityFn = self.pearsonFn
        
        # set self.r
        if (self.metric == 'minkowski'and r > 0):
            self.r = r
        elif (self.metric == 'minkowski'and r <= 0):
            print ("    (DEBUG - invalid value of r for minkowski (must be > 0) - defaulting to 1)")
            self.r = 1
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (DEBUG - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            
    
    #################################################
    # minkowski distance (dis)similarity - most general distance-based (dis)simialrity measure
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def minkowskiFn(self, userXItemRatings, userYItemRatings):
        
        distance = 0
        commonRatings = False 
        
        for item in userXItemRatings:
            # inlcude item rating in distance only if it exists for both users
            if item in userYItemRatings:
                distance += pow(abs(userXItemRatings[item] - userYItemRatings[item]), self.r)
                commonRatings = True
                
        if commonRatings:
            return round(pow(distance,1/self.r), 2)
        else:
            # no ratings in common
            return -2

    #################################################
    # cosince similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def cosineFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x2 = 0
        sum_y2 = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        
        denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
        if denominator == 0:
            return -2
        else:
            return round(sum_xy / denominator, 3)

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                n += 1
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
       
        if n == 0:
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        # YOUR CODE HERE
        
        # for given userX, get the sorted list of users - by most similar to least similar        
        
        # calcualte the weighted average item recommendations for userX from userX's k NNs
        
        # return sorted list of recommendations (sorted highest to lowest ratings)
        # example: [('Broken Bells', 2.64), ('Vampire Weekend', 2.2), ('Deadmau5', 1.71)]
        
        # once you are done coding this method, delete the pass statement below
        
        
        # Calculate Distance of the input user with other users in the master dictionary - songData. 
        # Call Similarity Function with arguments as input user and any other user one at a time in for loop.
        distance= {}
        for (k,v) in self.usersItemRatings.items():
            if k != userX:
               distance[k]=self.similarityFn(self.usersItemRatings[userX],self.usersItemRatings[k])
                
        # Sort the caculated distances in order to be able to select the least, highest or any specific type of elements required.
        #The distancesorted is a list of tuples with each tuple being sorted in key, value pair in ascending order of values in the list.
        # The distance caclculated is taken care in the minkowski function for values of r=1,2 or 3
        from operator import itemgetter        
        distancesorted = sorted(distance.items(), key=itemgetter(1))
                    
        # Caculate Euclidean, Manhattan and Minkowski distances if input is minkowski       
        if self.metric == 'minkowski':
           # Select the least distance key from the distancesorted list of tuples. This wills elect the user closest to Input User.
           for key,value in distancesorted:
               selectedKey = key
               break
           
           # Assign the Input User Ratings and ratings of user with least distances to the below dictionaries.
           userDerived=self.usersItemRatings[selectedKey]
           userCompared=self.usersItemRatings[userX]
           
           #Create outputMatrix dictionary which will have the suggested output ratings for the input user
           #The below for condition iterates through Input User and the User with least distance from inout users.
           outputMatrix={}
           for (k,v) in userDerived.items():
               counter=0
               for (k1,v1) in userCompared.items():
                    if k == k1:
                       counter=counter+1
               #Each counter that does not get assigned ensures that the key in the lowest distance user                
               if counter==0:
                    outputMatrix[k]=v
           print(list(sorted(outputMatrix.items())))
        
        #Calculate suggest ratings for cosine
        elif self.metric == 'cosine':
             for key,value in distancesorted:
                 selectedKey = key
             
             #Assign the lowest value key to selectedKey variable
             userDerived=self.usersItemRatings[selectedKey]
             userCompared=self.usersItemRatings[userX]

             #Create outputMatrix dictionary which will have the suggested output ratings for the input user for cosine or pearson.              
             outputMatrix={}
             for (k,v) in userDerived.items():
                 counter=0
                 for (k1,v1) in userCompared.items():
                     if k == k1:
                        counter=counter+1
                 if counter==0:
                    outputMatrix[k]=v
             print(list(sorted(outputMatrix.items())))        
        #Calulate the ratings for pearson.      
        elif self.metric == 'pearson':
            #This IF condition will take care of k=1 default case
            if self.k == 1:
               #Assign the keys from the distancessorted list of tuples to selectedkey variable
               for key,value in distancesorted:
                   selectedKey = key
               #Assign the user from selectedkey variable and input user to respective dictionaries below.
               userDerived=self.usersItemRatings[selectedKey]
               userCompared=self.usersItemRatings[userX]
                             
               #Create outputMatrix dictionary which will have the suggested output ratings for the input user for cosine or pearson.              
               outputMatrix={}
               for (k,v) in userDerived.items():
                    counter=0
                    for (k1,v1) in userCompared.items():
                        if k == k1:
                           counter=counter+1
                    if counter==0:
                       outputMatrix[k]=v
               print(list(sorted(outputMatrix.items())))
            else:
                 #This else black takes care of all conditions of k which are greater than 1 like 2,3,4 etc.,
                 values = list(distance.values())
                 
                 #Select the sorted values from the distance array into valuessorted variable
                 valuessorted = sorted(values)                 
                 length =len(valuessorted)
                 #Select the top n elements for caclculating the k nearest neighbors
                 topelements = valuessorted[(length-self.k):length]
                 #Do the pearson calculation on the selected n neigbors. 
                 pearsonknn=list(map(lambda pc:round(((pc+1)/2),2), topelements))
                 #Calculate the weights from the pearson coefficients above.
                 weights = list(map(lambda pk:round((pk/sum(pearsonknn)),2), pearsonknn))
                 
                 #Select the corresponding keys for each weights.
                 sortedkeys=[]
                 for i in range(len(topelements)):
                     for (k,v) in distance.items():
                         if topelements[i] == v:
                             sortedkeys.append(k)
                 
                 #Calculate the ratings based on weights for knn.              
                 userCompared=self.usersItemRatings[userX]
                 outputMatrix={}
                 for i in range(len(sortedkeys)):
                     for (k,v) in self.usersItemRatings[sortedkeys[i]].items():
                          counter=0
                          for (k1,v1) in userCompared.items():
                             #print (k1,v1)
                             if k == k1:
                                counter=counter+1
                                
                          if counter==0:
                             if k in outputMatrix.keys():
                                 outputMatrix[k]=round((outputMatrix[k]+v*weights[i]),2)
                             else:
                                 outputMatrix[k]=round(v*weights[i],2)
                 #Print the KNN Caculated Ratings 
                 print(list(outputMatrix.items()))