import random

from locust import HttpUser, task, between

class FileUser(HttpUser):
    # Specifies the wait time for a user between executing tasks
    wait_time = between(1, 2.5)

    # Host address (the target system under test)
    # Make sure your service is running at this location
    host = "http://localhost:8000"

    @task
    def get_files(self):
        """
        Represents one user task, which in this case, is sending a GET request to "/files".
        """
        # Sending GET request to the "/files" endpoint
        response = self.client.get("/files")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @task
    def get_file(self):
        """
        Represents one user task, which in this case, is sending a GET request to "/files".
        """
        file_id = random.randrange(1, 10)
        # Sending GET request to the "/files" endpoint
        response = self.client.get(f"/files/{file_id}")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @task
    def post_file(self):
        """
        Represents one user task, which in this case, is sending a POST request to "/files".
        """
        file_id = random.randrange(1, 10)
        # Sending POST request to the "/files" endpoint
        response = self.client.post("/files", json={"file_id": file_id})
        assert response.status_code == 201, f"Unexpected status code: {response.status_code}"

    @task
    def get_records(self):
        file_id = random.randrange(1, 10)
        response = self.client.get(f"/files/{file_id}/records")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @task
    def get_record(self):
        file_id = random.randrange(1, 10)
        record_id = random.randrange(1, 20)
        response = self.client.get(f"/files/{file_id}/records/{record_id}")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

# Optional setup for running with command-line flags
# You could customize these values by passing them as arguments on the command line
# For instance, you could set the number of users to simulate, spawn rate, and test run time
if __name__ == "__main__":
    import os
    from locust.main import main

    # Add default options for command line execution
    os.environ["LOCUST_OPTS"] = "--users 100 --spawn-rate 10 --run-time 1m"
    main()
