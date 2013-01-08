from ..models import *

class ResultCollection(list):
    """
    The ResultCollection class handles retrieval of statistics from multiple TestInstances.
    
    Extends the list class allowing for a collection of objects.
    """
    
    def append(self, test_instance):
        """
        Appends the TestInstance to the collection.
        
        @param TestInstance The TestInstance obect to add to the object.
        @throws TypeError If the object is not an instance of TestInstance 
        """
        if type(test_instance) != TestInstance:
            raise TypeError, "TestInstance is required, %s supplied" % type(test_instance)
        super(ResultCollection, self).append(test_instance)
        return
    
    def get_average_mark(self, test):
        """
        Returns the average mark for the every TestInstance matching the test.
        @param Test The test to search on.
        @return Float The float of average mark as percentage. 
        """
        return
    
    def get_median(self, test):
        """
        Returns the media for every TestInstance matching the test.
        @param Test The test to search on.
        @return Float The median of the test
        """
        return
    
    def get_highest(self, test):
        """
        Returns the TestInstance with the highest test score.
        @param Test The test to search on.
        @returns TestInstance Returns the TestInstance with the highest mark.
        """
        return
    
    def get_average_for_question(self, question):
        """
        Returns the average mark for that question in the ResultCollection
        @param Question The question object to search on.
        @return Float The average as a float. 
        """
        return
