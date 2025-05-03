class Logger:

    def __init__(self):
        self._msg_dict = {}


    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        """
        The time complexity is O(n).
        The space complexity is O(1).
        """
        if message not in self._msg_dict:
            self._msg_dict[message] = timestamp
            return True

        if timestamp - self._msg_dict[message] >= 10:
            self._msg_dict[message] = timestamp
            return True
        else:
            return False


# Your Logger object will be instantiated and called as such:
# obj = Logger()
# param_1 = obj.shouldPrintMessage(timestamp,message)
