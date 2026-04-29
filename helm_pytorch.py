import torch
import numpy as np

class dHELM_PyTorch:
    def __init__(self, Y, slack_bus=0, device='cpu'):
        self.device = device
        
        # Ensure Y is a PyTorch tensor
        if isinstance(Y, np.ndarray):
            Y = torch.tensor(Y, device=self.device)
            
        self.Y = Y.to(torch.complex128).to(self.device)
        self.slack_bus = slack_bus
        
        # Separate the slack bus row/column
        Y_ns_rows = torch.cat([self.Y[:slack_bus], self.Y[slack_bus+1:]], dim=0)
        self.y_slack = Y_ns_rows[:, slack_bus]
        self.Y_ns = torch.cat([Y_ns_rows[:, :slack_bus], Y_ns_rows[:, slack_bus+1:]], dim=1)
        
        # Pre-calculate the inverse of the reduced Y-bus matrix
        self.Y_inv = torch.linalg.inv(self.Y_ns)
        
    def remove_slack(self, S):
        S1 = S[:, :self.slack_bus]
        S2 = S[:, self.slack_bus+1:]
        return torch.cat([S1, S2], dim=-1)
    
    def get_voltage(self, S, slack_v, iterations=50):
        """
        S: Complex power injections tensor (Batch, Buses - 1)
        slack_v: Tensor of slack bus voltages (Batch)
        """
        batch_num = S.shape[0]
        
        # --- FIX 1: Dynamically grab the device from the incoming neural network tensor ---
        curr_device = S.device 
        
        # Repeat slack admittance for batch dimension (ensure it's on curr_device)
        Y_slack = self.y_slack.to(curr_device).unsqueeze(0).expand(batch_num, -1)
        
        # Format slack voltage to complex [Batch, 1]
        slack_v_complex = torch.complex(
            slack_v.to(torch.float64), 
            torch.zeros_like(slack_v, dtype=torch.float64)
        ).unsqueeze(-1)

        # Base case (Order 0)
        term = -Y_slack * slack_v_complex
        
        # --- FIX 2: Move Y_inv to curr_device before matrix multiplication ---
        c0 = torch.einsum('ji,aj->ai', self.Y_inv.to(curr_device), term).unsqueeze(1)
        
        c_list = [c0]
        d_list = [1.0 / c0]

        # Recursive power series coefficients
        for n in range(iterations - 1):
            RHS = torch.conj(S) * torch.conj(d_list[-1][:, 0, :])
            # --- FIX 3: Move Y_inv here as well ---
            new_c = torch.einsum('ij,aj->ai', self.Y_inv.to(curr_device), RHS).unsqueeze(1)
            c_list.append(new_c)
            
            c_tensor = torch.cat(c_list, dim=1)
            d_tensor = torch.cat(d_list, dim=1)
            
            # Convolution step: sum(c[n-k] * d[k])
            c_rev = torch.flip(c_tensor[:, 1:, :], dims=[1])
            new_d = -torch.sum(c_rev * d_tensor, dim=1, keepdim=True) / c_tensor[:, 0:1, :]
            d_list.append(new_d)

        # Combine all iteration coefficients [Batch, Iterations, Buses-1]
        c = torch.cat(c_list, dim=1)

        # Helper function for Padé Approximant (Wynn Epsilon)
        def pade_approx_1(an):
            m = int(iterations / 2)
            N = iterations - 1
            n = int((iterations - 1) - (iterations / 2))
            
            an = an.unsqueeze(1) # [Batch, 1, Iterations]
            
            # --- FIX 4: Ensure all internally generated tensors use curr_device ---
            A = torch.eye(N + 1, n + 1, dtype=torch.complex128, device=curr_device).unsqueeze(0).expand(batch_num, -1, -1)
            B_list = [torch.zeros((batch_num, 1, m), dtype=torch.complex128, device=curr_device)]
            
            for row in range(1, m + 1):
                z = torch.zeros((batch_num, 1, m - row), dtype=torch.complex128, device=curr_device)
                rev_an = -torch.flip(an[:, :, :row], dims=[2])
                B_list.append(torch.cat([rev_an, z], dim=2))
            for row in range(m + 1, N + 1):
                rev_an = -torch.flip(an[:, :, row - m:row], dims=[2])
                B_list.append(rev_an)
            
            B = torch.cat(B_list, dim=1)
            C = torch.cat([A, B], dim=2)
            
            # Solve AX = B
            rhs = torch.transpose(an, 1, 2)
            pq = torch.linalg.solve(C, rhs).squeeze(2)
            
            p = torch.sum(pq[:, :n + 1], dim=-1)
            q = 1.0 + torch.sum(pq[:, n + 1:], dim=-1)
            
            return p / q

        # Apply Padé approximation across all buses
        v_list = []
        for bus_i in range(c.shape[2]):
            v_list.append(pade_approx_1(c[:, :, bus_i]))
            
        v = torch.stack(v_list, dim=1) # Shape: [Batch, Buses-1]
        
        # Re-insert the slack bus voltage
        v = torch.cat([v[:, :self.slack_bus], slack_v_complex, v[:, self.slack_bus:]], dim=1)
        
        # Verify physical power constraints (S_out)
        v_mat = torch.einsum('ai,aj->aij', torch.conj(v), v)
        
        # --- FIX 5: Move original Y to curr_device for power verification ---
        S_out = torch.conj(torch.sum(v_mat * self.Y.to(curr_device), dim=-1))
        
        S_ns = self.remove_slack(S_out)
        err = torch.max(torch.abs(S_ns - S), dim=-1)[0]
        
        return v, S_out, torch.log(err), c

