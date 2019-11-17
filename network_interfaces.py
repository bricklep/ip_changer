#import subprocess
import socket
import tkinter as tk
import wmi


# Create window using tkinter.
class IpWindow(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		# Obtain network adaptors configurations
		nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

		# set nic to main adapter
		self.nic = nic_configs[0]

		# How many nics were found with IP enabled
		num_nics = len(nic_configs)        
		print(f'Number of Nics: {num_nics}')

		c = wmi.WMI()
		c.Win32_ComputerSystem.methods.keys()

		# create a prompt, an input box, an output label,
		# and a button to do the computation
		self.prompt = tk.Label(self, text="Enter an IP Address:", anchor="w")
		self.entry = tk.Entry(self)
		self.current = tk.Label(self, text="")
		self.submit_ip = tk.Button(self, text="Set IP", command=self.set_ip)
		self.output = tk.Label(self, text="Format: x.x.x.x")
		self.dhcp = tk.Button(self, text="DHCP", command=self.set_dhcp)
		self.hard_ip_1 = tk.Button(self, text="192.168.0.253", command=self.set_hard_ip_1)
		self.hard_ip_2 = tk.Button(self, text="192.168.1.253", command=self.set_hard_ip_2)
		self.current_ip = tk.Label(self,text=f"Current IP is: x")
		self.refresh_current_ip = tk.Button(self, text="Refresh Current IP", command=self.refresh_ip)

		# lay the widgets out on the screen. 
		self.prompt.pack(side="top", fill="x")
		self.entry.pack(side="top", fill="x", padx=20)
		self.output.pack(side="top", fill="x", expand=True)
		self.hard_ip_1.pack(side="bottom", fill="x", padx=50)
		self.hard_ip_2.pack(side="bottom", fill="x", padx=50, pady=10)
		self.current_ip.pack(side="bottom", fill="x", padx=30, pady=10)
		self.submit_ip.pack(side="right", padx=50)
		self.dhcp.pack(side="left", padx=50)
		self.refresh_current_ip.pack(side="top", fill="x")

		self.get_current_ip()

	def refresh_ip(self):

		self.get_current_ip()

	def get_current_ip(self):

		print("Refreshing Current IP")
		hostname = socket.gethostname()
		socket_ip = socket.gethostbyname(hostname)
		self.current_ip.config(text=f"Device IP set to: {socket_ip}")


	def set_hard_ip_1(self):

		ip = u'192.168.0.253'
		subnetmask = u'255.255.255.0'
		gateway = u'192.168.0.1'

		is_ip_configurable = self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
		print(is_ip_configurable)

		if is_ip_configurable == (0,):
			self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
			self.output.configure(text=f"Device IP set to {ip}")
			print(f"Device IP Set to {ip}")
		else:
			# Draw result to window
			self.output.configure(text="Device not configurable")
			print("Device not configurable")

	def set_hard_ip_2(self):

		ip = u'192.168.1.253'
		subnetmask = u'255.255.255.0'
		gateway = u'192.168.1.1'

		is_ip_configurable = self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
		print(is_ip_configurable)

		if is_ip_configurable == (0,):
			self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
			self.output.configure(text=f"Device IP set to {ip}")
			print(f"Device IP Set to {ip}")
		else:
			# Draw result to window
			self.output.configure(text="Device not configurable")
			print("Device not configurable")

	def set_dhcp(self):

		# Check to see if the interface can be set to dhcp
		# Return 0 = configurable
		is_dhcp_configurable = self.nic.EnableDHCP()
		print(is_dhcp_configurable)

		if is_dhcp_configurable == (0,):
			# set the interface to dhcp
			self.nic.EnableDHCP()
			# Draw output to screen
			self.output.configure(text="Device is configured to DCHP")
			print("Device is configured to DHCP")
		else:
			# Draw output to screen
			self.output.configure(text="Device not configurable")
			print("Device not configurable")

	def set_ip(self):
		# IP address, subnetmask and gateway values should be unicode objects
		
		# get input from window
		ip_get = self.entry.get()

		# Hard set IP and Mask
		ip = ip_get
		subnetmask = u'255.255.255.0'
		gateway = u'192.168.0.1'


		# Set IP address, subnetmask and default gateway
		# Note: EnableStatic() and SetGateways() methods require *lists* of values to be passed
		is_ip_configurable = self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
		print(is_ip_configurable)

		if is_ip_configurable == (0,):
			self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
			self.output.configure(text=f"Device IP set to {ip}")

			print(f"Device IP Set to {ip}")
		else:
			# Draw result to window
			self.output.configure(text="Device not configurable")
			print("Device not configurable")
			
		# If i want to set gateway
		# self.nic.SetGateways(DefaultIPGateway=[gateway])


# if this is run as a program (versus being imported),
	# create a root window and an instance of our example,
	# then start the event loop

if __name__ == "__main__":

	root = tk.Tk()
	root.title("IP address Changer")
	
	# Set window size and location
	root.geometry("400x200+1500+800")
	IpWindow(root).pack(fill="both", expand=True)

	root.mainloop()