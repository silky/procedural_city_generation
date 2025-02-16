import sys,os
import procedural_city_generation
donemessage="\n-------------------------------------------------------------------------------\n\t\t\t  Done, waiting for command\n-------------------------------------------------------------------------------"
path=os.path.dirname(procedural_city_generation.__file__)
sys.path.append(path)

def roadmap():
	from procedural_city_generation.roadmap import main as roadmap_main
	roadmap_main.main()

def polygons():
	from procedural_city_generation.polygons import main as polygon_main
	polygon_main.main(None)

def building_generation():
	from procedural_city_generation.building_generation import main as building_generation_main
	import pickle
	try:
		with open(path+"/outputs/polygons.txt",'r') as f:
			polygons=pickle.loads(f.read())	
		building_generation_main.main(polygons)
	except IOError:
		print "Input could not be located. Try to run the previous program in the chain first."
		return 0

	
def visualization():
	os.system("blender --python "+path+"/visualization/blenderize.py")

def main(args):
	"""
	
	Welcome to procedural_city_generation, a module for procedurally generating a 3D model of a city in Blender with python.
	
	A call to this module from the command line should follow this format::
	
		python UI.py <submodule-name> <options>
	
	<submodule-name> is either "roadmap","polygons","building_generation,"visualization".
	<options> is either "run" or "configure"
	"""
	
	if len(args)==1:
		print main.__doc__
		return 0
	if "configure" in args[2]:
		if len(args)==3:
			os.system("nano ./procedural_city_generation/inputs/"+args[1]+".conf")
			sys.exit(0)
		
		elif args[3] and args[4]:
			import json
			with open("./procedural_city_generation/inputs/"+args[1]+".conf",'r') as f:
				wb=json.loads(f.read())
			i=0
			while True:
				try:
					
					old=wb[args[3+i]]
					wb[args[3+i]]=args[4+i]
					print args[3+i], " was changed from ",old," to ",args[4+i]
					i+=2
					if len(args)-1<i+4:
						return 0
					
				except:
					print i, len(args)
					print "Either ",args[3+i], "is not a configurable parameter for ",args[1]
					return 0
					
			with open("./procedural_city_generation/inputs/"+args[1]+".conf",'w') as f:
				f.write(json.dumps(wb))
			print main.__doc__
			return 0
	elif "run" in args[2]:
		eval(args[1])()
		print donemessage
			
if __name__=='__main__':
	print sys.argv
	main(sys.argv)