# import torch
# import numpy as np

# class dHELM_PyTorch:
#     def __init__(self, Y, slack_bus=0, device='cpu'):
#         self.device = device
        
#         # Ensure Y is a PyTorch tensor
#         if isinstance(Y, np.ndarray):
#             Y = torch.tensor(Y, device=self.device)
            
#         self.Y = Y.to(torch.complex128).to(self.device)
#         self.slack_bus = slack_bus
        
#         # Separate the slack bus row/column
#         Y_ns_rows = torch.cat([self.Y[:slack_bus], self.Y[slack_bus+1:]], dim=0)
#         self.y_slack = Y_ns_rows[:, slack_bus]
#         self.Y_ns = torch.cat([Y_ns_rows[:, :slack_bus], Y_ns_rows[:, slack_bus+1:]], dim=1)
        
#         # Pre-calculate the inverse of the reduced Y-bus matrix
#         self.Y_inv = torch.linalg.inv(self.Y_ns)
        
#     def remove_slack(self, S):
#         S1 = S[:, :self.slack_bus]
#         S2 = S[:, self.slack_bus+1:]
#         return torch.cat([S1, S2], dim=-1)
    
#     def get_voltage(self, S, slack_v, iterations=50):
#         """
#         S: Complex power injections tensor (Batch, Buses - 1)
#         slack_v: Tensor of slack bus voltages (Batch)
#         """
#         batch_num = S.shape[0]
        
#         # Repeat slack admittance for batch dimension
#         Y_slack = self.y_slack.unsqueeze(0).expand(batch_num, -1)
        
#         # Format slack voltage to complex [Batch, 1]
#         slack_v_complex = torch.complex(
#             slack_v.to(torch.float64), 
#             torch.zeros_like(slack_v, dtype=torch.float64)
#         ).unsqueeze(-1)

#         # Base case (Order 0)
#         # term = -Y_slack * slack_v_complex
#         term = -Y_slack.to(slack_v_complex.device) * slack_v_complex
#         c0 = torch.einsum('ji,aj->ai', self.Y_inv, term).unsqueeze(1)
        
#         c_list = [c0]
#         d_list = [1.0 / c0]

#         # Recursive power series coefficients
#         for n in range(iterations - 1):
#             RHS = torch.conj(S) * torch.conj(d_list[-1][:, 0, :])
#             new_c = torch.einsum('ij,aj->ai', self.Y_inv, RHS).unsqueeze(1)
#             c_list.append(new_c)
            
#             c_tensor = torch.cat(c_list, dim=1)
#             d_tensor = torch.cat(d_list, dim=1)
            
#             # Convolution step: sum(c[n-k] * d[k])
#             c_rev = torch.flip(c_tensor[:, 1:, :], dims=[1])
#             new_d = -torch.sum(c_rev * d_tensor, dim=1, keepdim=True) / c_tensor[:, 0:1, :]
#             d_list.append(new_d)

#         # Combine all iteration coefficients [Batch, Iterations, Buses-1]
#         c = torch.cat(c_list, dim=1)

#         # Helper function for Padé Approximant (Wynn Epsilon)
#         def pade_approx_1(an):
#             m = int(iterations / 2)
#             N = iterations - 1
#             n = int((iterations - 1) - (iterations / 2))
            
#             an = an.unsqueeze(1) # [Batch, 1, Iterations]
            
#             A = torch.eye(N + 1, n + 1, dtype=torch.complex128, device=self.device).unsqueeze(0).expand(batch_num, -1, -1)
#             B_list = [torch.zeros((batch_num, 1, m), dtype=torch.complex128, device=self.device)]
            
#             for row in range(1, m + 1):
#                 z = torch.zeros((batch_num, 1, m - row), dtype=torch.complex128, device=self.device)
#                 rev_an = -torch.flip(an[:, :, :row], dims=[2])
#                 B_list.append(torch.cat([rev_an, z], dim=2))
#             for row in range(m + 1, N + 1):
#                 rev_an = -torch.flip(an[:, :, row - m:row], dims=[2])
#                 B_list.append(rev_an)
            
#             B = torch.cat(B_list, dim=1)
#             C = torch.cat([A, B], dim=2)
            
#             # Solve AX = B
#             rhs = torch.transpose(an, 1, 2)
#             pq = torch.linalg.solve(C, rhs).squeeze(2)
            
#             p = torch.sum(pq[:, :n + 1], dim=-1)
#             q = 1.0 + torch.sum(pq[:, n + 1:], dim=-1)
            
#             return p / q

#         # Apply Padé approximation across all buses
#         # Instead of tf.map_fn, we build a list over the bus dimension
#         v_list = []
#         for bus_i in range(c.shape[2]):
#             v_list.append(pade_approx_1(c[:, :, bus_i]))
            
#         v = torch.stack(v_list, dim=1) # Shape: [Batch, Buses-1]
        
#         # Re-insert the slack bus voltage
#         v = torch.cat([v[:, :self.slack_bus], slack_v_complex, v[:, self.slack_bus:]], dim=1)
        
#         # Verify physical power constraints (S_out)
#         v_mat = torch.einsum('ai,aj->aij', torch.conj(v), v)
#         S_out = torch.conj(torch.sum(v_mat * self.Y, dim=-1))
        
#         S_ns = self.remove_slack(S_out)
#         err = torch.max(torch.abs(S_ns - S), dim=-1)[0]
        
#         return v, S_out, torch.log(err), c