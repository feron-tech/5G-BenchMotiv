import docker
import socket
from helper import Helper
import gparams
class Orchestrator:
	def __init__(self):
		self.orch = docker.from_env()
		self.helper=Helper()
	def get_all_ifaces(self):
		final_list = []
		list_of_tuples = socket.if_nameindex()
		for tuple in list_of_tuples:
			try:
				final_list.append(tuple[1])
			except:
				pass
		return final_list

	def activate(self,image,detach=True,env=None,network_mode='bridge'):
		try:
			initial_list_of_ifaces=self.get_all_ifaces()

			if env is None:
				if network_mode is None:
					self.orch.containers.run(image, detach=detach, remove=True)
				else:
					self.orch.containers.run(image, detach=detach, network_mode=network_mode, remove=True)
			else:
				if network_mode is None:
					self.orch.containers.run(image, detach=detach,environment=env,remove=True)
				else:
					self.orch.containers.run(image, detach=detach,environment=env,network_mode=network_mode,remove=True)
			print('(Orch) DBG: Activated container OK')

			attempt=1
			res=None
			while (res is None):
				print('(Backend) DBG: Seaching for iface (attempt=' + str(attempt) + ')...')

				if attempt > 1:
					self.helper.wait(gparams._WAIT_SEC_BACKEND_READ_INPUT_SOURCES)

				final_list_of_ifaces=self.get_all_ifaces()
				for final_iface in final_list_of_ifaces:
					if (final_iface not in initial_list_of_ifaces) and ('veth' in final_iface):
						res=final_iface
						print('(Orch) DBG: Iface found='+str(res))
						break

				attempt = attempt + 1

				if attempt >= gparams._ATTEMPTS_BACKEND_READ_INPUT_SOURCES:
					print('(Orch) ERROR: Cannot find iface during activation!')
					return None
			return res
		except Exception as ex:
			print('(Orch) ERROR: Failed to activate container=' + str(ex))
			return None

	def deactivate(self,image):
		try:
			initial_list_of_ifaces = self.get_all_ifaces()

			found=False
			container_list=self.orch.containers.list()
			for cont in container_list:
				if cont.attrs['Config']['Image']==image:
					cont.stop()
					found=True
					print('(Orch) DBG: De-activated container OK!')
					return 200
			if not found:
				print('(Orch) ERROR: Failed to find image during container dactivation, image=' + str(image))
				return None

			attempt = 1
			res = None
			while (res is None):
				print('(Backend) DBG: Seaching for iface (attempt=' + str(attempt) + ')...')

				if attempt > 1:
					self.helper.wait(gparams._WAIT_SEC_BACKEND_READ_INPUT_SOURCES)

				final_list_of_ifaces = self.get_all_ifaces()
				for init_iface in initial_list_of_ifaces:
					if (init_iface not in final_list_of_ifaces) and ('veth' in init_iface):
						res = init_iface
						print('(Orch) DBG: Iface found=' + str(res))
						break

				attempt = attempt + 1

				if attempt >= gparams._ATTEMPTS_BACKEND_READ_INPUT_SOURCES:
					print('(Orch) ERROR: Cannot find iface during DE-activation!')
					return None
			return res

		except Exception as ex:
			print('(Orch) ERROR: Failed to de-activate container=' + str(ex))
			return None

	def misc(self):
		#container.attrs['Config']['Image']
		#orch.images.pull('nginx')
		#orch.images.list()
		pass




