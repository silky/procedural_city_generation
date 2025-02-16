#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

def main():
	from procedural_city_generation.roadmap.config import config
	from copy import copy

	singleton=config()
	
	front=copy(singleton.global_lists.vertex_list)
	front.pop(0)
	front.pop()
	vertex_queue = copy(singleton.global_lists.vertex_queue)
	from iteration import iteration
	singleton.iterationszaehler=0
	
	
	if singleton.plot==1:
		
		import matplotlib.pyplot as plt
		plt.close()
		fig=plt.figure()
		ax=plt.subplot(111)
		
		fig.canvas.draw()
		ax.set_xlim((-singleton.border[0],singleton.border[0]))
		ax.set_ylim((-singleton.border[1],singleton.border[1]))
	i=0
	while (front!=[] or singleton.global_lists.vertex_queue	!=[]):
		
		i+=1
		front=iteration(front)
		
		if singleton.plot==1:
			if i%singleton.plotabstand==0:
				plt.pause(0.001)
				fig.canvas.blit(ax.bbox)
				fig.canvas.flush_events()
			singleton.iterationszaehler=0

	from procedural_city_generation.additional_stuff.jsontools import save_vertexlist
	
	
	print "Roadmap is complete"
	if singleton.plot==1:
		plt.show()
	save_vertexlist(singleton.global_lists.vertex_list,"output",singleton.savefig)
	singleton.kill()
	return 0

	
if __name__ == '__main__':
	import os, sys
	parentpath=os.path.join(os.getcwd(),("../../"))
	sys.path.append(parentpath)
	main()
