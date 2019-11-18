#import subprocess
import socket
import tkinter as tk
import wmi

# Refresh current IP at set interval
UPDATE_RATE = 1000

# Create window using tkinter.
class IpWindow(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		# Obtain network adaptors configurations
		nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

		# How many nics were found with IP enabled.
		num_nics = len(nic_configs)        
		print(f'Number of Nics: {num_nics}')

		# Declare variables for 2 different interfaces
		self.nic = nic_configs[0]
		self.nic2 = nic_configs[1]

		# Get Descriptions for each interface
		self.int_1_desc = self.nic.Description
		self.int_2_desc = self.nic2.Description

		self.desc_list = [self.int_1_desc, self.int_2_desc]

		print (self.desc_list)

		# Print interface descriptions
		print(f"Interface 1 is: {self.int_1_desc}")
		print(f"Interface 2 is: {self.int_2_desc}")

		c = wmi.WMI()
		c.Win32_ComputerSystem.methods.keys()

		# Init drop down list.
		master = parent
		self.variable = tk.StringVar(master)
		# Set interface 0 to be default in list.
		self.variable.set(self.desc_list[0])
		


		# create a prompt, an input box, an output label,
		# and a button to do the computation
		self.prompt = tk.Label(self, justify="center", text="Enter an IP Address:")
		self.entry = tk.Entry(self, justify="center")
		self.current = tk.Label(self, text="")
		self.submit_ip = tk.Button(self, text="Set IP", command=self.set_ip)
		self.output = tk.Label(self, text="Format: x.x.x.x")
		self.dhcp = tk.Button(self, text="DHCP", command=self.set_dhcp)
		self.hard_ip_1 = tk.Button(self, text="192.168.0.253", command=self.set_hard_ip_1)
		self.hard_ip_2 = tk.Button(self, text="192.168.1.253", command=self.set_hard_ip_2)
		self.current_ip = tk.Label(self,text=f"Current IP is: x")
		self.drop_down = tk.OptionMenu(self, self.variable, *self.desc_list)

		# lay the widgets out on the screen.
		self.drop_down.pack(side="top", fill="x", padx=40)
		self.prompt.pack(side="top", fill="x")
		self.entry.pack(side="top", fill="x", padx=100)
		self.output.pack(side="top", fill="x", expand=True)
		self.hard_ip_1.pack(side="bottom", fill="x", padx=100)
		self.hard_ip_2.pack(side="bottom", fill="x", padx=100, pady=10)
		self.current_ip.pack(side="bottom", fill="x", padx=30, pady=10)
		self.submit_ip.pack(side="right", padx=50)
		self.dhcp.pack(side="left", padx=50)
		

		# Initialize number of refreshes.
		self.num_refresh = 0
		# Start auto updating current IP
		self.updater()

	def drop_down(self):
		pass

	def get_current_ip(self):

		# Add one to num_refresh per refresh and print number.
		self.num_refresh += 1
		print(f"Refreshed current IP {self.num_refresh} times.")

		hostname = socket.gethostname()
		socket_ip = socket.gethostbyname(hostname)
		self.current_ip.config(text=f"Device IP is currently: {socket_ip}")


	def set_hard_ip_1(self):

		ip = u'192.168.0.253'
		subnetmask = u'255.255.255.0'
		gateway = u'192.168.0.1'

		#is_ip_configurable = self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])

		#if is_ip_configurable == (0,):
		self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
		self.output.configure(text=f"Device IP set to {ip}")
		print(f"Device IP Set to {ip}")
		#else:
			# Draw result to window
			#self.output.configure(text="Device not configurable")
			#print("Device not configurable")

	def set_hard_ip_2(self):

		ip = u'192.168.1.253'
		subnetmask = u'255.255.255.0'
		gateway = u'192.168.1.1'

		#is_ip_configurable = self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])

		#if is_ip_configurable == (0,):
		self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
		self.output.configure(text=f"Device IP set to {ip}")
		print(f"Device IP Set to {ip}")
		#else:
			# Draw result to window
			#self.output.configure(text="Device not configurable")
			#print("Device not configurable")

	def set_dhcp(self):

		# Check to see if the interface can be set to dhcp
		# Return 0 = configurable
		is_dhcp_configurable = self.nic.EnableDHCP()

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
		#is_ip_configurable = self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])

		#if is_ip_configurable == (0,):
			#self.nic.ReleaseDHCPLease()
		self.nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
		self.output.configure(text=f"Device IP set to {ip}")

		print(f"Device IP Set to {ip}")
		#else:
			# Draw result to window
			#self.output.configure(text="Use Format x.x.x.x")
			#print("Use Format x.x.x.x")
			
		# If i want to set gateway
		# self.nic.SetGateways(DefaultIPGateway=[gateway])

	def updater(self):
		# Refresh current IP at set interval in global variable
		self.get_current_ip()
		self.after(UPDATE_RATE, self.updater)


# if this is run as a program (versus being imported),
	# create a root window and an instance of our example,
	# then start the event loop

if __name__ == "__main__":

	root = tk.Tk()
	root.title("IP address Changer")
	
	# Set window size and location
	root.geometry("400x250+1500+750")
	IpWindow(root).pack(fill="both", expand=True)

	root.mainloop()