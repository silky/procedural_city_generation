from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt
import procedural_city_generation


class BuildingHeight(object):
	"""
	Manages and distributes building-heights for buildings 
	"""
	def __init__(self):
		
		print "Population density image is being set up"
		
		self.path=os.path.dirname(procedural_city_generation.__file__)
		self.img=self.setupimage(self.path)
		with open(self.path+"/temp/border.txt",'r') as f:
			self.border=[eval(x) for x in f.read().split(" ") if x is not '']
		print "Population density image setup is finished"
	
	
	def diffusion(self,arr, d):
		""" Simulates diffusion. Taken from Stackoverflow user [aizquier]
		(https://stackoverflow.com/questions/8102781/efficiently-doing-diffusion-on-a-2d-map-in-python)
		
		Parameters
		----------
		arr : np.ndarray(m,n)
			Array representing the grayscale image to be diffused
		d : float
		
		Returns
		-------
		np.ndarray(m,n)
		"""
		contrib = (arr * d)
		w = contrib / 8.0
		r = arr - contrib
		N = np.roll(w, shift=-1, axis=0)
		S = np.roll(w, shift=1, axis=0)
		E = np.roll(w, shift=1, axis=1)
		W = np.roll(w, shift=-1, axis=1)
		NW = np.roll(N, shift=-1, axis=1)
		NE = np.roll(N, shift=1, axis=1)
		SW = np.roll(S, shift=-1, axis=1)
		SE = np.roll(S, shift=1, axis=1)
		diffused = r + N + S + E + W + NW + NE + SW + SE
		return diffused


	def setupimage(self,path):
		"""
		Sets up the image for the building height data
		As of now, always takes a diffused version of the population density image
		
		Parameters
		----------
		path : String
			Path to the population density image
		
		Returns
		-------
		img : np.ndarray(m,n,3)
		
		"""
		import matplotlib.image as mpimg
		
		#TODO: make diffused an option, add constants to config file
		#TODO: FIX. When fixed, change docstring
		img= mpimg.imread(path+"/temp/diffused.png")
		with open(path+"/temp/isdiffused.txt",'r') as f:
			diffused_bool=f.read()
			f.close()
		
		if not diffused_bool=="True":
			for i in range(72):
				img= self.diffusion(img, 1)
			img=img**1.80
			plt.imsave(path+"/temp/diffused.png",img)
			
			with open(path+"/temp/isdiffused.txt",'w') as g:
				g.write("True")
				g.close()
		else:
			return img
		
		return img
		
		
	def getBuildingHeight(self,center):
		"""
		Gets buildingheight for a building 
		
		Parameters
		----------
		center : numpy.ndarray(2,1)
			xy-coordinates of the center of the building to get buildingheight for
		
		Returns
		-------
		float
		
		"""
		#TODO: Export numbers to some sort of constant-singleton)
		
		x = (center[0]+self.border[0])/(self.border[0]*2)
		y = (center[1]+self.border[1])/(self.border[1]*2)
		
		height= self.img[self.img.shape[0]-y*self.img.shape[0]][x*self.img.shape[1]][0]
		if 0<height<0.45:
			height=min(0.035+np.random.uniform(0,1)*np.random.uniform(0,height-0.1),0.6)
		elif 0.45<height:
			if height>0.70 and np.random.uniform(0,1)<0.2:
				height*=np.random.uniform(1.3,2.6)
			else:
				height=min(0.15+np.random.uniform(0,1)*np.random.uniform(0,height-0.2),0.6)
		return height 
	
