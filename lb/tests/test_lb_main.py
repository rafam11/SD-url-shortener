# import pytest
# from load_balancer.utils.strategy import LoadBalancer


# class TestLoadBalancer:
#     """Test suite for a load balancer class."""

#     def test_round_robin_distribution(self):
#         """Test that requests are distributed in a round-robin way."""
#         servers = ["http://server1:8001", "http://server2:8002", "http://server3:8003"]
#         lb = LoadBalancer(servers=servers, strategy="round_robin")

#         assert lb.get_next_server() == "http://server1:8001"
#         assert lb.get_next_server() == "http://server2:8002"
#         assert lb.get_next_server() == "http://server3:8003"
#         assert lb.get_next_server() == "http://server1:8001"

#     def test_empty_server_list(self):
#         """Test that a ValueError is raised when there are no servers to balance."""
#         with pytest.raises(ValueError) as e:
#             LoadBalancer(servers=[], strategy="round_robin")

#         assert "Server list cannot be empty." in str(e.value)
