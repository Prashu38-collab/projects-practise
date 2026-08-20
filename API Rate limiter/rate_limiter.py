import time

class FixedWindowRateLimiter:
    def __init__(self,limit,windows_size):
        self.limit=limit
        self.window_size=windows_size
        self.clients={}
    
    def allow_request(self,client_id):
        current_time=time.time()

        # first request from a client
        if client_id not in self.clients:
            self.clients[client_id]={'request_count':0,'windows_start':current_time}
        client = self.clients[client_id]

         # Check whether the window has expired
        if current_time - client["window_start"] >= self.window_size:
            client["request_count"] = 0
            client["window_start"] = current_time
        # checking the limits

        if client["request_count"] < self.limit:
            client["request_count"] += 1
            return True
        return False